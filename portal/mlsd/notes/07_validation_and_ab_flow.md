# Model Validation and A/B Test Flow

## Как читать схему
Путь от offline validation до решения ship/iterate/rollback: корректный split, метрики, segment analysis, shadow/A-A, дизайн A/B, SRM и rollout.

## Что проговорить на интервью
- Offline split должен соответствовать реальному будущему использованию: time-based, user-based или group-based, без leakage.
- Кроме ML-метрик нужно считать business proxy и segment analysis, иначе среднее качество может скрыть деградацию важных сегментов.
- Перед A/B проверь logging, shadow mode, A/A или pre-period balance, особенно для online decisions.
- В дизайне A/B назови hypothesis, primary metric, guardrails, unit of randomization, MDE, duration и stopping rules.
- Ship происходит постепенно: rollout процентами с rollback criteria, а не мгновенный full launch.

## Термины и короткие пояснения

### Unit of randomization
Единица, на которой делится эксперимент: user, session, seller, geo, courier или time bucket. Неверный выбор вызывает contamination.

### Practical significance
Эффект достаточно большой, чтобы иметь бизнес-смысл после учета стоимости, риска и операционной сложности.

### Segment stability
Проверка, что выигрыш не куплен сильной деградацией по регионам, устройствам, категориям, новым пользователям или high-value cohorts.

## Быстрый ответ
Я бы не запускал модель только по offline metric. Сначала корректный split и segment analysis, потом shadow/A-A/logging checks, затем A/B с guardrails и постепенный rollout.

## Файл диаграммы
`uml/07_validation_and_ab_flow.uml`
