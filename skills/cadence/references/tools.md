# Course libraries

Run the bundled `scripts/cadence.py` using its absolute path relative to this skill. All operations use an explicit **course project folder**. Keep that folder outside the installed plugin so plugin updates cannot remove curriculum or libraries. Commands return JSON; a failed or partially failed import exits nonzero and lists the failures. Read the JSON before continuing.

Use Python 3.10+ with SQLite FTS5. Plain text and Markdown need no additional packages. For PDF, DOCX and PPTX use a Python environment with the packages in the plugin's `requirements.txt`. Prefer a suitable existing document runtime; otherwise create a virtual environment and install those requirements using normal host permissions. Use the same interpreter for subsequent commands. No separate API key or embedding service is used by these helpers.

In the examples, `TOOL` means the absolute path to this skill's `scripts/cadence.py`, and `COURSE` means the absolute course folder. Substitute real paths; quote paths with spaces.

For a new project, complete [intake.md](intake.md) before `init`. The CLI uses the saved project name; `--title` is optional and, when supplied for a new project, must match intake. Existing courses resume without repeating the questionnaire.

## Initialize and import

```text
python3 TOOL init --project COURSE
python3 TOOL ingest --project COURSE --library content /path/to/course.docx /path/to/readings.pdf
python3 TOOL ingest --project COURSE --library institution /path/to/process.pdf /path/to/lesson-template.docx
python3 TOOL sources --project COURSE
python3 TOOL snapshot --project COURSE
```

New courses initialized with the CLI automatically index the user-selected catalog from `assets/institution/` into the `institution` library. To adopt or update that guidance in an existing course, explicitly run `python3 TOOL seed-institution --project COURSE`, then create a new source snapshot. Reinitializing an existing course does not silently update its evidence. The stable source copy is under `COURSE/.cadence/institutional-guidance/`; retained versions and citations use the normal library rules.

Explicitly classify files before ingestion. `content` is material to review or teach from. `institution` is the institution's instructional process, requirements, guidance or templates. A document's membership does not prove that every statement is mandatory, current or authoritative; interpret wording, applicability and source authority. Do not silently classify an ambiguous document or copy a subject reference into the institution library to support a policy claim.

Imports support `.txt`, `.md`, `.markdown`, `.docx`, `.pdf`, and `.pptx`. Pass files individually. A folder can be inventoried first, then its selected files passed to ingestion. The initial plugin does not import Moodle/SCORM packages. Original files are retained with SHA-256 hashes. Reimporting the same file and contents reuses its evidence; a changed file creates a new version. Current retrieval excludes superseded versions. Renamed files are separate sources; inspect for duplicates or conflicting versions.

Mixed PDFs retain readable pages, preserve page numbers, and report skipped pages. Fully scanned PDFs cannot be indexed. PPTX extraction includes text, tables and speaker notes with slide locations. Charts, images, visual layout and OCR are outside this tool's scope. Warnings are evidence limitations, never proof those portions contain no relevant material.

## Pin the sources

`snapshot` saves a source manifest under `COURSE/.cadence/source_sets/` and returns its identifier. Pass that identifier to every specialist and each retrieval during a run. A snapshot identifies the evidence versions used; it does not assert that they were read or verified. After adding sources, explicitly create a new snapshot and refresh dependent findings.

```text
python3 TOOL search --project COURSE --library institution --snapshot SNAPSHOT --query "lesson structure approval objectives"
python3 TOOL search --project COURSE --library content --snapshot SNAPSHOT --query "briefing audience purpose"
python3 TOOL read --project COURSE PASSAGE_ID --neighbors 1
python3 TOOL passages --project COURSE --source SOURCE_ID --offset 0 --limit 20
```

Search is local SQLite FTS5 with BM25 keyword ranking, not semantic embeddings. Search each library separately with topic terms and alternate wording. A zero-result search means the query did not match. Use the source inventory and paginated `passages` to inspect structure or entire in-scope sections before claiming information is absent. `next_offset` is null at the end. Search returns at most 30 passages, and surrounding reads at most three neighbors on either side.

Every returned passage includes source name, library, SHA-256, location, ID, text, and a ready-made `citation`, for example `[institution:0123456789abcdef01234567:000001]`. Copy actual returned citation strings; never fabricate IDs. Reads may retrieve historical evidence, marked `source_active: false`; ensure it belongs to the pinned source set. Locators include PDF page or PPTX slide numbers where applicable. Chunks preserve offsets within their extraction unit and overlap to retain context.

## Curriculum and evidence files

Write curriculum into `COURSE/deliverables/`. Assign each subagent a unique output under `COURSE/working/roles/`; subagents read libraries and do not ingest or alter sources. The coordinator assembles outputs and records which sources/sections were inspected, skipped or remain unchecked. Retain the snapshot manifest alongside the curriculum's traceability/requirements record. Do not call retrieval or import counts a completed review.

```text
python3 TOOL check-citations --project COURSE --snapshot SNAPSHOT /path/to/traceability.md /path/to/review.md
```

This check verifies only that bracketed content/institution passage IDs exist and belong to the chosen snapshot. It reports unknown IDs, historical citations, and files with no citations. A successful exit does **not** verify that a passage supports a claim or prove complete citation coverage. The quality reviewer must check meaning and institutional applicability against actual passages.

Course storage is local: `.cadence/library.sqlite3`, retained originals, and source manifests. The host model still receives any passages Codex reads. The helpers make no model, provider, network or embedding calls. This prototype has no shared accounts, authorization boundary between libraries, or tamper-proof approval system.
