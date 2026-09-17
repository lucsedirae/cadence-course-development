"""Read the selected catalog's explicit phase headings as artifact checkpoints."""
from __future__ import annotations

import hashlib
from pathlib import Path
import re

INSTITUTION_DIR = Path(__file__).resolve().parent.parent / "assets" / "institution"
CATALOG_NAME = "Cadence_ADDIE_Artifact_Catalog.md"


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def definition(path=None):
    source = Path(path) if path else INSTITUTION_DIR / CATALOG_NAME
    data = source.read_bytes()
    phases = {}
    phase = None
    group = ""
    parent = None
    for line_number, line in enumerate(data.decode("utf-8").splitlines(), 1):
        heading = re.match(r"^## (ANALYSIS|DESIGN|DEVELOPMENT) PHASE:", line)
        if heading:
            phase = heading[1].lower()
            phases[phase] = {"document": "", "sections": []}
            group = ""
            parent = None
            continue
        if line.startswith("## "):
            phase = None
        if phase is None:
            continue
        document = re.match(r"^### 1\. \*\*(.+)\*\*$", line)
        if document and phase != "development":
            phases[phase]["document"] = document[1]
        category = re.match(r"^### Category (\d+): (.+)$", line)
        if category:
            group = f"{category[1]}. {category[2]}"
        section = re.match(r"^#### Section ([\d.]+): (.+)$", line) if phase != "development" else re.match(r"^#### ([\d.]+) \*\*(.+)\*\*$", line)
        if section:
            number, label = section.groups()
            document_title = phases[phase]["document"] if phase != "development" else label
            phases[phase]["sections"].append({
                "id": f"{phase}.{number}", "number": number, "title": label, "group": group,
                "document": document_title,
                "suggested_path": f"deliverables/{phase}/{slug(document_title)}.md",
                "source_location": f"{CATALOG_NAME}, line {line_number}",
            })
        part = re.match(r"^\*\*Part ([AB]): (.+)\*\*$", line)
        if phase == "analysis" and part:
            sections = phases[phase]["sections"]
            if part[1] == "A":
                if not sections:
                    raise ValueError("Catalog part has no parent section.")
                parent = sections.pop()
                group = f"{parent['number']}. {parent['title']}"
            if parent is None:
                raise ValueError("Catalog analysis part is missing its section context.")
            title = phases[phase]["document"]
            sections.append({"id": f"analysis.{parent['number']}.{part[1].lower()}",
                             "number": f"{parent['number']}{part[1].lower()}", "title": part[2],
                             "group": group, "document": title,
                             "suggested_path": f"deliverables/analysis/{slug(title)}.md",
                             "source_location": f"{CATALOG_NAME}, line {line_number}"})
    if set(phases) != {"analysis", "design", "development"} or any(not p["sections"] for p in phases.values()):
        raise ValueError("Catalog must contain numbered sections for Analysis, Design, and Development.")
    for phase_name in ("analysis", "design"):
        if not phases[phase_name]["document"]:
            raise ValueError("Catalog must name the consolidated Analysis and Design documents.")
    ids = [s["id"] for p in phases.values() for s in p["sections"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Catalog contains duplicate section identifiers.")
    return {"name": CATALOG_NAME, "sha256": hashlib.sha256(data).hexdigest(), "phases": phases}
