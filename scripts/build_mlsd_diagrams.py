from __future__ import annotations

import json
import hashlib
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MLSD_DIR = ROOT / "mlsd_diagrams"
SOURCE_MD = MLSD_DIR / "ml_system_design_lead_ds_plantuml_cheatsheet.md"
CATALOG_PATH = MLSD_DIR / "catalog.json"
UML_DIR = MLSD_DIR / "uml"
NOTES_DIR = MLSD_DIR / "notes"
MANIFEST_PATH = MLSD_DIR / "manifest.json"


HEADING_RE = re.compile(r"^#\s+(\d+)\.\s+(.+?)\s*$")
FENCE_START_RE = re.compile(r"^```plantuml\s*$")
FENCE_END_RE = re.compile(r"^```\s*$")


def extract_plantuml_blocks(markdown: str) -> list[dict[str, object]]:
    lines = markdown.splitlines()
    current_heading: dict[str, object] | None = None
    blocks: list[dict[str, object]] = []
    index = 0

    while index < len(lines):
        heading_match = HEADING_RE.match(lines[index])
        if heading_match:
            current_heading = {
                "index": int(heading_match.group(1)),
                "heading": heading_match.group(2).strip(),
            }
            index += 1
            continue

        if FENCE_START_RE.match(lines[index]) and current_heading:
            block_lines: list[str] = []
            index += 1
            while index < len(lines) and not FENCE_END_RE.match(lines[index]):
                block_lines.append(lines[index])
                index += 1

            blocks.append(
                {
                    "index": current_heading["index"],
                    "heading": current_heading["heading"],
                    "uml": "\n".join(block_lines).strip() + "\n",
                }
            )

        index += 1

    return blocks


def clean_output_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_note(entry: dict[str, object], note_path: Path) -> None:
    lines = [
        f"# {entry['title']}",
        "",
        "## Как читать схему",
        str(entry["summary"]),
        "",
        "## Что проговорить на интервью",
    ]

    for point in entry.get("talkTrack", []):
        lines.append(f"- {point}")

    terms = entry.get("terms", [])
    if terms:
        lines.extend(["", "## Термины и короткие пояснения"])
        for term in terms:
            lines.extend(["", f"### {term['name']}", str(term["definition"])])

    lines.extend(
        [
            "",
            "## Быстрый ответ",
            str(entry["interviewAnswer"]),
            "",
            "## Файл диаграммы",
            f"`{entry['umlPath']}`",
            "",
        ]
    )

    note_path.write_text("\n".join(lines), encoding="utf-8")


def short_hash(content: str | bytes) -> str:
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()[:12]


def main() -> None:
    markdown = SOURCE_MD.read_text(encoding="utf-8")
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    catalog_by_index = {int(item["index"]): item for item in catalog["diagrams"]}
    blocks = extract_plantuml_blocks(markdown)

    clean_output_dir(UML_DIR)
    clean_output_dir(NOTES_DIR)

    manifest: list[dict[str, object]] = []
    for block in blocks:
        block_index = int(block["index"])
        metadata = catalog_by_index.get(block_index)
        if metadata is None:
            raise ValueError(f"Missing catalog metadata for diagram #{block_index}")

        filename = f"{block_index:02d}_{metadata['slug']}.uml"
        note_filename = f"{block_index:02d}_{metadata['slug']}.md"
        uml_path = UML_DIR / filename
        note_path = NOTES_DIR / note_filename
        relative_uml_path = f"uml/{filename}"
        relative_note_path = f"notes/{note_filename}"

        uml_source = str(block["uml"])
        uml_path.write_text(uml_source, encoding="utf-8")

        entry = {
            "index": block_index,
            "slug": metadata["slug"],
            "title": metadata["title"],
            "sourceHeading": block["heading"],
            "umlPath": relative_uml_path,
            "umlHash": short_hash(uml_source),
            "notePath": relative_note_path,
            "summary": metadata["summary"],
            "talkTrack": metadata["talkTrack"],
            "terms": metadata.get("terms", []),
            "interviewAnswer": metadata["interviewAnswer"],
        }
        write_note(entry, note_path)
        entry["noteHash"] = short_hash(note_path.read_bytes())
        manifest.append(entry)

    missing = sorted(set(catalog_by_index) - {int(block["index"]) for block in blocks})
    if missing:
        raise ValueError(f"Catalog has entries without PlantUML blocks: {missing}")

    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {len(manifest)} MLSD diagrams into {UML_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
