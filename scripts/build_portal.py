from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDY_DIR = ROOT / "knowledge_base" / "study"
MLSD_DIR = ROOT / "mlsd_diagrams"
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
CATEGORY_ORDER = [
    "classic_ml",
    "deep_learning",
    "nlp_llm",
    "cv",
    "recsys",
    "metrics",
    "statistics",
    "python",
    "production",
    "databases",
]
CATEGORY_ORDER_INDEX = {name: idx for idx, name in enumerate(CATEGORY_ORDER)}


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

    def sort_key(item: dict[str, object]) -> tuple[int, str, str]:
        category = str(item["category"])
        order = CATEGORY_ORDER_INDEX.get(category, len(CATEGORY_ORDER_INDEX) + 1)
        return (order, category, str(item["path"]))

    handbook_items = [item for item in manifest if item["path"] == "__handbook__"]
    module_items = sorted((item for item in manifest if item["path"] != "__handbook__"), key=sort_key)
    return handbook_items + module_items


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


def copy_mlsd_diagrams() -> list[str]:
    if not (MLSD_DIR / "manifest.json").exists():
        return []

    urls: list[str] = []
    mlsd_out = PORTAL_OUT / "mlsd"
    mlsd_out.mkdir(parents=True, exist_ok=True)

    for source in [
        MLSD_DIR / "manifest.json",
        *sorted((MLSD_DIR / "uml").glob("*.uml")),
        *sorted((MLSD_DIR / "notes").glob("*.md")),
    ]:
        rel = source.relative_to(MLSD_DIR)
        target = mlsd_out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        urls.append(f"./mlsd/{rel.as_posix()}")

    return urls


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


def short_file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def write_asset_versions() -> None:
    index_path = PORTAL_OUT / "index.html"
    app_hash = short_file_hash(PORTAL_OUT / "assets" / "app.js")
    styles_hash = short_file_hash(PORTAL_OUT / "assets" / "styles.css")

    html = index_path.read_text(encoding="utf-8")
    html = html.replace("./assets/styles.css", f"./assets/styles.css?v={styles_hash}")
    html = html.replace("./assets/app.js", f"./assets/app.js?v={app_hash}")
    index_path.write_text(html, encoding="utf-8")


def collect_precache_urls(manifest: list[dict[str, object]], mlsd_urls: list[str]) -> list[str]:
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

    urls.extend(mlsd_urls)

    unique_urls = sorted(dict.fromkeys(urls))
    return unique_urls


def precache_version_seed(urls: list[str]) -> str:
    parts: list[str] = []

    for url in urls:
        if url == "./":
            path = PORTAL_OUT / "index.html"
        else:
            path = PORTAL_OUT / url.removeprefix("./")

        if path.exists():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            digest = "missing"

        parts.append(f"{url}:{digest}")

    return "\n".join(parts)


def write_service_worker(manifest: list[dict[str, object]], mlsd_urls: list[str]) -> None:
    precache_urls = collect_precache_urls(manifest, mlsd_urls)
    version_seed = precache_version_seed(precache_urls)
    cache_name = f"ml-portal-{hashlib.sha256(version_seed.encode('utf-8')).hexdigest()[:12]}"

    script = f"""const CACHE_NAME = "{cache_name}";
const PRECACHE_URLS = {json.dumps(precache_urls, ensure_ascii=False, indent=2)};
const NETWORK_FIRST_PATHS = ["/assets/", "/content/", "/mlsd/"];

function shouldUseNetworkFirst(url) {{
  return NETWORK_FIRST_PATHS.some((path) => url.pathname.includes(path));
}}

function isCacheable(response) {{
  return response && response.status === 200 && response.type === "basic";
}}

function cacheFallback(request) {{
  return caches
    .match(request)
    .then((cachedResponse) => cachedResponse || caches.match(request, {{ ignoreSearch: true }}));
}}

function offlineResponse() {{
  return new Response("Offline", {{
    status: 503,
    headers: {{ "Content-Type": "text/plain; charset=utf-8" }},
  }});
}}

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

  if (shouldUseNetworkFirst(url)) {{
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {{
          if (!isCacheable(networkResponse)) {{
            return networkResponse;
          }}

          const responseClone = networkResponse.clone();
          event.waitUntil(
            caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone))
          );
          return networkResponse;
        }})
        .catch(() => cacheFallback(request).then((cachedResponse) => cachedResponse || offlineResponse()))
    );
    return;
  }}

  event.respondWith(
    cacheFallback(request).then((cachedResponse) => {{
      if (cachedResponse) {{
        return cachedResponse;
      }}

      return fetch(request).then((networkResponse) => {{
        if (!isCacheable(networkResponse)) {{
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
python3 scripts/build_mlsd_diagrams.py
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
    mlsd_urls = copy_mlsd_diagrams()
    write_manifest(manifest)
    write_asset_versions()
    write_service_worker(manifest, mlsd_urls)
    write_nojekyll()
    write_readme()

    print(f"Built portal at {PORTAL_OUT.relative_to(ROOT)}")
    print(f"Modules: {len(manifest)}")


if __name__ == "__main__":
    main()
