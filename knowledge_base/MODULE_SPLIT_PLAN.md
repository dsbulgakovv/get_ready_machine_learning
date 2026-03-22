# План Дробления Модулей

Это не обязательный рефактор прямо сейчас, а рекомендуемое следующее улучшение структуры, если мы захотим сделать пособие ещё удобнее для запоминания и будущего knowledge portal.

## Уже хорошо как есть

- `classic_ml/01_models.md`
- `recsys/01_handbook.md`
- `deep_learning/01_core.md`
- `cv/01_handbook.md`
- `metrics/01_handbook.md`
- `databases/01_handbook.md`
- `production/01_handbook.md`
- `statistics/01_handbook.md`

Их можно пока оставить крупными модулями.

## Стоит дробить в первую очередь

### `classic_ml/02_advanced.md`

Лучше разрезать на:

- `ensembles.md`
- `clustering_dim_reduction.md`
- `anomaly_detection.md`
- `ml_fundamentals.md`

Причина: сейчас в одном файле живут слишком разные типы мышления.

### `nlp_llm/01_handbook.md`

Лучше разрезать на:

- `text_representation_and_tokenization.md`
- `transformers_core.md`
- `llm_inference_and_prompting.md`
- `fine_tuning_and_lora.md`
- `generation_and_summarization.md`
- `rag.md`
- `agents.md`
- `llm_economics.md`

Причина: это самый перегруженный модуль, и именно он сильнее всего мешает повторению.

### `python/01_handbook.md`

Лучше разрезать на:

- `python_core.md`
- `oop_iterators_generators.md`
- `async_threads_processes.md`
- `coding_patterns.md`

Причина: язык, concurrency и задачки лучше учатся отдельно.

## Можно дробить позже

### `classic_ml/01_models.md`

Если понадобится ещё более “карточный” режим:

- `linear_regression.md`
- `logistic_regression.md`
- `svm.md`
- `knn.md`
- `decision_trees.md`

### `metrics/01_handbook.md`

Позже можно разнести на:

- `classification_metrics.md`
- `ranking_metrics.md`
- `cv_metrics.md`
- `nlp_metrics.md`

## Практический приоритет

Если делать по пользе для запоминания, я бы шёл так:

1. `nlp_llm/01_handbook.md`
2. `classic_ml/02_advanced.md`
3. `python/01_handbook.md`
4. `metrics/01_handbook.md`
5. всё остальное оставить как есть
