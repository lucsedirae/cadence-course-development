#!/usr/bin/env python3
"""Local, two-library retrieval for the Cadence curriculum skill. No model calls."""
from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import tempfile

from extract import extract_file

LIBRARIES = ("content", "institution")
SCHEMA_VERSION = 1
CHUNK_SIZE = 2400
CHUNK_OVERLAP = 200
MAX_FILE_BYTES = 1024 ** 3
SOURCE_KEY = re.compile(r"^(content|institution)-[a-f0-9]{24}$")
PASSAGE_KEY = re.compile(r"^(content|institution):[a-f0-9]{24}:\d{6,}$")


def now():
    return datetime.now(timezone.utc).isoformat()


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def state_path(project):
    return Path(project).expanduser().resolve() / ".cadence"


def connect(project):
    path = state_path(project) / "library.sqlite3"
    if not path.is_file():
        raise ValueError("Initialize this course folder with the init command first.")
    connection = sqlite3.connect(path, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    if connection.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
        connection.close()
        raise ValueError("This library uses a different schema version; keep its files and use a compatible Cadence version.")
    return connection


def initialize(project, title):
    root = Path(project).expanduser().resolve()
    state = state_path(root)
    state.mkdir(parents=True, exist_ok=True)
    for folder in (state / "originals", state / "source_sets", root / "deliverables", root / "working" / "roles"):
        folder.mkdir(parents=True, exist_ok=True)
    path = state / "library.sqlite3"
    if path.exists():
        with closing(connect(root)) as connection:
            return {"project": str(root), "title": connection.execute("SELECT value FROM metadata WHERE key = 'title'").fetchone()[0], "existing": True}
    with closing(sqlite3.connect(path)) as connection, connection:
        connection.executescript("""
            CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE sources (
                id TEXT PRIMARY KEY, library TEXT NOT NULL CHECK(library IN ('content','institution')),
                name TEXT NOT NULL, original_path TEXT NOT NULL, sha256 TEXT NOT NULL,
                stored_file TEXT NOT NULL, imported_at TEXT NOT NULL, warnings TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1, passage_count INTEGER NOT NULL
            );
            CREATE TABLE passages (
                id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(id),
                ordinal INTEGER NOT NULL, locator TEXT NOT NULL, text TEXT NOT NULL,
                page INTEGER, slide INTEGER, unit_start INTEGER NOT NULL, unit_end INTEGER NOT NULL,
                UNIQUE(source_id, ordinal)
            );
            CREATE VIRTUAL TABLE passage_search USING fts5(passage_id UNINDEXED, text, tokenize='unicode61');
            CREATE INDEX source_current ON sources(library, original_path, active);
            CREATE INDEX passage_source ON passages(source_id, ordinal);
        """)
        connection.execute("INSERT INTO metadata VALUES ('title', ?)", (title,))
        connection.execute("INSERT INTO metadata VALUES ('created_at', ?)", (now(),))
        connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
    return {"project": str(root), "title": title, "existing": False, "libraries": list(LIBRARIES)}


def chunks(text):
    """Keep local offsets and overlap; never combine pages, slides or table units."""
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        if end < len(text):
            boundary = max(text.rfind("\n", start + CHUNK_SIZE // 2, end), text.rfind(" ", start + CHUNK_SIZE // 2, end))
            if boundary > start:
                end = boundary
        yield start, end, text[start:end]
        if end == len(text):
            break
        start = max(start + 1, end - CHUNK_OVERLAP)


def source_data(row):
    data = dict(row)
    data["warnings"] = json.loads(data["warnings"])
    data["active"] = bool(data["active"])
    return data


def ingest(project, library, filename):
    if library not in LIBRARIES:
        raise ValueError("Choose content or institution explicitly.")
    path = Path(filename).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"Source is not a file: {path}")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("Files must be 1 GB or smaller.")
    with closing(connect(project)) as connection:
        originals = state_path(project) / "originals"
        descriptor, temp_name = tempfile.mkstemp(prefix="import-", suffix=path.suffix.lower(), dir=originals)
        temporary = Path(temp_name)
        try:
            digest = hashlib.sha256()
            size = 0
            with os.fdopen(descriptor, "wb") as destination, path.open("rb") as source:
                while block := source.read(1024 * 1024):
                    size += len(block)
                    if size > MAX_FILE_BYTES:
                        raise ValueError("Files must be 1 GB or smaller.")
                    destination.write(block)
                    digest.update(block)
            sha = digest.hexdigest()
            key = hashlib.sha256(f"{library}\0{path}\0{sha}".encode()).hexdigest()[:24]
            source_id = f"{library}-{key}"
            existing = connection.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()
            if existing:
                with connection:
                    connection.execute("UPDATE sources SET active = 0 WHERE library = ? AND original_path = ?", (library, str(path)))
                    connection.execute("UPDATE sources SET active = 1 WHERE id = ?", (source_id,))
                return {**source_data(connection.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()), "reused": True}
            extracted = extract_file(temporary)
            stored = originals / f"{source_id}{path.suffix.lower()}"
            passage_count = 0
            # The original and database record are published only after extraction succeeds.
            with connection:
                connection.execute("INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0)",
                                   (source_id, library, path.name, str(path), sha, stored.name, now(), json.dumps(extracted.get("warnings", []))))
                for unit in extracted["units"]:
                    text = unit["text"].replace("\x00", "")
                    if not text.strip():
                        continue
                    for start, end, chunk in chunks(text):
                        passage_count += 1
                        passage_id = f"{library}:{key}:{passage_count:06d}"
                        connection.execute("INSERT INTO passages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                           (passage_id, source_id, passage_count, unit["locator"], chunk,
                                            unit.get("page"), unit.get("slide"), start, end))
                        connection.execute("INSERT INTO passage_search VALUES (?, ?)", (passage_id, chunk))
                if not passage_count:
                    raise ValueError("This file contains no readable text to index.")
                connection.execute("UPDATE sources SET active = 0 WHERE library = ? AND original_path = ? AND id != ?", (library, str(path), source_id))
                connection.execute("UPDATE sources SET passage_count = ? WHERE id = ?", (passage_count, source_id))
                temporary.replace(stored)
            return {**source_data(connection.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()), "reused": False}
        finally:
            temporary.unlink(missing_ok=True)


def list_sources(project, library=None, include_history=False):
    with closing(connect(project)) as connection:
        conditions, values = [], []
        if library:
            conditions.append("library = ?")
            values.append(library)
        if not include_history:
            conditions.append("active = 1")
        where = " WHERE " + " AND ".join(conditions) if conditions else ""
        return [source_data(row) for row in connection.execute("SELECT * FROM sources" + where + " ORDER BY library, name, imported_at", values)]


def snapshot(project):
    sources = list_sources(project)
    manifest = {"schema_version": SCHEMA_VERSION, "sources": sources}
    identifier = hashlib.sha256(encode(manifest).encode()).hexdigest()[:24]
    path = state_path(project) / "source_sets" / f"{identifier}.json"
    if not path.exists():
        # Exclusive creation keeps an existing snapshot intact, including concurrent callers.
        try:
            with path.open("x", encoding="utf-8") as file:
                file.write(encode(manifest))
        except FileExistsError:
            pass
    return {"snapshot": identifier, "manifest_path": str(path), "sources": sources}


def snapshot_sources(project, identifier):
    if not re.fullmatch(r"[a-f0-9]{24}", identifier):
        raise ValueError("Invalid snapshot identifier.")
    path = state_path(project) / "source_sets" / f"{identifier}.json"
    if not path.is_file():
        raise ValueError("Snapshot not found in this course folder.")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if hashlib.sha256(encode(manifest).encode()).hexdigest()[:24] != identifier:
        raise ValueError("Snapshot content has changed; use an intact source manifest.")
    return [source["id"] for source in manifest["sources"]]


def passage_data(row):
    data = dict(row)
    data["citation"] = f"[{data['id']}]"
    data["source_active"] = bool(data["source_active"])
    return data


PASSAGE_SELECT = """SELECT p.*, s.library, s.name AS source_name, s.sha256,
    s.active AS source_active FROM passages p JOIN sources s ON s.id = p.source_id"""


def search(project, library, query, limit=8, snapshot_id=None):
    if library not in LIBRARIES:
        raise ValueError("Choose content or institution explicitly.")
    tokens = list(dict.fromkeys(re.findall(r"\w{2,}", query.lower(), re.UNICODE)))[:40]
    if not tokens:
        return []
    match = " OR ".join('"' + term + '"' for term in tokens)
    with closing(connect(project)) as connection:
        filters = ["passage_search MATCH ?", "s.library = ?"]
        parameters = [match, library]
        if snapshot_id:
            ids = snapshot_sources(project, snapshot_id)
            if not ids:
                return []
            filters.append("s.id IN (" + ",".join("?" for _ in ids) + ")")
            parameters.extend(ids)
        else:
            filters.append("s.active = 1")
        parameters.append(max(1, min(limit, 30)))
        sql = PASSAGE_SELECT + " JOIN passage_search f ON f.passage_id = p.id WHERE " + " AND ".join(filters)
        rows = connection.execute(sql + " ORDER BY bm25(passage_search), p.id LIMIT ?", parameters)
        return [passage_data(row) for row in rows]


def read_passage(project, passage_id, neighbors=0):
    if not PASSAGE_KEY.fullmatch(passage_id):
        raise ValueError("Use a passage ID returned by search, without square brackets.")
    with closing(connect(project)) as connection:
        target = connection.execute("SELECT * FROM passages WHERE id = ?", (passage_id,)).fetchone()
        if not target:
            raise ValueError("Passage not found in this course folder.")
        count = max(0, min(neighbors, 3))
        rows = connection.execute(PASSAGE_SELECT + " WHERE p.source_id = ? AND p.ordinal BETWEEN ? AND ? ORDER BY p.ordinal",
                                  (target["source_id"], target["ordinal"] - count, target["ordinal"] + count))
        return [passage_data(row) for row in rows]


def list_passages(project, source_id, offset=0, limit=20):
    if not SOURCE_KEY.fullmatch(source_id):
        raise ValueError("Use a source ID returned by sources or ingest.")
    with closing(connect(project)) as connection:
        source = connection.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()
        if not source:
            raise ValueError("Source not found in this course folder.")
        count = max(1, min(limit, 30))
        start = max(0, offset)
        rows = list(connection.execute(PASSAGE_SELECT + " WHERE p.source_id = ? ORDER BY p.ordinal LIMIT ? OFFSET ?", (source_id, count, start)))
        return {"source": source_data(source), "passages": [passage_data(row) for row in rows],
                "next_offset": start + len(rows) if start + len(rows) < source["passage_count"] else None}


def check_citations(project, filenames, snapshot_id=None):
    """Check ID existence/scope only. Entailment and requirement authority require review."""
    scope = set(snapshot_sources(project, snapshot_id)) if snapshot_id else None
    results = []
    with closing(connect(project)) as connection:
        for filename in filenames:
            text = Path(filename).read_text(encoding="utf-8")
            citations = list(dict.fromkeys(re.findall(r"\[((?:content|institution):[^\]\n]+)\]", text)))
            invalid = []
            historical = []
            for pid in citations:
                row = connection.execute("SELECT p.source_id, s.active FROM passages p JOIN sources s ON s.id = p.source_id WHERE p.id = ?", (pid,)).fetchone()
                if not row or (scope is not None and row["source_id"] not in scope):
                    invalid.append(pid)
                elif not row["active"]:
                    historical.append(pid)
            results.append({"file": str(Path(filename).resolve()), "citation_count": len(citations), "invalid": invalid,
                            "historical": historical, "has_citations": bool(citations)})
    return {"valid": all(not row["invalid"] for row in results), "files": results,
            "limitation": "Checks citation IDs and optional snapshot scope only; does not establish factual support, complete citation coverage, or institutional compliance."}


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest="command", required=True)
    for name in ("init", "ingest", "sources", "search", "read", "passages", "snapshot", "check-citations"):
        command = commands.add_parser(name)
        command.add_argument("--project", required=True, help="Course folder; libraries are private to this folder")
        if name == "init":
            command.add_argument("--title", required=True)
        if name in ("ingest", "search", "sources"):
            command.add_argument("--library", choices=LIBRARIES, required=name != "sources")
        if name in ("ingest", "check-citations"):
            command.add_argument("files", nargs="+")
        if name == "sources":
            command.add_argument("--history", action="store_true")
        if name == "search":
            command.add_argument("--query", required=True)
        if name in ("search", "passages"):
            command.add_argument("--limit", type=int, default=8 if name == "search" else 20)
        if name in ("search", "check-citations"):
            command.add_argument("--snapshot")
        if name == "read":
            command.add_argument("passage_id")
            command.add_argument("--neighbors", type=int, default=0)
        if name == "passages":
            command.add_argument("--source", required=True)
            command.add_argument("--offset", type=int, default=0)
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.project, args.title)
        elif args.command == "ingest":
            result = {"imported": [], "errors": []}
            for filename in args.files:
                try:
                    result["imported"].append(ingest(args.project, args.library, filename))
                except (ValueError, OSError, sqlite3.Error) as error:
                    result["errors"].append({"file": filename, "error": str(error)})
        elif args.command == "sources":
            result = list_sources(args.project, args.library, args.history)
        elif args.command == "search":
            result = search(args.project, args.library, args.query, args.limit, args.snapshot)
        elif args.command == "read":
            result = read_passage(args.project, args.passage_id, args.neighbors)
        elif args.command == "passages":
            result = list_passages(args.project, args.source, args.offset, args.limit)
        elif args.command == "snapshot":
            result = snapshot(args.project)
        else:
            result = check_citations(args.project, args.files, args.snapshot)
        print(encode(result), end="")
        return 1 if isinstance(result, dict) and (result.get("errors") or result.get("valid") is False) else 0
    except (ValueError, OSError, sqlite3.Error) as error:
        print(encode({"error": str(error)}), file=sys.stderr, end="")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
