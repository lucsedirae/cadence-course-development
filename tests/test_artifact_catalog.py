"""Catalog integration checks use only the synthetic fixture, never user documents."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "cadence" / "scripts"))
import artifact_catalog
import cadence
import progress
import intake

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "artifact-catalog.md"


class CatalogTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.project = self.root / "course"
        self.sources = self.root / "bundle"
        self.sources.mkdir()
        self.catalog = self.sources / artifact_catalog.CATALOG_NAME
        shutil.copy2(FIXTURE, self.catalog)
        progress.initialize(self.project, "Synthetic catalog course")

    def attach(self):
        return progress.attach_catalog(self.project, self.catalog)

    def complete_analysis(self, file="analysis.md"):
        (self.project / file).write_text("Synthetic substantive analysis for tests.")
        for identifier in self.attach()["sections"]["analysis"]:
            progress.update(self.project, "section", phase="analysis", id=identifier,
                            status="complete", files=[file], note="Synthetic content checked")

    def test_numbered_sections_and_parts_are_derived_without_later_examples(self):
        result = artifact_catalog.definition(self.catalog)
        self.assertEqual([s["id"] for s in result["phases"]["analysis"]["sections"]],
                         ["analysis.1.1", "analysis.1.2", "analysis.1.3.a", "analysis.1.3.b"])
        self.assertEqual(result["phases"]["design"]["document"], "Synthetic Design Document")
        self.assertEqual(len(result["phases"]["development"]["sections"]), 2)
        self.assertEqual(result["phases"]["development"]["sections"][1]["group"], "2. Assessment Instruments")

    def test_missing_phases_and_unparented_parts_fail_cleanly(self):
        self.catalog.write_text("## ANALYSIS PHASE: Test\n**Part B: Missing parent**\n")
        with self.assertRaises(ValueError):
            artifact_catalog.definition(self.catalog)
        self.catalog.write_text("# No phase definitions")
        with self.assertRaises(ValueError):
            artifact_catalog.definition(self.catalog)

    def test_cli_initialization_indexes_only_institution_and_preserves_resume(self):
        intake.save(self.project, {"title": "Synthetic", "intent": "build", "delivery": "unsure", "learners": "unsure", "duration": "unsure", "role": "builder", "source_material": "unsure"})
        with patch.object(cadence, "INSTITUTION_DIR", self.sources), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cadence.main(["init", "--project", str(self.project), "--title", "Synthetic"]), 0)
            original = cadence.list_sources(self.project)[0]
            snapshot = cadence.snapshot(self.project)["snapshot"]
            self.catalog.write_text(self.catalog.read_text() + "\nSynthetic changed institutional requirement.\n")
            self.assertEqual(cadence.main(["init", "--project", str(self.project), "--title", "Resume"]), 0)
            self.assertEqual(cadence.list_sources(self.project)[0]["id"], original["id"])
            self.assertEqual(cadence.main(["seed-institution", "--project", str(self.project)]), 0)
        current = cadence.list_sources(self.project)[0]
        self.assertNotEqual(current["id"], original["id"])
        self.assertEqual(current["library"], "institution")
        self.assertEqual(cadence.list_sources(self.project, "content"), [])
        self.assertTrue(cadence.search(self.project, "institution", "synthetic", snapshot_id=snapshot))
        self.assertIn("institutional-guidance", current["original_path"])

    def test_plugin_location_changes_do_not_duplicate_unchanged_guidance(self):
        cadence.initialize(self.project, "Synthetic")
        first = cadence.seed_institution(self.project, self.sources)["imported"][0]
        another = self.root / "new-plugin-version"
        shutil.copytree(self.sources, another)
        second = cadence.seed_institution(self.project, another)["imported"][0]
        self.assertEqual(first["id"], second["id"])
        self.assertTrue(second["reused"])

    def test_attach_preserves_marks_but_does_not_infer_old_completions(self):
        progress.update(self.project, "phase", phase="analysis", status="complete")
        state = self.attach()
        self.assertEqual(state["phases"]["analysis"]["status"], "pending")
        self.complete_analysis()
        before = progress.read(self.project)
        self.assertEqual(self.attach(), before)
        self.catalog.write_text(self.catalog.read_text() + "\nChanged guidance\n")
        with self.assertRaisesRegex(ValueError, "catalog changed"):
            self.attach()
        self.assertEqual(progress.read(self.project), before)

    def test_checkmarks_require_existing_nonempty_documents_and_notes(self):
        self.attach()
        args = dict(phase="analysis", id="analysis.1.1", status="complete", note="Checked")
        for files in ([], ["missing.md"]):
            with self.assertRaises(ValueError):
                progress.update(self.project, "section", files=files, **args)
        (self.project / "empty.md").touch()
        with self.assertRaisesRegex(ValueError, "empty"):
            progress.update(self.project, "section", files=["empty.md"], **args)
        with self.assertRaises(ValueError):
            progress.update(self.project, "section", phase="analysis", id="analysis.1.1", status="skipped")
        state = progress.update(self.project, "section", phase="analysis", id="analysis.1.1", status="skipped", note="Outside the explicit review scope")
        self.assertEqual(state["sections"]["analysis"]["analysis.1.1"]["status"], "skipped")

    def test_phase_completion_requires_sections_and_consolidated_report(self):
        self.attach()
        with self.assertRaisesRegex(ValueError, "each catalog subsection"):
            progress.update(self.project, "phase", phase="analysis", status="complete")
        self.complete_analysis()
        (self.project / "separate.md").write_text("Separate synthetic fragment")
        progress.update(self.project, "section", phase="analysis", id="analysis.1.1", status="complete", path="separate.md", note="Checked")
        with self.assertRaisesRegex(ValueError, "consolidated"):
            progress.update(self.project, "phase", phase="analysis", status="complete")
        self.complete_analysis()
        self.assertEqual(progress.update(self.project, "phase", phase="analysis", status="complete")["phases"]["analysis"]["status"], "complete")

    def test_lost_evidence_removes_checkmark_without_rewriting_record(self):
        self.complete_analysis()
        progress.update(self.project, "phase", phase="analysis", status="complete")
        before = progress.state_path(self.project).read_bytes()
        (self.project / "analysis.md").unlink()
        state = progress.view(self.project)
        self.assertEqual(state["sections"]["analysis"]["analysis.1.1"]["status"], "missing")
        self.assertEqual(state["phases"]["analysis"]["status"], "blocked")
        self.assertEqual(progress.state_path(self.project).read_bytes(), before)

    def test_reopened_subsection_reopens_phase_and_interruption_marks_work(self):
        self.complete_analysis()
        progress.update(self.project, "phase", phase="analysis", status="complete")
        progress.update(self.project, "section", phase="analysis", id="analysis.1.1", status="working")
        self.assertEqual(progress.read(self.project)["phases"]["analysis"]["status"], "pending")
        state = progress.update(self.project, "run", status="interrupted", note="Stopped")
        self.assertEqual(state["sections"]["analysis"]["analysis.1.1"]["status"], "interrupted")


if __name__ == "__main__":
    unittest.main()
