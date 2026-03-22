from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDY_DIR = ROOT / "knowledge_base" / "study"
PORTAL_SRC = ROOT / "portal_src"
PORTAL_OUT = ROOT / "portal"

EXCLUDED_FILES = {"README.md"}
CATEGORY_LABELS = {
    "classic_ml": "Classic ML",
    "recsys": "Recsys",
    "deep_learning": "Deep Learning",
    "nlp_llm": "NLP / LLM",
    "cv": "Computer Vision",
    "metrics": "Metrics",
    "python": "Python",
    "databases": "Databases",
    "production": "Production",
    "statistics": "Statistics",
}


def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


def extract_summary(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    for line in lines[1:]:
        if not line:
            continue
        if line.startswith(">"):
            continue
        if line.startswith("#"):
            continue
        return line
    return "Учебный модуль для повторения."


def extract_search_text(text: str) -> str:
    collected: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            collected.append(stripped.lstrip("# ").strip())
        elif stripped.startswith("<summary>") and stripped.endswith("</summary>"):
            collected.append(stripped.removeprefix("<summary>").removesuffix("</summary>").strip())
    return " ".join(collected)


def build_manifest() -> list[dict[str, object]]:
    manifest: list[dict[str, object]] = []

    for path in sorted(STUDY_DIR.rglob("*.md")):
        rel = path.relative_to(STUDY_DIR)
        if rel.name in EXCLUDED_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        if rel.name == "HANDBOOK.md":
            manifest.append(
                {
                    "path": "__handbook__",
                    "sourcePath": rel.as_posix(),
                    "title": "Общий handbook",
                    "summary": "Единый файл со всеми study-модулями подряд.",
                    "category": "study",
                    "categoryLabel": "Общее",
                    "questionCount": text.count("<summary>"),
                    "searchText": "handbook all modules общий файл summary",
                }
            )
            continue

        category = rel.parts[0]
        manifest.append(
            {
                "path": rel.as_posix(),
                "sourcePath": rel.as_posix(),
                "title": extract_title(text),
                "summary": extract_summary(text),
                "category": category,
                "categoryLabel": CATEGORY_LABELS.get(category, category),
                "questionCount": text.count("<summary>"),
                "searchText": extract_search_text(text),
            }
        )

    return manifest


def copy_content() -> None:
    content_out = PORTAL_OUT / "content"
    content_out.mkdir(parents=True, exist_ok=True)
    for path in sorted(STUDY_DIR.rglob("*.md")):
        rel = path.relative_to(STUDY_DIR)
        if rel.name in EXCLUDED_FILES:
            continue
        target = content_out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def copy_static_assets() -> None:
    for source in PORTAL_SRC.rglob("*"):
        if source.is_dir():
            continue
        rel = source.relative_to(PORTAL_SRC)
        target = PORTAL_OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def write_manifest(manifest: list[dict[str, object]]) -> None:
    assets_dir = PORTAL_OUT / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "modules.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def collect_precache_urls(manifest: list[dict[str, object]]) -> list[str]:
    urls = [
        "./",
        "./index.html",
        "./site.webmanifest",
        "./assets/app.js",
        "./assets/styles.css",
        "./assets/modules.json",
        "./assets/icon.svg",
    ]

    for item in manifest:
        source_path = str(item["sourcePath"])
        urls.append(f"./content/{source_path}")

    unique_urls = sorted(dict.fromkeys(urls))
    return unique_urls


def write_service_worker(manifest: list[dict[str, object]]) -> None:
    precache_urls = collect_precache_urls(manifest)
    version_seed = "\n".join(precache_urls)
    cache_name = f"ml-portal-{hashlib.sha256(version_seed.encode('utf-8')).hexdigest()[:12]}"

    script = f"""const CACHE_NAME = "{cache_name}";
const PRECACHE_URLS = {json.dumps(precache_urls, ensure_ascii=False, indent=2)};

self.addEventListener("install", (event) => {{
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
}});

self.addEventListener("activate", (event) => {{
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key.startsWith("ml-portal-") && key !== CACHE_NAME)
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
}});

self.addEventListener("fetch", (event) => {{
  const request = event.request;
  if (request.method !== "GET") {{
    return;
  }}

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) {{
    return;
  }}

  if (request.mode === "navigate") {{
    event.respondWith(fetch(request).catch(() => caches.match("./index.html")));
    return;
  }}

  event.respondWith(
    caches.match(request).then((cachedResponse) => {{
      if (cachedResponse) {{
        return cachedResponse;
      }}

      return fetch(request).then((networkResponse) => {{
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== "basic") {{
          return networkResponse;
        }}

        const responseClone = networkResponse.clone();
        event.waitUntil(
          caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone))
        );
        return networkResponse;
      }});
    }})
  );
}});
"""

    (PORTAL_OUT / "sw.js").write_text(script, encoding="utf-8")


def write_nojekyll() -> None:
    (PORTAL_OUT / ".nojekyll").write_text("", encoding="utf-8")


def write_readme() -> None:
    text = """# Portal

Это статический сайт для повторения ML interview modules с телефона и компьютера.

## Как пересобрать

```bash
python3 scripts/build_study_modules.py
python3 scripts/build_portal.py
```

## Как открыть локально

```bash
cd portal
python3 -m http.server 8000
```

Потом открыть `http://localhost:8000`.

## Как деплоить

- Если репозиторий уже лежит на GitHub, удобнее всего включить GitHub Pages и использовать workflow из `.github/workflows/deploy-portal.yml`.
- Если хочешь максимально быстрый внешний хостинг с предпросмотрами и отдельным доменом, удобно использовать Cloudflare Pages.
- Для Cloudflare Pages можно собрать портал локально и публиковать папку `portal/` как статический output.

Для деплоя обычно публикуют содержимое папки `portal/`.
"""
    (PORTAL_OUT / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    if PORTAL_OUT.exists():
        shutil.rmtree(PORTAL_OUT)
    PORTAL_OUT.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest()
    copy_static_assets()
    copy_content()
    write_manifest(manifest)
    write_service_worker(manifest)
    write_nojekyll()
    write_readme()

    print(f"Built portal at {PORTAL_OUT.relative_to(ROOT)}")
    print(f"Modules: {len(manifest)}")


if __name__ == "__main__":
    main()
