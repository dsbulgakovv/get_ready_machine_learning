# Production ML Architecture

## Как читать схему
End-to-end production контур: ingestion, feature engineering, training, registry, batch/online/hybrid serving, experiments, monitoring и feedback loop.

## Что проговорить на интервью
- Разделяй offline training path и online serving path: они используют разные SLA, storage и проверки качества.
- Batch scoring хорош, когда решение не требует миллисекундной свежести; online нужен для интерактивного продукта; hybrid сочетает тяжелые precomputed candidates и легкий reranking.
- Feature store снижает риск train-serving skew, но не отменяет проверку freshness, backfill и совместимость схем.
- Model registry нужен для versioning, approval, reproducibility и rollback.
- Monitoring должен покрывать data, model, business и system уровни, иначе деградация будет обнаружена слишком поздно.

## Термины и короткие пояснения

### Batch scoring
Периодический расчет предсказаний заранее, например hourly/daily. Дешевле и проще, но менее свежо.

### Online inference
Скоринг в момент запроса пользователя через API/model serving. Требует низкой latency, fallback и надежных online features.

### Model registry
Хранилище версий моделей с метаданными, метриками, артефактами, стадиями approval и возможностью rollback.

## Быстрый ответ
Я бы описал два контура: данные и обучение offline, затем serving как batch, online или hybrid. После этого добавил бы experiment layer, monitoring, feedback loop и rollback.

## Файл диаграммы
`uml/04_production_architecture.uml`
