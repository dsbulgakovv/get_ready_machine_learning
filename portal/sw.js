const CACHE_NAME = "ml-portal-6d92603a05bd";
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
  "./mlsd/manifest.json",
  "./mlsd/notes/01_universal_answer_flow.md",
  "./mlsd/notes/02_metric_tree.md",
  "./mlsd/notes/03_domain_decision_map.md",
  "./mlsd/notes/04_production_architecture.md",
  "./mlsd/notes/05_team_and_lead_ownership.md",
  "./mlsd/notes/06_sixty_minute_timeline.md",
  "./mlsd/notes/07_validation_and_ab_flow.md",
  "./mlsd/notes/08_senior_answer_loop.md",
  "./mlsd/notes/09_interview_quick_reference.md",
  "./mlsd/uml/01_universal_answer_flow.uml",
  "./mlsd/uml/02_metric_tree.uml",
  "./mlsd/uml/03_domain_decision_map.uml",
  "./mlsd/uml/04_production_architecture.uml",
  "./mlsd/uml/05_team_and_lead_ownership.uml",
  "./mlsd/uml/06_sixty_minute_timeline.uml",
  "./mlsd/uml/07_validation_and_ab_flow.uml",
  "./mlsd/uml/08_senior_answer_loop.uml",
  "./mlsd/uml/09_interview_quick_reference.uml",
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
