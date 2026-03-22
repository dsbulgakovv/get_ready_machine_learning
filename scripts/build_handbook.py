from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge_base"
OUTPUT = KB / "HANDBOOK.md"

MODULES = [
    KB / "README.md",
    KB / "classic_ml" / "01_models.md",
    KB / "classic_ml" / "02_advanced.md",
    KB / "recsys" / "01_handbook.md",
    KB / "deep_learning" / "01_core.md",
    KB / "nlp_llm" / "01_handbook.md",
    KB / "cv" / "01_handbook.md",
    KB / "metrics" / "01_handbook.md",
    KB / "python" / "01_handbook.md",
    KB / "databases" / "01_handbook.md",
    KB / "production" / "01_handbook.md",
    KB / "statistics" / "01_handbook.md",
]


def read_module(path: Path) -> str:
    if not path.exists():
        study_path = KB / "study" / path.relative_to(KB)
        if study_path.exists():
            path = study_path
    text = path.read_text(encoding="utf-8").strip()
    title = f"\n\n---\n\n<!-- source: {path.relative_to(ROOT)} -->\n\n"
    return title + text + "\n"


def main() -> None:
    parts = ["# ML Interview Handbook\n"]
    for module in MODULES:
        parts.append(read_module(module))
    OUTPUT.write_text("".join(parts), encoding="utf-8")
    print(f"Built {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
