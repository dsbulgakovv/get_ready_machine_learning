# Interview Quick Reference

## Как читать схему
Одностраничная шпаргалка с полной последовательностью ответа и подсказками справа: что уточнить, какие метрики назвать, как перейти к production и lead ownership.

## Что проговорить на интервью
- Эту диаграмму можно использовать как последний прогон перед интервью: она напоминает полный порядок без деталей.
- В каждом блоке нужно назвать 2-3 конкретики, а не говорить общими словами: например latency p95, PR-AUC, label delay, rollback criteria.
- Формулировка baseline → advanced approach показывает зрелость: ты не прыгаешь сразу в сложную модель.
- Production должен звучать прикладно: batch/online/hybrid, API, cache, DB, Kafka, feature store, monitoring.
- Lead ownership в конце закрепляет seniority: owners, risks, design review, lean team и связь с business metric.

## Термины и короткие пояснения

### Label delay
Задержка появления таргета после события. Например churn или default может стать известен через недели, что влияет на training data и мониторинг.

### Expected profit
Business-aware offline proxy, где TP/FP/FN/TN имеют разную денежную ценность. Лучше простой accuracy, если цена ошибок различается.

### Decision engine
Слой после модели, который применяет thresholds, business rules, constraints, fallback и иногда human-review routing.

## Быстрый ответ
Я бы шел по этой странице сверху вниз и в каждом блоке давал конкретный пример: metric, data risk, baseline, serving mode, validation check, rollout и owner.

## Файл диаграммы
`uml/09_interview_quick_reference.uml`
