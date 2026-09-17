# Cadence for Codex

Create and review curriculum through ADDIE using two separate local source libraries and predefined specialist subagents. Codex provides the conversation and model runtime; the plugin supplies the instructional workflow, role prompts and retrieval tools. It does not run the web application, PostgreSQL or a separate model server.

## Start a course

After installing the plugin, start a new Codex task and select the **Cadence** skill. For example:

> Use Cadence to build this course. These files contain course content, and these files describe our institution's instructional process. Use specialist subagents as needed and assemble instructor-ready curriculum through ADDIE.

Provide files or local file paths and a folder for the course outputs. The agent classifies the sources, indexes them separately, and works from a saved set of source versions. It checks supplied materials before asking for missing information.

Curriculum reviews default to a concise mode: Cadence works across ADDIE, pauses only for critical failures, authoritative conflicts, or decisions that would materially change the conclusion, and delivers a short decision-oriented review with a linked evidence audit. Missing supporting material is normally recorded as an evidence limitation rather than interrupting the review. Formal phase-gated audit mode remains available when explicitly requested.

Formal audits pause after every phase. In either mode, reports retain sources, checks, concise rationales, findings and user decisions rather than private internal thinking. The saved workflow state allows interrupted work to resume without repeating settled questions.

| Library | Purpose |
| --- | --- |
| Content | Existing curriculum, subject references, readings and teaching material |
| Institution | Local instructional process, policies, standards and templates |

No institutional documents or course content are preloaded. The bundled ADDIE guide is a working method, not a claim about your institution's rules. Institution-specific claims need supporting evidence from your documents.

The coordinator can deploy an institutional process analyst, subject expert, instructional designer, assessment specialist, exercise specialist and independent quality reviewer. Each gets a focused assignment and its predefined prompt. These use the host's native subagents and inherited model; no extra provider key is required. If that capability is unavailable, the plugin discloses sequential checks rather than claiming independent agents ran.

## Deliverables

A build produces actual teaching and learning materials appropriate to the requested scope, plus objective/activity/check traceability and a concise source/decision record. Markdown is the initial portable output. When suitable host document capabilities are available, requested audit reports and curriculum packages can also be delivered as visually checked Word documents. Cadence retains a navy-and-Aptos Word baseline modeled on the established institutional review package; applicable institutional templates and explicit user directions take precedence. True inline comments are anchored to the precise affected wording rather than a general gap summary.

ADDIE covers analysis, design, development, implementation preparation and evaluation planning/formative review. The plugin cannot claim actual delivery or learner effectiveness without delivery and outcome evidence. Course files live outside the plugin installation so updates do not remove your work.

A review remains review-only unless you explicitly authorize revisions. Its five phases inspect needs/context, curriculum design, developed materials, delivery readiness and evaluation evidence. Concise mode produces an executive review backed by detailed evidence records; formal audit mode retains phase reports under `deliverables/`. Workflow state and decisions are retained in `working/review-state.md`.

## Local dependencies

Python 3.10+ with SQLite FTS5 is required. TXT and Markdown ingestion and search need only the Python standard library. PDF, DOCX and PPTX also need the packages in `requirements.txt`. Codex can use an existing document runtime or a project virtual environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r /absolute/path/to/cadence/requirements.txt
```

Use that interpreter for the skill's `scripts/cadence.py`. The full tool guide is [tools.md](skills/cadence/references/tools.md).

Retrieval uses SQLite FTS5/BM25 keyword ranking. It is local retrieval-augmented generation, not a semantic embedding index. Search always names one library. Helpers retain originals, locations, hashes and versioned passages; a source snapshot keeps all specialists on the same versions. The host model receives the passages it reads, while the helper tools make no external or model calls.

Supported sources: TXT, Markdown, DOCX, PDF and PPTX, up to 1 GB per file; PDFs up to 1,000 pages. Mixed PDFs retain readable pages and identify skipped pages. PPTX includes text, tables and speaker notes. No OCR, image interpretation, Moodle/SCORM import or exact layout preservation in this first plugin. This is a single-user local workflow, without team accounts, shared comments or enforced institutional approvals.

## Development and checks

The source plugin lives in `plugins/cadence` in the project repository. Personal marketplace installation is separate from the web app.

```sh
python3 -m unittest discover -s plugins/cadence/tests -v
```

Use an interpreter with the parser dependencies to run the complete suite. Tests use synthetic files and no provider calls. The fixtures also support a manual skill check: ask for a 60-minute project-update workshop using the content and institutional files, then examine the curriculum, source citations and ADDIE status. Automated parser and library checks do not establish educational quality.

Public publication, hosted MCP, semantic embeddings and the earlier web application's collaboration features are outside this first delivery.
