# Cadence Word formatting

Read this reference before creating or revising a Cadence `.docx` deliverable. It preserves the visual system established from the institutional curriculum-review document while allowing a supplied institutional template or explicit user instruction to take precedence.

## Authority and reuse

1. If the institution library contains an applicable Word template or a user identifies a reference `.docx`, inspect and inherit its actual Word styles, page geometry, headers/footers, table treatment, and cover hierarchy.
2. Keep the selected visual system consistent across review audits, curriculum packages, and later revisions in the same project. Do not fall back to a generic office theme between exports.
3. When no more authoritative template is available, use the Cadence baseline below.

## Established Cadence baseline

- Page: US Letter, portrait; 0.8-inch left/right margins and 0.7-inch top/bottom margins.
- Body: Aptos, 10.5 pt, black; approximately 1.08 line spacing with 5 pt after paragraphs.
- Title: Aptos Display, 24 pt, navy `#17365D`, centered on a sparse cover.
- Heading 1: Aptos Display, 16 pt, bold, navy `#17365D`.
- Heading 2: Aptos Display, 13 pt, bold, blue `#1F4E79`.
- Heading 3: Aptos Display, 11.5 pt, bold, blue `#2F5597`.
- Tables: dark navy `#17365D` header row with bold white text; white body cells, restrained black borders, and repeated header rows when tables continue.
- Cover: centered title, subdued italic subtitle, preparation date, generous white space, and no running header.
- Footer: centered short document title, bullet separator, and a live page number. Use a cross-compatible simple `PAGE` field with a cached display value, mark it dirty, and set the document to update fields on open so Word, Google Docs, Pages, and PDF renderers receive a visible number.
- Avoid decorative borders, alternating table fills, running headers, or unrelated theme colors unless the governing institutional template uses them.

## Comments and known gaps

- Use true Word comments, not bracketed notes or a comment table.
- Anchor each comment to the narrowest meaningful phrase or sentence in the substantive section that creates the issue. The highlighted text must let a reviewer understand why the comment appears there.
- Do not anchor only to a generic “known gaps,” limitations, or summary bullet when the actual affected passage is present elsewhere.
- Keep one actionable issue per comment. State the practical problem and the decision, evidence, or correction required.
- Preserve unresolved status unless the issue has actually been resolved.
- Verify the selected range and comment text after generation. Structural verification must include the comments part, relationships, content type, and start/end/reference markers.

## Verification

- Use the document-authoring render workflow and inspect every page for clipping, orphaned headings, table overflow, inconsistent fonts, and footer behavior.
- Check early, middle, and final page numbers in the rendered output; do not assume a correct field code guarantees visible numbering in every target editor.
- Confirm that comments remain present and attached to the intended highlighted wording after any rebuild, conversion, or compatibility edit.
- Record any deliberate deviation from this baseline in the deliverable notes.
