#!/usr/bin/env python3
"""Record Cadence milestones and serve a read-only local progress panel."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import sqlite3
import sys
import tempfile
from urllib.parse import urlsplit
from artifact_catalog import CATALOG_NAME, definition
import intake

PHASES = ("analysis", "design", "development", "implementation", "evaluation")
PHASE_STATES = ("pending", "working", "waiting", "blocked", "interrupted", "complete", "skipped")
RUN_STATES = ("working", "waiting", "blocked", "interrupted", "complete")
AGENT_STATES = ("queued", "working", "complete", "blocked", "interrupted")


def now():
    return datetime.now(timezone.utc).isoformat()


def root(project):
    return Path(project).expanduser().resolve()


def state_path(project):
    return root(project) / ".cadence" / "progress.json"


def read(project):
    path = state_path(project)
    if not path.is_file():
        raise ValueError("No progress record yet. Run progress.py init first.")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if state.get("version") != 1 or list(state["phases"]) != list(PHASES):
            raise ValueError("Unsupported progress record; preserve it before migrating.")
        for key in ("title", "mode", "status", "updated_at", "agents", "artifacts", "events", "revision"):
            if key not in state:
                raise ValueError("Incomplete progress record; do not overwrite it.")
        return state
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError) as error:
        raise ValueError("Cannot read the progress record; preserve it before repairing.") from error


def save(project, state):
    path = state_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".progress-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=2)
            file.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def record(state, message):
    state["updated_at"] = now()
    state["revision"] += 1
    state["events"] = (state["events"] + [{"at": state["updated_at"], "message": message}])[-30:]


def initialize(project, title, mode="review", demo=False, new_run=False):
    if state_path(project).exists():
        previous = read(project)
        if not new_run:
            return previous  # Starting the viewer must never reset a course.
        history = state_path(project).parent / "progress-history"
        history.mkdir(exist_ok=True)
        with (history / f"{secrets.token_hex(12)}.json").open("x", encoding="utf-8") as file:
            json.dump(previous, file, ensure_ascii=False, indent=2)
    if mode not in ("review", "build", "revise", "orient") or not title.strip():
        raise ValueError("Provide a title and review, build, revise, or orient mode.")
    state = {"version": 1, "revision": 0, "title": title, "mode": mode, "demo": demo,
             "status": "working", "note": "Getting oriented", "updated_at": now(),
             "phases": {phase: {"status": "pending", "note": ""} for phase in PHASES},
             "agents": {}, "artifacts": {}, "events": []}
    record(state, "Progress tracking started")
    save(project, state)
    return state


def artifact_path(project, value):
    path = (root(project) / value).resolve()
    if not path.is_relative_to(root(project)) or not path.is_file():
        raise ValueError("A deliverable must be an existing file inside the course folder.")
    return path.relative_to(root(project)).as_posix()


def attach_catalog(project, path=None):
    state = read(project)
    imported = root(project) / ".cadence" / "institutional-guidance" / CATALOG_NAME
    catalog = definition(path or (imported if imported.is_file() else None))
    if state.get("catalog"):
        if state["catalog"]["sha256"] != catalog["sha256"]:
            raise ValueError("The catalog changed. Review the changes and start a new progress run before replacing its checklist.")
        return state
    state["catalog"] = {key: catalog[key] for key in ("name", "sha256")}
    state["sections"] = {}
    for phase, details in catalog["phases"].items():
        state["sections"][phase] = {s["id"]: {**s, "status": "pending", "note": "", "files": []} for s in details["sections"]}
        if state["phases"][phase]["status"] == "complete":
            state["phases"][phase] = {"status": "pending", "note": "Catalog sections await verification"}
    if state["status"] == "complete":
        state["status"], state["note"] = "working", "Catalog sections await verification"
    record(state, "Artifact catalog attached; subsection completion requires saved evidence")
    save(project, state)
    return state


def check_sections(project, state, phase):
    sections = list(state.get("sections", {}).get(phase, {}).values())
    if any(s["status"] not in ("complete", "skipped") for s in sections):
        raise ValueError("Finish or explicitly skip each catalog subsection before completing the phase.")
    completed = [s for s in sections if s["status"] == "complete"]
    if sections and not completed:
        raise ValueError("Every subsection is skipped; mark the phase skipped rather than complete.")
    for section in completed:
        if not section["files"]:
            raise ValueError("Completed subsections require saved supporting documents.")
        for filename in section["files"]:
            safe = artifact_path(project, filename)
            if (root(project) / safe).stat().st_size == 0:
                raise ValueError("A completed subsection cannot point to an empty document.")
    if completed and phase in ("analysis", "design"):
        shared_files = set(completed[0]["files"]).intersection(*(set(s["files"]) for s in completed[1:]))
        if not shared_files:
            raise ValueError("Analysis and Design sections must share their consolidated phase report.")


def update(project, command, **fields):
    # The coordinator is the single writer; specialists report to it.
    state = read(project)
    note = fields.get("note", "").strip()
    if command == "phase":
        phase, status = fields["phase"], fields["status"]
        if phase not in PHASES or status not in PHASE_STATES:
            raise ValueError("Unknown ADDIE phase or phase status.")
        if status in ("waiting", "blocked", "skipped") and not note:
            raise ValueError("Explain a waiting, blocked, or skipped phase.")
        if status == "working" and any(v["status"] == "working" for k, v in state["phases"].items() if k != phase):
            raise ValueError("Finish or pause the current phase before starting another.")
        if status == "complete":
            check_sections(project, state, phase)
        state["phases"][phase] = {"status": status, "note": note}
        if status in ("working", "waiting", "blocked"):
            state["status"] = status
            state["note"] = note or f"Working through {phase}"
        elif state["status"] == "complete" and status == "pending":
            state["status"], state["note"] = "working", "Revisiting the workflow"
        message = f"{phase.capitalize()}: {status}" + (f" — {note}" if note else "")
    elif command == "section":
        phase, section_id, status = fields["phase"], fields["id"], fields["status"]
        sections = state.get("sections", {}).get(phase, {})
        if section_id not in sections:
            raise ValueError("Unknown subsection. Attach the catalog and use an ID from show.")
        if status not in PHASE_STATES:
            raise ValueError("Unknown subsection status.")
        if status in ("complete", "skipped", "waiting", "blocked") and not note:
            raise ValueError("Explain the completed work, skipped scope, or waiting dependency.")
        filenames = fields.get("files") or ([fields["path"]] if fields.get("path") else [])
        if status == "complete" and not filenames:
            raise ValueError("A checkmark requires saved supporting document paths.")
        safe_files = list(dict.fromkeys(artifact_path(project, name) for name in filenames))
        if status == "complete" and any((root(project) / name).stat().st_size == 0 for name in safe_files):
            raise ValueError("A checkmark cannot point to an empty document.")
        sections[section_id].update(status=status, note=note, files=safe_files)
        if status not in ("complete", "skipped") and state["phases"][phase]["status"] == "complete":
            state["phases"][phase] = {"status": "pending", "note": "Subsection reopened"}
            if state["status"] == "complete":
                state["status"], state["note"] = "working", "Subsection reopened"
        message = f"{sections[section_id]['title']}: {status}" + (f" — {note}" if note else "")
    elif command == "agent":
        status, execution = fields["status"], fields["execution"]
        if status not in AGENT_STATES or execution not in ("native", "sequential"):
            raise ValueError("Unknown specialist status or execution mode.")
        if not fields["id"].strip() or not fields["role"].strip():
            raise ValueError("Give the assignment an ID and role.")
        if state["status"] == "complete" and status != "complete":
            raise ValueError("Reopen the workflow before recording more specialist work.")
        state["agents"][fields["id"]] = {"role": fields["role"], "status": status,
                                          "execution": execution, "note": note}
        message = f"{fields['role']}: {status}" + (f" — {note}" if note else "")
    elif command == "artifact":
        path = artifact_path(project, fields["path"])
        if fields["status"] not in ("draft", "checked"):
            raise ValueError("A deliverable is draft or checked.")
        state["artifacts"][path] = {"label": fields.get("label") or Path(path).name,
                                     "status": fields["status"]}
        message = f"Deliverable {fields['status']}: {state['artifacts'][path]['label']}"
    elif command == "run":
        status = fields["status"]
        if status not in RUN_STATES:
            raise ValueError("Unknown workflow status.")
        if not note:
            raise ValueError("Describe what is happening or needed next.")
        if status == "complete":
            if any(p["status"] not in ("complete", "skipped") for p in state["phases"].values()):
                raise ValueError("Complete or explicitly skip each phase before finishing.")
            if any(a["status"] in ("queued", "working", "blocked") for a in state["agents"].values()):
                raise ValueError("Resolve outstanding specialist assignments before finishing.")
            for path in state["artifacts"]:
                artifact_path(project, path)
            for phase in PHASES:
                if state["phases"][phase]["status"] == "complete":
                    check_sections(project, state, phase)
        if status == "interrupted":
            for phase in state["phases"].values():
                if phase["status"] == "working":
                    phase["status"] = "interrupted"
            for agent in state["agents"].values():
                if agent["status"] in ("working", "queued"):
                    agent["status"] = "interrupted"
            for sections in state.get("sections", {}).values():
                for section in sections.values():
                    if section["status"] == "working":
                        section["status"] = "interrupted"
        state["status"], state["note"] = status, note
        message = f"Workflow {status} — {note}"
    elif command == "activity":
        if not note:
            raise ValueError("Provide a short milestone note.")
        state["note"] = note
        message = note
    else:
        raise ValueError("Unknown progress command.")
    record(state, message)
    save(project, state)
    return state


def view(project):
    state = read(project)
    try:
        profile = intake.read(project)
        state["intake"] = intake.summary(profile) if profile else None
    except (ValueError, OSError):
        state["intake"] = None
    for phase, sections in state.get("sections", {}).items():
        for section in sections.values():
            if section["status"] == "complete":
                try:
                    if not section["files"]:
                        raise ValueError("No supporting files")
                    for path in section["files"]:
                        safe = artifact_path(project, path)
                        if (root(project) / safe).stat().st_size == 0:
                            raise ValueError("Empty document")
                except (ValueError, OSError):
                    section["recorded_status"], section["status"] = "complete", "missing"
        if state["phases"][phase]["status"] == "complete" and any(s["status"] not in ("complete", "skipped") for s in sections.values()):
            state["phases"][phase] = {"status": "blocked", "note": "Subsection evidence needs attention"}
            if state["status"] == "complete":
                state["status"], state["note"] = "blocked", "A completed subsection's document is missing or empty"
    state["libraries"] = None
    database = root(project) / ".cadence" / "library.sqlite3"
    if database.is_file():
        connection = None
        try:
            connection = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True, timeout=1)
            rows = connection.execute("SELECT library, COUNT(*) FROM sources WHERE active=1 GROUP BY library").fetchall()
            state["libraries"] = {"content": 0, "institution": 0, **dict(rows)}
        except sqlite3.Error:
            pass  # Unavailable is different from an empty library.
        finally:
            if connection is not None:
                connection.close()
    for path, artifact in state["artifacts"].items():
        try:
            artifact_path(project, path)
            artifact["exists"] = True
        except ValueError:
            artifact["exists"] = False
    return state


def text_summary(state):
    markers = {"pending": "○", "working": "●", "complete": "✓", "waiting": "Ⅱ", "blocked": "!", "interrupted": "!", "skipped": "–"}
    phases = " → ".join(f"{markers[row['status']]} {name.capitalize()}" for name, row in state["phases"].items())
    lines = [phases, f"{state['status'].capitalize()}: {state['note']}"]
    for phase, sections in state.get("sections", {}).items():
        lines.append(phase.capitalize())
        lines.extend(f"  {markers.get(s['status'], '!')} {s['number']} {s['title']}" for s in sections.values())
    return "\n".join(lines)


def make_server(project, port=0):
    view(project)
    token = secrets.token_urlsafe(24)
    assets = Path(__file__).resolve().parent.parent / "assets" / "progress"
    routes = {"": ("index.html", "text/html; charset=utf-8"),
              "app.js": ("app.js", "text/javascript; charset=utf-8"),
              "style.css": ("style.css", "text/css; charset=utf-8"),
              "project-cadence-logo.png": ("project-cadence-logo.png", "image/png")}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            prefix = f"/{token}/"
            path = urlsplit(self.path).path
            expected_host = f"127.0.0.1:{self.server.server_port}"
            if self.headers.get("Host") != expected_host or not path.startswith(prefix):
                self.send_error(404)
                return
            route = path[len(prefix):]
            status = 200
            try:
                if route == "state":
                    data = json.dumps(view(project), ensure_ascii=False).encode()
                    content_type = "application/json; charset=utf-8"
                elif route in routes:
                    filename, content_type = routes[route]
                    data = (assets / filename).read_bytes()
                else:
                    self.send_error(404)
                    return
            except (ValueError, OSError):
                status, content_type = 503, "application/json"
                data = b'{"error":"Progress is temporarily unavailable. Saved milestones have not been changed."}'
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    return server, f"http://127.0.0.1:{server.server_port}/{token}/"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "catalog", "section", "phase", "agent", "artifact", "run", "activity", "show", "serve"))
    parser.add_argument("--project", required=True)
    parser.add_argument("--title")
    parser.add_argument("--mode", default="review", choices=("review", "build", "revise", "orient"))
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--new-run", action="store_true")
    parser.add_argument("--phase", choices=PHASES)
    parser.add_argument("--status")
    parser.add_argument("--note", default="")
    parser.add_argument("--id")
    parser.add_argument("--role")
    parser.add_argument("--execution", choices=("native", "sequential"), default="native")
    parser.add_argument("--path")
    parser.add_argument("--files", nargs="+")
    parser.add_argument("--catalog-file")
    parser.add_argument("--label")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args(argv)
    required = {"init": ("title",), "phase": ("phase", "status"), "section": ("phase", "id", "status"), "agent": ("id", "role", "status"),
                "artifact": ("path", "status"), "run": ("status",)}
    for field in required.get(args.command, ()):
        if not getattr(args, field):
            parser.error(f"{args.command} requires --{field}")
    try:
        if args.command == "serve":
            server, url = make_server(args.project, args.port)
            print(json.dumps({"url": url, "scope": "Local read-only viewer; keep this process running."}), flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
            return 0
        if args.command == "init":
            initialize(args.project, args.title, args.mode, args.demo, args.new_run)
        elif args.command == "catalog":
            attach_catalog(args.project, args.catalog_file)
        elif args.command != "show":
            fields = vars(args).copy()
            fields.pop("command")
            fields.pop("project")
            update(args.project, args.command, **fields)
        state = view(args.project)
        print(text_summary(state) if args.format == "text" else json.dumps(state, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
