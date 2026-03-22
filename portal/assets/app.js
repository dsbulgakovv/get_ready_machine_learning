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

const state = {
  modules: [],
  filtered: [],
  currentPath: null,
  currentModule: null,
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
  homePanel: document.getElementById("home-panel"),
  readerPanel: document.getElementById("reader-panel"),
  articleContent: document.getElementById("article-content"),
  articleToc: document.getElementById("article-toc"),
  topbarTitle: document.getElementById("topbar-title"),
  topbarMeta: document.getElementById("topbar-meta"),
  continueButton: document.getElementById("continue-button"),
  installApp: document.getElementById("install-app"),
  openHandbook: document.getElementById("open-handbook"),
  openHandbookHome: document.getElementById("open-handbook-home"),
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

function applySearch() {
  const query = els.search.value.trim();
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

function revealReaderMode(module) {
  els.homePanel.classList.add("is-hidden");
  els.readerPanel.classList.remove("is-hidden");
  updateTopbar(module);
}

function revealHomeMode() {
  state.currentModule = null;
  state.currentPath = null;
  els.readerPanel.classList.add("is-hidden");
  els.homePanel.classList.remove("is-hidden");
  els.articleContent.innerHTML = "";
  els.articleToc.innerHTML = "";
  updateTopbar(null);
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

  const response = await fetch(`./content/${module.sourcePath}`);
  if (!response.ok) {
    els.articleContent.innerHTML = `<div class="tip-card"><h3>Не удалось загрузить модуль</h3><p>Проверь, что сайт собран полностью и файл существует.</p></div>`;
    revealReaderMode(module);
    return;
  }

  const markdown = await response.text();
  const html = window.marked.parse(markdown, {
    gfm: true,
    breaks: false,
    headerIds: false,
    mangle: false,
  });

  els.articleContent.innerHTML = html;
  rewriteLocalLinks(els.articleContent);
  buildToc(els.articleContent);
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
  });

  els.search.addEventListener("input", applySearch);
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
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./sw.js").catch((error) => {
      console.error("Service worker registration failed", error);
    });
  });
}

async function init() {
  const response = await fetch("./assets/modules.json");
  state.modules = await response.json();
  state.filtered = state.modules.filter((item) => item.path !== "__handbook__");
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
