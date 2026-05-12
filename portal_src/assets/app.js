const CATEGORY_LABELS = {
  classic_ml: "Classic ML",
  deep_learning: "Deep Learning",
  nlp_llm: "NLP / LLM",
  cv: "Computer Vision",
  recsys: "Recsys",
  metrics: "Metrics",
  statistics: "Statistics",
  python: "Python",
  production: "Production",
  databases: "Databases",
};
const CATEGORY_ORDER = [
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
];
const MLSD_ROUTE = "mlsd";
const PLANTUML_SERVER = "https://www.plantuml.com/plantuml/svg/";
const PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_";
const RUNTIME_CACHE_BUST = Date.now().toString(36);

const state = {
  mode: "study",
  modules: [],
  filtered: [],
  diagrams: [],
  filteredDiagrams: [],
  currentPath: null,
  currentModule: null,
  currentDiagramSlug: null,
  lastOpened: localStorage.getItem("ml-portal-last-opened"),
  deferredInstallPrompt: null,
};

const els = {
  sidebar: document.getElementById("sidebar"),
  openSidebar: document.getElementById("open-sidebar"),
  closeSidebar: document.getElementById("close-sidebar"),
  moduleNav: document.getElementById("module-nav"),
  moduleGrid: document.getElementById("module-grid"),
  learningRoute: document.getElementById("learning-route"),
  search: document.getElementById("module-search"),
  searchLabel: document.querySelector(".search-box__label"),
  studyTab: document.getElementById("study-tab"),
  mlsdTab: document.getElementById("mlsd-tab"),
  studyActions: document.getElementById("study-actions"),
  homePanel: document.getElementById("home-panel"),
  readerPanel: document.getElementById("reader-panel"),
  mlsdPanel: document.getElementById("mlsd-panel"),
  mlsdContent: document.getElementById("mlsd-content"),
  articleContent: document.getElementById("article-content"),
  articleToc: document.getElementById("article-toc"),
  topbarTitle: document.getElementById("topbar-title"),
  topbarMeta: document.getElementById("topbar-meta"),
  continueButton: document.getElementById("continue-button"),
  installApp: document.getElementById("install-app"),
  openHandbook: document.getElementById("open-handbook"),
  openHandbookHome: document.getElementById("open-handbook-home"),
  openMlsdHome: document.getElementById("open-mlsd-home"),
  startLearning: document.getElementById("start-learning"),
  backHome: document.getElementById("back-home"),
  copyLink: document.getElementById("copy-link"),
  expandAll: document.getElementById("expand-all"),
  collapseAll: document.getElementById("collapse-all"),
};

function slugify(text) {
  return text
    .toLowerCase()
    .trim()
    .replace(/ё/g, "е")
    .replace(/[^\p{L}\p{N}\s-]/gu, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}

function getHashPath() {
  const raw = decodeURIComponent(window.location.hash.replace(/^#\/?/, ""));
  return raw || null;
}

function setHashPath(path) {
  window.location.hash = path ? `#/${encodeURIComponent(path)}` : "";
}

function humanCategory(category) {
  return CATEGORY_LABELS[category] || category;
}

function isMlsdPath(path) {
  return path === MLSD_ROUTE || path.startsWith(`${MLSD_ROUTE}/`);
}

function getMlsdPath(slug) {
  return slug ? `${MLSD_ROUTE}/${slug}` : MLSD_ROUTE;
}

function getVersionedMlsdAsset(path, version) {
  const suffix = version ? `?v=${encodeURIComponent(version)}` : "";
  return `./mlsd/${path}${suffix}`;
}

function getRuntimeVersionedAsset(path) {
  return `${path}?v=${RUNTIME_CACHE_BUST}`;
}

function pluralize(value, one, few, many) {
  const n = Math.abs(value) % 100;
  const n1 = n % 10;
  if (n > 10 && n < 20) return many;
  if (n1 > 1 && n1 < 5) return few;
  if (n1 === 1) return one;
  return many;
}

function closeSidebarOnMobile() {
  els.sidebar.classList.remove("is-open");
}

function isStandaloneMode() {
  return window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
}

function toggleInstallButton() {
  if (!els.installApp) return;
  const shouldShow = Boolean(state.deferredInstallPrompt) && !isStandaloneMode();
  els.installApp.hidden = !shouldShow;
}

function matchesSearch(module, query) {
  if (!query) return true;
  const haystack = [
    module.title,
    module.summary,
    module.categoryLabel,
    module.searchText,
  ]
    .join(" ")
    .toLowerCase();
  return haystack.includes(query.toLowerCase());
}

function matchesDiagram(diagram, query) {
  if (!query) return true;
  const terms = (diagram.terms || []).flatMap((term) => [term.name, term.definition]);
  const haystack = [
    diagram.title,
    diagram.sourceHeading,
    diagram.summary,
    diagram.interviewAnswer,
    ...(diagram.talkTrack || []),
    ...terms,
  ]
    .join(" ")
    .toLowerCase();
  return haystack.includes(query.toLowerCase());
}

function applySearch() {
  const query = els.search.value.trim();
  if (state.mode === "mlsd") {
    state.filteredDiagrams = state.diagrams.filter((diagram) => matchesDiagram(diagram, query));
    renderSidebar();
    return;
  }

  state.filtered = state.modules.filter((module) => matchesSearch(module, query));
  renderSidebar();
  renderModuleGrid();
}

function groupModules(modules) {
  const grouped = new Map();
  for (const module of modules) {
    const key = module.category;
    if (!grouped.has(key)) grouped.set(key, []);
    grouped.get(key).push(module);
  }

  return CATEGORY_ORDER.filter((category) => grouped.has(category)).map((category) => ({
    category,
    modules: grouped.get(category),
  }));
}

function renderSidebar() {
  if (state.mode === "mlsd") {
    renderMlsdSidebar();
    return;
  }

  const groups = groupModules(state.filtered);
  const fragments = [];

  for (const group of groups) {
    const { category, modules } = group;
    const items = modules
      .map((module) => {
        const active = module.path === state.currentPath ? " is-active" : "";
        return `
          <button class="module-link${active}" data-open-module="${module.path}" type="button">
            <strong>${module.title}</strong>
            <span>${module.questionCount} ${pluralize(module.questionCount, "вопрос", "вопроса", "вопросов")}</span>
          </button>
        `;
      })
      .join("");

    fragments.push(`
      <section class="module-group">
        <p class="module-group__title">${humanCategory(category)}</p>
        <div class="module-group__list">${items}</div>
      </section>
    `);
  }

  if (!fragments.length) {
    els.moduleNav.innerHTML = `<p class="section-header__note">По этому запросу ничего не нашлось.</p>`;
    return;
  }

  els.moduleNav.innerHTML = fragments.join("");
}

function renderMlsdSidebar() {
  if (!state.filteredDiagrams.length) {
    els.moduleNav.innerHTML = `<p class="section-header__note">По этому запросу диаграммы не нашлись.</p>`;
    return;
  }

  const items = state.filteredDiagrams
    .map((diagram) => {
      const active = diagram.slug === state.currentDiagramSlug ? " is-active" : "";
      return `
        <button class="module-link${active}" data-open-mlsd="${diagram.slug}" type="button">
          <strong>${diagram.index}. ${diagram.title}</strong>
          <span>${diagram.sourceHeading}</span>
        </button>
      `;
    })
    .join("");

  els.moduleNav.innerHTML = `
    <section class="module-group">
      <p class="module-group__title">MLSD diagrams</p>
      <div class="module-group__list">${items}</div>
    </section>
  `;
}

function renderLearningRoute() {
  const groups = groupModules(state.modules.filter((item) => item.path !== "__handbook__"));
  els.learningRoute.innerHTML = groups
    .map((group, index) => {
      const firstModule = group.modules[0];
      return `
        <button class="route-card" data-open-module="${firstModule.path}" type="button">
          <span class="route-card__step">Шаг ${index + 1}</span>
          <strong>${humanCategory(group.category)}</strong>
          <span>${group.modules.length} ${pluralize(group.modules.length, "модуль", "модуля", "модулей")}</span>
        </button>
      `;
    })
    .join("");
}

function renderModuleGrid() {
  if (!state.filtered.length) {
    els.moduleGrid.innerHTML = `<div class="tip-card"><h3>Ничего не найдено</h3><p>Попробуй другой запрос или очисти поиск.</p></div>`;
    return;
  }

  const groups = groupModules(state.filtered);
  els.moduleGrid.innerHTML = groups
    .map((group) => {
      const cards = group.modules
        .map(
          (module) => `
            <button class="module-card" data-open-module="${module.path}" type="button">
              <div class="module-card__meta">
                <span>${module.categoryLabel}</span>
                <span>${module.questionCount} ${pluralize(module.questionCount, "вопрос", "вопроса", "вопросов")}</span>
              </div>
              <h4>${module.title}</h4>
              <p class="module-card__summary">${module.summary}</p>
              <p class="module-card__footer">Открыть модуль</p>
            </button>
          `
        )
        .join("");

      return `
        <section class="module-section">
          <div class="module-section__header">
            <p class="eyebrow">Раздел</p>
            <h3>${humanCategory(group.category)}</h3>
          </div>
          <div class="module-section__grid">
            ${cards}
          </div>
        </section>
      `;
    })
    .join("");
}

function rewriteLocalLinks(root) {
  root.querySelectorAll("a[href]").forEach((link) => {
    const href = link.getAttribute("href");
    if (!href) return;

    const studyMarker = "/knowledge_base/study/";
    if (href.includes(studyMarker)) {
      const relative = href.split(studyMarker)[1];
      link.setAttribute("href", `#/${encodeURIComponent(relative)}`);
      link.addEventListener("click", () => {
        closeSidebarOnMobile();
      });
      return;
    }

    if (href.startsWith("/Users/")) {
      link.removeAttribute("href");
      link.style.pointerEvents = "none";
      link.style.opacity = "0.7";
      return;
    }

    if (href.startsWith("http")) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noreferrer");
    }
  });
}

function buildToc(root) {
  const headings = [...root.querySelectorAll("h2, h3")];
  const usedIds = new Set();
  const tocItems = [];

  headings.forEach((heading) => {
    const text = heading.textContent.trim();
    if (!text) return;

    let id = slugify(text);
    let suffix = 2;
    while (usedIds.has(id)) {
      id = `${slugify(text)}-${suffix}`;
      suffix += 1;
    }
    usedIds.add(id);
    heading.id = id;
    tocItems.push({
      id,
      text,
      depth: heading.tagName === "H2" ? 2 : 3,
    });
  });

  if (!tocItems.length) {
    els.articleToc.innerHTML = `<p class="section-header__note">Оглавление появится после загрузки модуля.</p>`;
    return;
  }

  els.articleToc.innerHTML = tocItems
    .map(
      (item) => `
        <a href="#${item.id}" style="padding-left:${item.depth === 3 ? "14px" : "0"}">
          ${item.text}
        </a>
      `
    )
    .join("");
}

function updateTopbar(module) {
  if (!module) {
    els.topbarTitle.textContent = "Выбери модуль";
    els.topbarMeta.textContent = "";
    return;
  }
  const modulesOnly = state.modules.filter((item) => item.path !== "__handbook__");
  const position = modulesOnly.findIndex((item) => item.path === module.path);
  const routeMeta = position >= 0 ? `Модуль ${position + 1} из ${modulesOnly.length}` : "Общий режим";
  els.topbarTitle.textContent = module.title;
  els.topbarMeta.textContent = `${module.categoryLabel} · ${module.questionCount} ${pluralize(module.questionCount, "вопрос", "вопроса", "вопросов")} · ${routeMeta}`;
}

function updateMlsdTopbar(diagram) {
  els.topbarTitle.textContent = diagram ? diagram.title : "ML System Design";
  els.topbarMeta.textContent = `${state.diagrams.length} ${pluralize(state.diagrams.length, "диаграмма", "диаграммы", "диаграмм")} · PlantUML`;
}

function setMode(mode) {
  state.mode = mode;
  const isMlsd = mode === "mlsd";

  els.studyTab.classList.toggle("is-active", !isMlsd);
  els.mlsdTab.classList.toggle("is-active", isMlsd);
  els.studyActions.classList.toggle("is-hidden", isMlsd);
  els.searchLabel.textContent = isMlsd ? "Поиск по MLSD" : "Поиск по модулям";
  els.search.placeholder = isMlsd ? "Например: PR-AUC, rollout, feature store" : "Например: RAG, SVM, метрики";
}

function revealReaderMode(module) {
  setMode("study");
  els.homePanel.classList.add("is-hidden");
  els.mlsdPanel.classList.add("is-hidden");
  els.readerPanel.classList.remove("is-hidden");
  updateTopbar(module);
}

function revealHomeMode() {
  setMode("study");
  state.currentModule = null;
  state.currentPath = null;
  state.currentDiagramSlug = null;
  els.readerPanel.classList.add("is-hidden");
  els.mlsdPanel.classList.add("is-hidden");
  els.homePanel.classList.remove("is-hidden");
  els.articleContent.innerHTML = "";
  els.articleToc.innerHTML = "";
  updateTopbar(null);
  renderSidebar();
}

function revealMlsdMode(diagram) {
  setMode("mlsd");
  state.currentModule = null;
  state.currentPath = null;
  els.homePanel.classList.add("is-hidden");
  els.readerPanel.classList.add("is-hidden");
  els.mlsdPanel.classList.remove("is-hidden");
  updateMlsdTopbar(diagram);
  renderSidebar();
}

async function copyText(value) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(value);
    return true;
  }
  window.prompt("Скопируй ссылку вручную", value);
  return false;
}

async function renderMath() {
  if (window.MathJax?.typesetPromise) {
    await window.MathJax.typesetPromise([els.articleContent]);
  }
}

function bindDetailsMathRendering() {
  els.articleContent.querySelectorAll("details").forEach((item) => {
    item.addEventListener("toggle", () => {
      if (!item.open || !window.MathJax?.typesetPromise) {
        return;
      }
      window.MathJax.typesetPromise([item]).catch((error) => {
        console.error("MathJax details rendering failed", error);
      });
    });
  });
}

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function encodePlantUmlBase64(bytes) {
  let output = "";

  for (let index = 0; index < bytes.length; index += 3) {
    const b1 = bytes[index];
    const b2 = index + 1 < bytes.length ? bytes[index + 1] : 0;
    const b3 = index + 2 < bytes.length ? bytes[index + 2] : 0;
    const c1 = b1 >> 2;
    const c2 = ((b1 & 0x3) << 4) | (b2 >> 4);
    const c3 = ((b2 & 0xf) << 2) | (b3 >> 6);
    const c4 = b3 & 0x3f;

    output += PLANTUML_ALPHABET[c1 & 0x3f];
    output += PLANTUML_ALPHABET[c2 & 0x3f];
    if (index + 1 < bytes.length) output += PLANTUML_ALPHABET[c3 & 0x3f];
    if (index + 2 < bytes.length) output += PLANTUML_ALPHABET[c4 & 0x3f];
  }

  return output;
}

function buildPlantUmlUrl(uml) {
  if (!window.pako?.deflateRaw) {
    return null;
  }
  const bytes = new TextEncoder().encode(uml);
  const compressed = window.pako.deflateRaw(bytes, { level: 9 });
  return `${PLANTUML_SERVER}${encodePlantUmlBase64(compressed)}`;
}

function normalizeMathDelimiters(markdown) {
  const fencedCodePattern = /(```[\s\S]*?```)/g;

  return markdown
    .split(fencedCodePattern)
    .map((chunk, index) => {
      if (index % 2 === 1) {
        return chunk;
      }

      return chunk
        .replace(/\\\[((?:.|\n)*?)\\\]/g, (_, expression) => `\n$$\n${expression.trim()}\n$$\n`)
        .replace(/\\\((.+?)\\\)/g, (_, expression) => `$${expression.trim()}$`);
    })
    .join("");
}

function renderMarkdown(markdown) {
  return window.marked.parse(normalizeMathDelimiters(markdown), {
    gfm: true,
    breaks: false,
    headerIds: false,
    mangle: false,
  });
}

function preprocessDetailsMarkdown(markdown) {
  const detailsPattern = /<details>\s*<summary>([\s\S]*?)<\/summary>\s*([\s\S]*?)<\/details>/g;

  return markdown.replace(detailsPattern, (_, rawSummary, rawBody) => {
    const summary = escapeHtml(rawSummary.trim());
    const body = rawBody.trim();
    const bodyHtml = body ? renderMarkdown(body).trim() : "";

    return [
      "<details>",
      `<summary>${summary}</summary>`,
      '<div class="details-content">',
      bodyHtml,
      "</div>",
      "</details>",
    ].join("\n");
  });
}

async function fetchMarkdownBySourcePath(sourcePath) {
  const response = await fetch(`./content/${sourcePath}`);
  if (!response.ok) {
    return null;
  }
  return response.text();
}

async function fetchMlsdManifest() {
  try {
    const response = await fetch(getRuntimeVersionedAsset("./mlsd/manifest.json"), {
      cache: "no-store",
    });
    if (!response.ok) {
      return [];
    }
    return response.json();
  } catch (error) {
    console.warn("MLSD manifest is not available", error);
    return [];
  }
}

async function fetchMlsdUml(diagram) {
  const response = await fetch(getVersionedMlsdAsset(diagram.umlPath, diagram.umlHash), {
    cache: "no-store",
  });
  if (!response.ok) {
    return null;
  }
  return response.text();
}

function renderMlsdTerms(diagram) {
  const terms = diagram.terms || [];
  if (!terms.length) {
    return "";
  }

  return `
    <section class="mlsd-notes-block">
      <p class="eyebrow">Термины</p>
      <dl class="mlsd-terms">
        ${terms
          .map(
            (term) => `
              <div>
                <dt>${escapeHtml(term.name)}</dt>
                <dd>${escapeHtml(term.definition)}</dd>
              </div>
            `
          )
          .join("")}
      </dl>
    </section>
  `;
}

function renderMlsdDiagram(diagram, uml) {
  const sourceHref = getVersionedMlsdAsset(diagram.umlPath, diagram.umlHash);
  const noteHref = getVersionedMlsdAsset(diagram.notePath, diagram.noteHash);
  const imageUrl = uml ? buildPlantUmlUrl(uml) : null;
  const talkTrack = (diagram.talkTrack || []).map((point) => `<li>${escapeHtml(point)}</li>`).join("");
  const diagramFrame = imageUrl
    ? `
      <a class="mlsd-diagram-frame mlsd-diagram-frame--${diagram.slug}" href="${imageUrl}" target="_blank" rel="noreferrer">
        <img id="mlsd-diagram-img" src="${imageUrl}" alt="${escapeHtml(diagram.title)}" />
      </a>
      <div class="mlsd-render-warning is-hidden" id="mlsd-render-warning">
        Не удалось загрузить SVG с PlantUML server. Исходник ниже готов для локального рендера в PDF или SVG.
      </div>
    `
    : `
      <div class="mlsd-render-warning">
        Для SVG-превью нужен pako из CDN. Исходник ниже готов для локального рендера в PDF или SVG.
      </div>
    `;

  els.mlsdContent.innerHTML = `
    <div class="mlsd-hero">
      <div>
        <p class="eyebrow">ML System Design</p>
        <h2>${escapeHtml(diagram.title)}</h2>
        <p>${escapeHtml(diagram.summary)}</p>
      </div>
      <div class="mlsd-actions">
        ${imageUrl ? `<a class="ghost-btn" href="${imageUrl}" target="_blank" rel="noreferrer">Открыть SVG</a>` : ""}
        <a class="ghost-btn" href="${sourceHref}" target="_blank" rel="noreferrer">.uml файл</a>
        <a class="ghost-btn" href="${noteHref}" target="_blank" rel="noreferrer">Конспект</a>
      </div>
    </div>

    <div class="mlsd-viewer-grid">
      <section class="mlsd-diagram-card">
        ${diagramFrame}
      </section>

      <aside class="mlsd-notes-card">
        <section class="mlsd-notes-block">
          <p class="eyebrow">Что проговорить</p>
          <ul>${talkTrack}</ul>
        </section>
        ${renderMlsdTerms(diagram)}
        <section class="mlsd-notes-block">
          <p class="eyebrow">Быстрый ответ</p>
          <p>${escapeHtml(diagram.interviewAnswer)}</p>
        </section>
      </aside>
    </div>

    <details class="mlsd-source">
      <summary>PlantUML source</summary>
      <pre><code>${escapeHtml(uml || "Не удалось загрузить UML-файл.")}</code></pre>
    </details>
  `;

  const image = document.getElementById("mlsd-diagram-img");
  const warning = document.getElementById("mlsd-render-warning");
  if (image && warning) {
    image.addEventListener("error", () => {
      warning.classList.remove("is-hidden");
    });
  }
}

async function loadMlsdDiagram(slug) {
  if (!state.diagrams.length) {
    state.currentDiagramSlug = null;
    els.mlsdContent.innerHTML = `
      <div class="tip-card">
        <h3>MLSD диаграммы не найдены</h3>
        <p>Проверь, что выполнен <code>python3 scripts/build_mlsd_diagrams.py</code> и сайт пересобран.</p>
      </div>
    `;
    revealMlsdMode(null);
    closeSidebarOnMobile();
    return;
  }

  const diagram = state.diagrams.find((item) => item.slug === slug) || state.diagrams[0];
  state.currentDiagramSlug = diagram.slug;
  const uml = await fetchMlsdUml(diagram);
  renderMlsdDiagram(diagram, uml);
  revealMlsdMode(diagram);
  closeSidebarOnMobile();
}

async function buildHandbookFromModules() {
  const modules = state.modules.filter((item) => item.path !== "__handbook__");
  const sections = ["# ML Interview Study Handbook"];

  for (const module of modules) {
    const markdown = await fetchMarkdownBySourcePath(module.sourcePath);
    if (!markdown) {
      continue;
    }
    sections.push("");
    sections.push("---");
    sections.push("");
    sections.push(`<!-- source: ${module.sourcePath} -->`);
    sections.push("");
    sections.push(markdown.trim());
  }

  return sections.join("\n");
}

async function loadModule(path) {
  const module = state.modules.find((item) => item.path === path);
  if (!module) {
    revealHomeMode();
    return;
  }

  state.currentPath = path;
  state.currentModule = module;
  localStorage.setItem("ml-portal-last-opened", path);
  toggleContinueButton();
  renderSidebar();

  let markdown = await fetchMarkdownBySourcePath(module.sourcePath);

  if (!markdown && module.path === "__handbook__") {
    markdown = await buildHandbookFromModules();
  }

  if (!markdown) {
    els.articleContent.innerHTML = `<div class="tip-card"><h3>Не удалось загрузить модуль</h3><p>Проверь, что сайт собран полностью и файл существует.</p></div>`;
    revealReaderMode(module);
    return;
  }

  const html = renderMarkdown(preprocessDetailsMarkdown(markdown));

  els.articleContent.innerHTML = html;
  rewriteLocalLinks(els.articleContent);
  buildToc(els.articleContent);
  bindDetailsMathRendering();
  await renderMath();
  revealReaderMode(module);
  closeSidebarOnMobile();
}

function toggleContinueButton() {
  if (!state.lastOpened) {
    els.continueButton.hidden = true;
    return;
  }
  const module = state.modules.find((item) => item.path === state.lastOpened);
  if (!module) {
    els.continueButton.hidden = true;
    return;
  }
  els.continueButton.hidden = false;
  els.continueButton.textContent = `Продолжить: ${module.title}`;
}

async function route() {
  const hashPath = getHashPath();
  if (!hashPath) {
    revealHomeMode();
    return;
  }
  if (isMlsdPath(hashPath)) {
    const slug = hashPath.split("/")[1] || null;
    await loadMlsdDiagram(slug);
    return;
  }
  if (hashPath === "__handbook__") {
    const handbook = state.modules.find((item) => item.path === "__handbook__");
    if (handbook) {
      await loadModule(handbook.path);
      return;
    }
    revealHomeMode();
    return;
  }
  await loadModule(hashPath);
}

function attachUiHandlers() {
  document.addEventListener("click", async (event) => {
    const target = event.target.closest("[data-open-module]");
    if (target) {
      const path = target.getAttribute("data-open-module");
      state.lastOpened = path;
      setHashPath(path);
      return;
    }

    const mlsdTarget = event.target.closest("[data-open-mlsd]");
    if (mlsdTarget) {
      const slug = mlsdTarget.getAttribute("data-open-mlsd");
      setHashPath(getMlsdPath(slug));
      return;
    }
  });

  els.search.addEventListener("input", applySearch);
  els.studyTab.addEventListener("click", () => {
    setHashPath("");
  });
  els.mlsdTab.addEventListener("click", () => {
    const slug = state.currentDiagramSlug || state.diagrams[0]?.slug || null;
    setHashPath(getMlsdPath(slug));
  });
  els.openSidebar.addEventListener("click", () => els.sidebar.classList.add("is-open"));
  els.closeSidebar.addEventListener("click", closeSidebarOnMobile);
  els.backHome.addEventListener("click", () => {
    setHashPath("");
  });
  els.continueButton.addEventListener("click", () => {
    if (state.lastOpened) setHashPath(state.lastOpened);
  });
  els.startLearning.addEventListener("click", () => {
    const firstModule = state.modules.find((item) => item.path !== "__handbook__");
    if (firstModule) setHashPath(firstModule.path);
  });
  els.installApp.addEventListener("click", async () => {
    if (!state.deferredInstallPrompt) return;
    state.deferredInstallPrompt.prompt();
    await state.deferredInstallPrompt.userChoice.catch(() => null);
    state.deferredInstallPrompt = null;
    toggleInstallButton();
  });
  els.openHandbook.addEventListener("click", () => {
    setHashPath("__handbook__");
  });
  els.openHandbookHome.addEventListener("click", () => {
    setHashPath("__handbook__");
  });
  els.openMlsdHome.addEventListener("click", () => {
    const slug = state.currentDiagramSlug || state.diagrams[0]?.slug || null;
    setHashPath(getMlsdPath(slug));
  });
  els.copyLink.addEventListener("click", async () => {
    const url = window.location.href;
    const copied = await copyText(url);
    els.copyLink.textContent = copied ? "Ссылка скопирована" : "Показал ссылку";
    window.setTimeout(() => {
      els.copyLink.textContent = "Скопировать ссылку";
    }, 1500);
  });
  els.expandAll.addEventListener("click", () => {
    els.articleContent.querySelectorAll("details").forEach((item) => {
      item.open = true;
    });
  });
  els.collapseAll.addEventListener("click", () => {
    els.articleContent.querySelectorAll("details").forEach((item) => {
      item.open = false;
    });
  });

  window.addEventListener("hashchange", route);
  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    state.deferredInstallPrompt = event;
    toggleInstallButton();
  });
  window.addEventListener("appinstalled", () => {
    state.deferredInstallPrompt = null;
    toggleInstallButton();
  });
}

function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) {
    return;
  }

  let refreshing = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (refreshing) return;
    refreshing = true;
    window.location.reload();
  });

  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./sw.js").catch((error) => {
      console.error("Service worker registration failed", error);
    });
  });
}

async function init() {
  const response = await fetch(getRuntimeVersionedAsset("./assets/modules.json"), {
    cache: "no-store",
  });
  const [modules, diagrams] = await Promise.all([response.json(), fetchMlsdManifest()]);
  state.modules = modules;
  state.diagrams = diagrams;
  state.filtered = state.modules.filter((item) => item.path !== "__handbook__");
  state.filteredDiagrams = state.diagrams;
  toggleContinueButton();
  toggleInstallButton();
  renderSidebar();
  renderLearningRoute();
  renderModuleGrid();
  attachUiHandlers();
  registerServiceWorker();
  await route();
}

init().catch((error) => {
  console.error(error);
  els.homePanel.innerHTML = `
    <div class="tip-card">
      <h3>Не удалось инициализировать портал</h3>
      <p>Проверь сборку сайта или открой консоль браузера.</p>
    </div>
  `;
});
