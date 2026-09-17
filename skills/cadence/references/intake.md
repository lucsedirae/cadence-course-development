# New-project intake

Before initializing a new course or starting ADDIE work, collect the seven intake answers. Resume existing projects without repeating intake. Read their `.cadence/intake.json` and working scope/decision record; later explicit user corrections supersede the initial answers. Retain the initial record as history. Earlier four-question records remain readable; the three new answers are labeled “Not asked in earlier intake,” never fabricated as “Not sure yet.” Ask for those missing details only when needed for the current work.

Use `scripts/intake.py` relative to this skill with the same Python interpreter as the other helpers. Choose the user-provided output folder, or a new, clearly named course folder in the authorized workspace. Reuse that exact folder through intake, initialization, and progress. The project name is a display name, never a shell command or filesystem path. Serving the form does not create a course; submission saves only intake.

## Questions

1. **What should we call the project?** A text field.
2. **Are we building?** Brand new course; Review existing course; Not sure yet.
3. **How will learners take this course?** In a classroom (instructor-led); On a computer (self-paced); Mix of both (blended); Not sure yet.
4. **Who are the learners mostly?** Junior enlisted; NCOs; Staff NCOs; Officers; DoW civilians; A mix (civilians/military); A mix (military); Not sure yet.
5. **How long should the course run?** A few hours; About a day; Several days; Weeks or more; Not sure yet.
6. **What is your role?** I'm building it; I teach it; I oversee/approve it.
7. **Do you have source material to work from?** Yes; No; Not sure yet. Examples: doctrine, manuals, or previous course content.

Use one choice per option question, with no preselected defaults. Do not infer expertise, reading level, or proficiency from rank or civilian status. “Not sure yet” is valid; preserve the distinction between unknown and mixed groups.

## Show the form

Run `python3 INTAKE serve --project COURSE` in a persistent process and open the returned URL in the host's browser panel. In Codex, use `open_in_codex` with a browser target and right placement; reuse the intake/progress tab when practical. Keep the process handle. The form shows one question at a time with Back and Continue, then Save answers. It writes to the specified course's `.cadence/intake.json` through a loopback server with a per-session URL and same-origin submission checks. No extra packages or model calls are needed. This is a local browser form, not a native Codex control.

Tell the user briefly that the form is ready. Use `python3 INTAKE wait --project COURSE --timeout 45` for a bounded wait if continuing in this turn. Check the actual returned status; elapsed time is not an answer. If pending, leave the form open and yield with a short instruction to return to chat after saving. Do not poll indefinitely, start ADDIE work, or assume defaults. On continuation, `python3 INTAKE show --project COURSE` reads the answers. Stop the intake server after reading the submission and switching to the progress panel.

If the host cannot show the form, ask conversationally one question at a time with the same options. Reuse answers explicitly supplied by the user instead of asking again. If all seven are already supplied, save directly without another form submission:

```text
python3 INTAKE save --project COURSE --title "Project name" --intent build --delivery classroom --learners ncos --duration few_hours --role builder --source-material yes
```

Use `show` for exact option values. Pass actual user answers, never sample defaults. An explicit decision to defer a choice can be saved as `unsure`; silence cannot. Include the chosen output folder in the handoff so continuation uses the same pending intake.

## Use the answers

Run `cadence.py init --project COURSE` after intake. The CLI requires saved intake for new courses, uses its project name, and indexes bundled institutional guidance. Existing libraries resume without new intake. These are user decisions, not institutional evidence passages or permission to revise a course selected for review.

Initialize progress with the saved title and `--mode build` for a new course or `--mode review` for a review. With intent `unsure`, use `--mode orient`, clarify the immediate goal conversationally, and record that decision before creating curriculum or running a full review. Never default unknown intent to a build or assessment audit. Once settled, start the first substantive progress run with the resolved mode and `--new-run`, preserving intake and earlier progress history.

Include the answers in the scope brief and relevant specialist assignments. Delivery informs activities, pacing, instructor support, and artifact selection. Learner group informs questions about actual roles, prior knowledge, access, and needs; it does not replace Analysis. Keep uncertainties visible and ask a focused follow-up when needed for the next meaningful decision. The progress panel shows the original answers under **Course intake**; record later changes in the working brief.

Duration informs realistic scope, pacing, practice, and workload; these broad ranges are not exact contact hours or a project deadline. The user's role helps tailor guidance and deliverables: building support, teaching preparation, or oversight decisions. Selecting oversight/approval does not itself approve artifacts or establish formal institutional authority. Source availability shapes the next step: for Yes, inspect supplied files or ask for their location; for No or Not sure yet, clarify the subject and available evidence without inventing source support. Do not request files already supplied, treat No as automatic permission to browse externally, or block all planning merely because sources are not yet available.

Use `--demo` only for a separate illustrative preview. Never substitute sample answers for a real course.
