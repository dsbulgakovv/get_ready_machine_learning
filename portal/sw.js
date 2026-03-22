const CACHE_NAME = "ml-portal-a4b0288f4c94";
const PRECACHE_URLS = [
  "./",
  "./assets/app.js",
  "./assets/icon.svg",
  "./assets/modules.json",
  "./assets/styles.css",
  "./content/HANDBOOK.md",
  "./content/classic_ml/01_models.md",
  "./content/classic_ml/02_ensembles_and_unsupervised.md",
  "./content/classic_ml/03_anomaly_detection.md",
  "./content/classic_ml/04_ml_fundamentals.md",
  "./content/cv/01_handbook.md",
  "./content/databases/01_handbook.md",
  "./content/deep_learning/01_core.md",
  "./content/metrics/01_handbook.md",
  "./content/nlp_llm/01_text_and_tokenization.md",
  "./content/nlp_llm/02_transformers_and_architectures.md",
  "./content/nlp_llm/03_inference_prompting_and_llm.md",
  "./content/nlp_llm/04_finetuning_and_lora.md",
  "./content/nlp_llm/05_generation_and_summarization.md",
  "./content/nlp_llm/06_rag.md",
  "./content/nlp_llm/07_agents_and_economics.md",
  "./content/production/01_handbook.md",
  "./content/python/01_handbook.md",
  "./content/recsys/01_handbook.md",
  "./content/statistics/01_handbook.md",
  "./index.html",
  "./site.webmanifest"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
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
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") {
    return;
  }

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) {
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(fetch(request).catch(() => caches.match("./index.html")));
    return;
  }

  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== "basic") {
          return networkResponse;
        }

        const responseClone = networkResponse.clone();
        event.waitUntil(
          caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone))
        );
        return networkResponse;
      });
    })
  );
});
