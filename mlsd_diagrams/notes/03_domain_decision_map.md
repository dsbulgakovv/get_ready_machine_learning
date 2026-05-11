# Domain Decision Map

## Как читать схему
Карта выбора ML-подхода по типу задачи: classification, regression, ranking, recsys, forecasting, NLP/LLM, CV, optimization и fraud/anomaly detection.

## Что проговорить на интервью
- Сначала формулируй, что именно предсказываем или оптимизируем: вероятность, число, порядок, будущий спрос, действие, текст или изображение.
- Для каждого домена называй простой baseline и более сильную модель: SQL/rules/BM25/popularity перед CatBoost, LambdaMART, two-tower, transformer или LLM.
- Метрика должна совпадать с пользовательским действием: ranking оценивается top-K метриками, pricing - margin/revenue/retention, fraud - prevented loss при review capacity.
- Не забывай про систему вокруг модели: human review для high-risk, business rules для pricing, retrieval для RAG, fallback для online inference.
- Всегда возвращайся к бизнес-ценности и trade-off quality vs latency/cost/explainability.

## Термины и короткие пояснения

### Two-tower model
Архитектура для retrieval/recsys/search: одна башня кодирует пользователя или запрос, другая объект; близость embedding помогает быстро искать кандидатов.

### LambdaMART
Градиентный бустинг для learning-to-rank, который оптимизирует порядок объектов, а не независимое предсказание для каждого объекта.

### Uplift modeling
Моделирование инкрементального эффекта действия: кому пуш, скидка или звонок реально изменит поведение, а не просто совпадет с высокой склонностью купить.

## Быстрый ответ
Я бы сначала определил тип решения: событие, число, ranking, recommendation, forecast, NLP/CV или optimization. Затем предложил baseline, advanced approach, подходящую метрику и объяснил trade-offs.

## Файл диаграммы
`uml/03_domain_decision_map.uml`
