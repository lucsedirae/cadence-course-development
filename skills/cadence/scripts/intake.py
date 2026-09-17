#!/usr/bin/env python3
"""Collect a new course's intake locally, before initializing its libraries."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import tempfile
import threading
import time
from urllib.parse import urlsplit

QUESTIONS = [
    {"id": "title", "question": "What should we call the project?", "type": "text"},
    {"id": "intent", "question": "Are we building?", "options": [
        ["build", "Brand new course"], ["review", "Review existing course"], ["unsure", "Not sure yet"]]},
    {"id": "delivery", "question": "How will learners take this course?", "options": [
        ["classroom", "In a classroom (instructor-led)"], ["self_paced", "On a computer (self-paced)"],
        ["blended", "Mix of both (blended)"], ["unsure", "Not sure yet"]]},
    {"id": "learners", "question": "Who are the learners mostly?", "options": [
        ["junior_enlisted", "Junior enlisted"], ["ncos", "NCOs"], ["staff_ncos", "Staff NCOs"],
        ["officers", "Officers"], ["dow_civilians", "DoW civilians"],
        ["mixed_civilian_military", "A mix (civilians/military)"], ["mixed_military", "A mix (military)"],
        ["unsure", "Not sure yet"]]},
    {"id": "duration", "question": "How long should the course run?", "options": [
        ["few_hours", "A few hours"], ["about_a_day", "About a day"], ["several_days", "Several days"],
        ["weeks_or_more", "Weeks or more"], ["unsure", "Not sure yet"]]},
    {"id": "role", "question": "What is your role?", "options": [
        ["builder", "I'm building it"], ["instructor", "I teach it"], ["approver", "I oversee/approve it"]]},
    {"id": "source_material", "question": "Do you have source material to work from?",
     "hint": "For example: doctrine, manuals, or previous course content.", "options": [
        ["yes", "Yes"], ["no", "No"], ["unsure", "Not sure yet"]]},
]


def record_path(project):
    return Path(project).expanduser().resolve() / ".cadence" / "intake.json"


def validate(answers, version=2):
    questions = QUESTIONS[:4] if version == 1 else QUESTIONS
    if not isinstance(answers, dict) or set(answers) != {q["id"] for q in questions}:
        raise ValueError(f"Answer all {len(questions)} intake questions.")
    result = {}
    for question in questions:
        value = answers[question["id"]]
        if not isinstance(value, str):
            raise ValueError("Choose an answer for each question.")
        if question["id"] == "title":
            value = value.strip()
            if not value or len(value) > 160 or any(ord(c) < 32 or ord(c) == 127 for c in value):
                raise ValueError("Use a project name of 1–160 characters on one line.")
        elif value not in dict(question["options"]):
            raise ValueError("Choose one of the listed options for " + question["question"])
        result[question["id"]] = value
    return result


def read(project):
    path = record_path(project)
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        if record["version"] not in (1, 2) or record["status"] != "complete":
            raise ValueError("Unsupported intake record; preserve it before repairing.")
        record["answers"] = validate(record["answers"], version=record["version"])
        return record
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise ValueError("Cannot read the saved intake; preserve it before repairing.") from error


def summary(record):
    answers = record["answers"]
    return [{"question": q["question"], "answer": "Not asked in earlier intake" if q["id"] not in answers else answers[q["id"]] if q["id"] == "title"
             else dict(q["options"])[answers[q["id"]]]} for q in QUESTIONS]


def save(project, answers):
    answers = validate(answers)
    prior = read(project)
    if prior:
        if prior["answers"] != answers:
            raise ValueError("Intake is already saved. Continue the existing project; record changes with Cadence in chat.")
        return prior
    path = record_path(project)
    if (path.parent / "library.sqlite3").exists():
        raise ValueError("This project already exists. Resume it without a new-project questionnaire.")
    record = {"version": 2, "status": "complete", "answers": answers,
              "saved_at": datetime.now(timezone.utc).isoformat()}
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".intake-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(record, output, ensure_ascii=False, indent=2)
            output.write("\n")
        # Publish a fully written record without replacing another submission.
        try:
            os.link(temporary, path)
        except FileExistsError:
            return save(project, answers)
    finally:
        os.unlink(temporary)
    return record


def view(project, demo=False):
    record = read(project)
    existing = (record_path(project).parent / "library.sqlite3").exists()
    return {"status": "complete" if record else "existing" if existing else "pending",
            "questions": QUESTIONS, "answers": record["answers"] if record else None, "demo": demo}


def make_server(project, port=0, demo=False):
    view(project, demo)
    token = secrets.token_urlsafe(24)
    assets = Path(__file__).resolve().parent.parent / "assets"
    routes = {"": ("intake/index.html", "text/html; charset=utf-8"),
              "app.js": ("intake/app.js", "text/javascript; charset=utf-8"),
              "style.css": ("progress/style.css", "text/css; charset=utf-8"),
              "intake.css": ("intake/style.css", "text/css; charset=utf-8")}
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def route(self):
            prefix = f"/{token}/"
            path = urlsplit(self.path).path
            host = f"127.0.0.1:{self.server.server_port}"
            if self.headers.get("Host") != host or not path.startswith(prefix):
                return None
            return path[len(prefix):]

        def respond(self, code, data, content_type="application/json; charset=utf-8"):
            if not isinstance(data, bytes):
                data = json.dumps(data, ensure_ascii=False).encode()
            self.send_response(code)
            for name, value in {"Content-Type": content_type, "Content-Length": str(len(data)),
                                "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff",
                                "Referrer-Policy": "no-referrer",
                                "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"}.items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            route = self.route()
            try:
                if route == "state":
                    self.respond(200, view(project, demo))
                elif route in routes:
                    path, content_type = routes[route]
                    self.respond(200, (assets / path).read_bytes(), content_type)
                else:
                    self.respond(404, {"error": "Not found"})
            except (OSError, ValueError):
                self.respond(503, {"error": "The saved intake could not be read. Return to chat for help."})

        def do_POST(self):
            if self.route() != "answers":
                self.respond(404, {"error": "Not found"})
                return
            origin = f"http://127.0.0.1:{self.server.server_port}"
            if self.headers.get("Origin") != origin or self.headers.get("Content-Type") != "application/json":
                self.respond(403, {"error": "Submit from the local Cadence intake form."})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 8192:
                    raise ValueError("The intake submission is too large or empty.")
                answers = json.loads(self.rfile.read(size))
                with lock:
                    save(project, answers)
                self.respond(200, view(project, demo))
            except (ValueError, UnicodeDecodeError) as error:
                self.respond(400, {"error": str(error)})
            except OSError:
                self.respond(500, {"error": "Could not save the answers. Your entries are still here; retry or return to chat."})

        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    return server, f"http://127.0.0.1:{server.server_port}/{token}/"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("serve", "show", "save", "wait"))
    parser.add_argument("--project", required=True)
    parser.add_argument("--title")
    for q in QUESTIONS[1:]:
        parser.add_argument("--" + q["id"].replace("_", "-"), choices=list(dict(q["options"])))
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=45, choices=range(1, 61), metavar="1–60")
    args = parser.parse_args(argv)
    try:
        if args.command == "serve":
            server, url = make_server(args.project, args.port, args.demo)
            print(json.dumps({"url": url, "scope": "Local intake only; no course work starts on submission."}), flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
            return 0
        if args.command == "save":
            save(args.project, {q["id"]: getattr(args, q["id"]) for q in QUESTIONS})
        if args.command == "wait":
            end = time.monotonic() + args.timeout
            while view(args.project)["status"] == "pending" and time.monotonic() < end:
                time.sleep(0.5)
        print(json.dumps(view(args.project, args.demo), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as error:
        print(json.dumps({"error": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
