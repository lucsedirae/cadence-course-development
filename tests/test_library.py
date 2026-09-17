import contextlib
import io
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "cadence" / "scripts"))
import cadence


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "course"
        cadence.initialize(self.project, "Briefing course")

    def source(self, name, text, library="content"):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return cadence.ingest(self.project, library, path)

    def test_libraries_are_separate_even_for_same_file_and_query(self):
        content = self.source("source.md", "Every briefing includes a clear purpose.")
        institution = cadence.ingest(self.project, "institution", self.root / "source.md")
        self.assertNotEqual(content["id"], institution["id"])
        self.assertEqual([p["source_id"] for p in cadence.search(self.project, "content", "briefing")], [content["id"]])
        self.assertEqual([p["source_id"] for p in cadence.search(self.project, "institution", "briefing")], [institution["id"]])

    def test_unchanged_import_is_idempotent_and_preserves_original(self):
        first = self.source("source.md", "A briefing makes a decision clear.")
        again = cadence.ingest(self.project, "content", self.root / "source.md")
        self.assertTrue(again["reused"])
        self.assertEqual(first["id"], again["id"])
        self.assertEqual(len(cadence.list_sources(self.project)), 1)
        original = self.project / ".cadence" / "originals" / first["stored_file"]
        self.assertEqual(original.read_text(), "A briefing makes a decision clear.")

    def test_replacement_excludes_old_version_but_keeps_pinned_evidence(self):
        old = self.source("process.md", "The pilot course takes forty minutes.", "institution")
        old_passage = cadence.search(self.project, "institution", "forty")[0]
        pinned = cadence.snapshot(self.project)["snapshot"]
        new = self.source("process.md", "The pilot course takes sixty minutes.", "institution")
        self.assertNotEqual(old["id"], new["id"])
        self.assertEqual(cadence.search(self.project, "institution", "forty"), [])
        self.assertEqual(cadence.search(self.project, "institution", "forty", snapshot_id=pinned)[0]["id"], old_passage["id"])
        self.assertFalse(cadence.read_passage(self.project, old_passage["id"])[0]["source_active"])
        self.assertEqual(len(cadence.list_sources(self.project, include_history=True)), 2)

    def test_failed_replacement_does_not_retire_readable_version(self):
        first = self.source("course.md", "Original readable briefing content.")
        with self.assertRaises(ValueError):
            self.source("course.md", "")
        self.assertEqual(cadence.list_sources(self.project)[0]["id"], first["id"])
        self.assertEqual(len(cadence.list_sources(self.project, include_history=True)), 1)

    def test_reimporting_an_older_file_reactivates_that_version(self):
        first = self.source("course.md", "Original briefing content.")
        self.source("course.md", "Revised presentation content.")
        reverted = self.source("course.md", "Original briefing content.")
        self.assertEqual(reverted["id"], first["id"])
        self.assertEqual(cadence.list_sources(self.project)[0]["id"], first["id"])
        self.assertEqual(cadence.search(self.project, "content", "presentation"), [])

    def test_snapshot_is_deterministic_and_detects_tampering(self):
        self.source("course.md", "A useful source.")
        first = cadence.snapshot(self.project)
        self.assertEqual(first["snapshot"], cadence.snapshot(self.project)["snapshot"])
        Path(first["manifest_path"]).write_text('{"sources": []}')
        with self.assertRaisesRegex(ValueError, "changed"):
            cadence.snapshot_sources(self.project, first["snapshot"])

    def test_no_cross_project_or_empty_snapshot_search(self):
        empty = cadence.snapshot(self.project)["snapshot"]
        self.source("course.md", "Useful briefing instruction.")
        self.assertEqual(cadence.search(self.project, "content", "briefing", snapshot_id=empty), [])
        other = self.root / "another-course"
        cadence.initialize(other, "Other")
        with self.assertRaisesRegex(ValueError, "not found"):
            cadence.read_passage(other, cadence.search(self.project, "content", "briefing")[0]["id"])

    def test_chunk_offsets_overlap_and_cover_all_characters(self):
        text = "Briefing detail " * 800
        parts = list(cadence.chunks(text))
        covered = set()
        for start, end, part in parts:
            self.assertEqual(part, text[start:end])
            self.assertLessEqual(len(part), cadence.CHUNK_SIZE)
            covered.update(range(start, end))
        self.assertEqual(len(covered), len(text))
        self.assertGreater(parts[0][1], parts[1][0])

    def test_passage_pagination_and_neighbors_remain_in_source(self):
        first = self.source("long.txt", "Briefing example. " * 1700)
        self.source("other.txt", "Unrelated briefing.")
        page = cadence.list_passages(self.project, first["id"], limit=2)
        self.assertEqual(page["next_offset"], 2)
        second = cadence.list_passages(self.project, first["id"], offset=2, limit=2)
        self.assertFalse(set(p["id"] for p in page["passages"]) & set(p["id"] for p in second["passages"]))
        around = cadence.read_passage(self.project, second["passages"][0]["id"], neighbors=1)
        self.assertEqual([p["ordinal"] for p in around], [2, 3, 4])
        self.assertTrue(all(p["source_id"] == first["id"] for p in around))

    def test_query_punctuation_cannot_escape_library_or_break_fts(self):
        self.source("course.md", "Useful briefing content.")
        self.source("rules.md", "Secret institutional requirements.", "institution")
        results = cadence.search(self.project, "content", 'briefing OR " ) ; DROP TABLE sources --')
        self.assertTrue(results)
        self.assertTrue(all(p["library"] == "content" for p in results))
        self.assertEqual(len(cadence.list_sources(self.project)), 2)

    def test_citation_validation_checks_unknown_and_snapshot_scope(self):
        self.source("course.md", "Briefing content.")
        pinned = cadence.snapshot(self.project)["snapshot"]
        self.source("rules.md", "Briefing institutional requirements.", "institution")
        content = cadence.search(self.project, "content", "briefing")[0]
        institution = cadence.search(self.project, "institution", "briefing")[0]
        draft = self.root / "draft.md"
        draft.write_text("A supported statement " + content["citation"])
        self.assertTrue(cadence.check_citations(self.project, [draft], pinned)["valid"])
        draft.write_text(institution["citation"])
        self.assertFalse(cadence.check_citations(self.project, [draft], pinned)["valid"])
        draft.write_text("[content:invented:000001]")
        self.assertFalse(cadence.check_citations(self.project, [draft])["valid"])

    def test_no_citations_is_reported_not_claimed_as_supported(self):
        draft = self.root / "draft.md"
        draft.write_text("An uncited proposal.")
        result = cadence.check_citations(self.project, [draft])
        self.assertFalse(result["files"][0]["has_citations"])
        self.assertIn("does not establish factual support", result["limitation"])

    def test_init_preserves_existing_project_and_reads_can_fail_cleanly(self):
        initialized = cadence.initialize(self.project, "Changed title")
        self.assertTrue(initialized["existing"])
        self.assertEqual(initialized["title"], "Briefing course")
        with self.assertRaises(ValueError):
            cadence.read_passage(self.project, "../../anything")
        with self.assertRaises(ValueError):
            cadence.snapshot_sources(self.project, "../../anything")
        with self.assertRaises(ValueError):
            cadence.search(self.project, "both", "anything")

    def test_partial_batch_import_reports_errors_and_nonzero_exit(self):
        good = self.root / "good.md"
        good.write_text("Readable briefing source.")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = cadence.main(["ingest", "--project", str(self.project), "--library", "content", str(good), str(self.root / "missing.md")])
        result = json.loads(output.getvalue())
        self.assertEqual(status, 1)
        self.assertEqual(len(result["imported"]), 1)
        self.assertEqual(len(result["errors"]), 1)

    def test_nuls_removed_and_invalid_schema_rejected(self):
        self.source("course.txt", "Briefing\x00 content.")
        passage = cadence.search(self.project, "content", "briefing")[0]
        self.assertNotIn("\x00", passage["text"])
        with sqlite3.connect(self.project / ".cadence" / "library.sqlite3") as connection:
            connection.execute("PRAGMA user_version=99")
        with self.assertRaisesRegex(ValueError, "schema"):
            cadence.list_sources(self.project)


if __name__ == "__main__":
    unittest.main()
