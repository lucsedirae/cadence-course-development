# Workflow progress

Keep a live progress panel beside the conversation when the host supports a browser panel and a persistent local process. Use short milestone updates in chat as well. The panel displays recorded milestones; it cannot independently observe agent execution, estimate time remaining, or certify curriculum quality.

The coordinator is the only writer. Record milestones when they happen, without pausing useful work merely to manufacture updates. Specialists report status to the coordinator and do not edit the progress record.

## Start or resume

For a new project, complete [intake.md](intake.md) before starting progress. Use its saved project name and selected build/review mode; use `orient` while the user is unsure of intent. The panel includes a collapsible record of the initial intake answers.

`PROGRESS` means the absolute path to this skill's `scripts/progress.py`; `COURSE` means the course project folder. Use the same Python interpreter as the library helpers. The progress helper uses only the Python standard library.

```text
python3 PROGRESS init --project COURSE --title "Course title" --mode review
python3 PROGRESS catalog --project COURSE
python3 PROGRESS serve --project COURSE
```

Use `build` or `revise` for those workflows. `init` preserves existing progress. On a genuinely new review/build in the same folder, use `init --new-run` to archive the previous record and start fresh. Do not reset progress merely because a conversation resumed. First inspect any existing `working/review-state.md`; reconcile progress with known evidence and decisions, and do not infer phase completion from the existence of a deliverable alone.

`serve` prints a JSON object containing a loopback `url`, then stays running. Start it using the host's persistent terminal/process facility, keep the returned session handle, and open that exact URL in its in-app browser panel. In Codex, use the available `open_in_codex` tool with a browser target and right placement. Prefer reusing a working viewer for the course over opening duplicates. The panel stays live while its local process runs; stop that process when the user is finished with the view. The record persists after the viewer stops. Do not create recurring automations or other agent processes for the viewer.

If the host cannot serve or display the panel, use `show --format text` and surface the compact phase markers in chat. Explain this fallback once; do not claim the live panel is open. Opening this panel does not add a custom native Codex sidebar or modify the app's own task status.

## Record real milestones

`catalog` attaches the Analysis, Design, and Development subsections defined by the institutional catalog. Analysis has four completion markers (Section 1.3 is split into Parts A and B), Design has six, and Development has 22 artifact types grouped into five categories. The panel displays a checkmark only for a completed subsection with saved supporting content. `catalog` is idempotent for an unchanged catalog; it does not infer subsection completion from older phase-level markers.

```text
python3 PROGRESS section --project COURSE --phase analysis --id analysis.1.1 --status working --note "Writing the needs assessment"
python3 PROGRESS section --project COURSE --phase analysis --id analysis.1.1 --status complete --files deliverables/analysis/analysis-summary-report.md --note "Needs assessment written and source support checked"
python3 PROGRESS section --project COURSE --phase development --id development.3.3 --status skipped --note "The agreed course has no narrated audio component"
```

Read `show` for the section IDs, required document names, and suggested paths. Supply all relevant files after `--files` (or use `--path` for one). All Analysis subsections share the Analysis Summary Report; all Design subsections share the Course Design Document. Add an explanatory completion note identifying what was checked; the tool checks existence and nonempty files, not whether the content meets the catalog. In review-only mode, attach the saved findings report and describe the inspection, not a newly produced course artifact. Mark the entire phase complete only after all its subsection work is completed or explicitly skipped. Skipped, missing, waiting, and blocked items have no completion checkmark. If a supporting file disappears or becomes empty, its checkmark is removed in the viewer and the affected completed phase is shown as needing attention.

```text
python3 PROGRESS phase --project COURSE --phase analysis --status working --note "Checking course purpose and learners"
python3 PROGRESS phase --project COURSE --phase analysis --status complete --note "Scope and learner needs recorded"
python3 PROGRESS phase --project COURSE --phase design --status working --note "Checking the lesson sequence"
python3 PROGRESS agent --project COURSE --id design-1 --role "Instructional designer" --execution native --status working --note "Checking activities against objectives"
python3 PROGRESS agent --project COURSE --id design-1 --role "Instructional designer" --execution native --status complete --note "Findings returned to the coordinator"
python3 PROGRESS artifact --project COURSE --path deliverables/review.md --label "Curriculum review" --status draft
python3 PROGRESS activity --project COURSE --note "Evidence citations checked"
```

Use each subagent's actual assignment ID or a stable local assignment key. Mark an assignment working only after it is actually dispatched. Record returned or failed work promptly. Set `--execution sequential` when applying a role yourself; never label that an independent subagent review. Use new IDs for new assignments so earlier results remain visible.

Supported phase states: `pending`, `working`, `waiting`, `blocked`, `interrupted`, `complete`, `skipped`. Only one ADDIE phase may be working at a time. Skipped phases require a reason and remain visibly skipped. Review phase completion means the authorized review work was done; it does not mean the underlying course passed. In builds, label Implementation as preparation and Evaluation as planning/formative checks unless actual delivery/outcome evidence exists.

Register deliverables only after their files exist inside the course folder. Change `draft` to `checked` only after the relevant quality checks actually ran. A file or a checked label does not establish institutional approval. The panel lists filenames and status; deliver files through the host's normal artifact links.

## Waiting, interruptions, and handoff

```text
python3 PROGRESS run --project COURSE --status waiting --note "Waiting for your decision on the target learners"
python3 PROGRESS run --project COURSE --status working --note "Continuing with the agreed learners"
python3 PROGRESS run --project COURSE --status interrupted --note "Stopped at the user's request"
python3 PROGRESS run --project COURSE --status complete --note "Review and evidence audit ready"
python3 PROGRESS show --project COURSE --format text
```

The other run state is `blocked`; name the actual blocking dependency. Update the phase too when it pauses. Apply the skill's existing pause/approval rules; the panel does not introduce new ones. After interrupting actual subagents, record the interruption; this marks tracked active assignments and phases interrupted but does not stop processes itself. Unexpected host termination cannot write a checkpoint: the panel shows the last milestone time, and a lost viewer connection is labeled disconnected. On resumption, inspect actual task state before restoring working labels.

Before marking the run complete, settle the phase statuses, resolve outstanding specialist work, and verify registered files. Briefly report the result in chat and link the actual deliverables. Keep detailed evidence and decisions in the existing audit/review records, not in progress notes. No percentages, estimated finish times, token usage, or source-review coverage should be invented. Source counts in the panel mean available sources, not inspected sources.

Progress is stored in `COURSE/.cadence/progress.json`, with archived runs in `progress-history/`. The viewer is read-only, listens only on loopback, requires its per-session URL, and serves only its UI and progress state. It makes no model calls and sends no data to external services. Use `init --demo` only for clearly labeled illustrative previews in a separate synthetic project.
