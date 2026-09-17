"""Synthetic progress records and loopback-only viewer tests; no provider calls."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "cadence" / "scripts"))
import cadence
import progress


class ProgressTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.project = Path(temporary.name) / "course"
        progress.initialize(self.project, "Synthetic workshop", demo=True)

    def test_resume_preserves_state_and_new_run_archives_it(self):
        progress.update(self.project, "phase", phase="analysis", status="working", note="Checking learners")
        before = progress.read(self.project)
        self.assertEqual(progress.initialize(self.project, "Another title"), before)
        fresh = progress.initialize(self.project, "Second review", new_run=True)
        self.assertEqual(fresh["phases"]["analysis"]["status"], "pending")
        archive = list((self.project / ".cadence" / "progress-history").glob("*.json"))
        self.assertEqual(len(archive), 1)
        self.assertEqual(json.loads(archive[0].read_text()), before)

    def test_only_one_phase_can_be_working(self):
        progress.update(self.project, "phase", phase="analysis", status="working")
        before = progress.read(self.project)
        with self.assertRaisesRegex(ValueError, "current phase"):
            progress.update(self.project, "phase", phase="design", status="working")
        self.assertEqual(progress.read(self.project), before)
        progress.update(self.project, "phase", phase="analysis", status="complete")
        state = progress.update(self.project, "phase", phase="design", status="working")
        self.assertEqual(state["status"], "working")

    def test_waiting_and_skips_require_explanation(self):
        for status in ("waiting", "blocked", "skipped"):
            with self.assertRaises(ValueError):
                progress.update(self.project, "phase", phase="analysis", status=status)
        state = progress.update(self.project, "phase", phase="analysis", status="waiting", note="Learner decision needed")
        self.assertEqual(state["status"], "waiting")
        self.assertEqual(state["note"], "Learner decision needed")

    def test_completion_does_not_hide_outstanding_work(self):
        with self.assertRaisesRegex(ValueError, "each phase"):
            progress.update(self.project, "run", status="complete", note="Ready")
        for phase in progress.PHASES:
            progress.update(self.project, "phase", phase=phase, status="complete")
        progress.update(self.project, "agent", id="quality", role="Quality reviewer", execution="native", status="working")
        with self.assertRaisesRegex(ValueError, "specialist"):
            progress.update(self.project, "run", status="complete", note="Ready")
        progress.update(self.project, "agent", id="quality", role="Quality reviewer", execution="native", status="complete")
        state = progress.update(self.project, "run", status="complete", note="Ready")
        self.assertEqual(state["status"], "complete")
        with self.assertRaisesRegex(ValueError, "Reopen"):
            progress.update(self.project, "agent", id="new", role="New check", execution="native", status="working")

    def test_interruption_preserves_work_and_marks_active_assignments(self):
        progress.update(self.project, "phase", phase="analysis", status="complete")
        progress.update(self.project, "phase", phase="design", status="working")
        progress.update(self.project, "agent", id="design", role="Designer", execution="sequential", status="working")
        state = progress.update(self.project, "run", status="interrupted", note="Stopped by user")
        self.assertEqual(state["phases"]["analysis"]["status"], "complete")
        self.assertEqual(state["phases"]["design"]["status"], "interrupted")
        self.assertEqual(state["agents"]["design"]["status"], "interrupted")
        self.assertEqual(state["agents"]["design"]["execution"], "sequential")

    def test_artifacts_must_exist_and_stay_in_project(self):
        outside = self.project.parent / "outside.md"
        outside.write_text("Synthetic document")
        for path in ("absent.md", "../outside.md", str(outside)):
            with self.assertRaisesRegex(ValueError, "existing file inside"):
                progress.update(self.project, "artifact", path=path, status="draft")
        (self.project / "link.md").symlink_to(outside)
        with self.assertRaises(ValueError):
            progress.update(self.project, "artifact", path="link.md", status="checked")
        deliverable = self.project / "review.md"
        deliverable.write_text("Synthetic review")
        progress.update(self.project, "artifact", path="review.md", status="draft")
        self.assertTrue(progress.view(self.project)["artifacts"]["review.md"]["exists"])
        deliverable.unlink()
        self.assertFalse(progress.view(self.project)["artifacts"]["review.md"]["exists"])

    def test_unavailable_library_is_not_zero_and_counts_are_actual_sources(self):
        self.assertIsNone(progress.view(self.project)["libraries"])
        cadence.initialize(self.project, "Synthetic workshop")
        source = self.project / "source.md"
        source.write_text("A concise presentation needs a purpose.")
        cadence.ingest(self.project, "content", source)
        self.assertEqual(progress.view(self.project)["libraries"], {"content": 1, "institution": 0})

    def test_history_is_bounded_and_state_reads_do_not_write(self):
        for number in range(40):
            progress.update(self.project, "activity", note=f"Milestone {number}")
        before = progress.state_path(self.project).read_bytes()
        state = progress.view(self.project)
        self.assertEqual(len(state["events"]), 30)
        self.assertEqual(state["events"][-1]["message"], "Milestone 39")
        self.assertEqual(progress.state_path(self.project).read_bytes(), before)

    def test_corrupt_progress_is_not_overwritten(self):
        path = progress.state_path(self.project)
        path.write_text("{broken")
        with self.assertRaises(ValueError):
            progress.initialize(self.project, "Replacement")
        self.assertEqual(path.read_text(), "{broken")

    def test_cli_returns_markers_and_actionable_errors(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = progress.main(["show", "--project", str(self.project), "--format", "text"])
        self.assertEqual(result, 0)
        self.assertIn("○ Analysis", output.getvalue())
        with contextlib.redirect_stderr(output):
            result = progress.main(["phase", "--project", str(self.project), "--phase", "analysis", "--status", "invented"])
        self.assertEqual(result, 1)

    def test_viewer_serves_live_state_but_not_other_files_or_writes(self):
        server, url = progress.make_server(self.project)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 2)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(url) as response:
            self.assertIn(b"Through ADDIE", response.read())
            self.assertEqual(response.headers["Cache-Control"], "no-store")
            self.assertIn("img-src 'self'", response.headers["Content-Security-Policy"])
        with opener.open(url + "project-cadence-logo.png") as response:
            self.assertEqual(response.headers["Content-Type"], "image/png")
            self.assertTrue(response.read().startswith(b"\x89PNG\r\n\x1a\n"))
        progress.update(self.project, "activity", note="A newer milestone")
        with opener.open(url + "state") as response:
            self.assertEqual(json.load(response)["note"], "A newer milestone")
        for target in (url + "../progress.json", url.split(urlsplit_token(url))[0], url + ".cadence/progress.json"):
            with self.assertRaises(urllib.error.HTTPError) as caught:
                opener.open(target)
            self.assertEqual(caught.exception.code, 404)
        request = urllib.request.Request(url + "state", headers={"Host": "attacker.example"})
        with self.assertRaises(urllib.error.HTTPError) as caught:
            opener.open(request)
        self.assertEqual(caught.exception.code, 404)
        request = urllib.request.Request(url + "state", data=b"{}", method="POST")
        with self.assertRaises(urllib.error.HTTPError) as caught:
            opener.open(request)
        self.assertEqual(caught.exception.code, 501)


def urlsplit_token(url):
    return url.split("/")[-2]


if __name__ == "__main__":
    unittest.main()
