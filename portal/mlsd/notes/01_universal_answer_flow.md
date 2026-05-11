# Universal ML System Design Answer Flow

## Как читать схему
Главная карта ответа на ML System Design: от уточнения бизнес-цели до production, A/B, мониторинга и ownership. Ее удобно держать как скелет любого часового ответа.

## Что проговорить на интервью
- Начинай не с модели, а с цели, пользователя, цены ошибки и ограничений по latency, privacy, cost и explainability.
- Связывай business metric, product proxy, ML metric и guardrails, чтобы интервьюер видел причинную цепочку.
- Baseline нужен как быстрая проверка гипотезы и нижняя планка, advanced model стоит предлагать только после понимания данных и ROI.
- Production часть должна включать serving mode, feature availability, fallback, monitoring, rollout и rollback.
- В конце проговаривай, кто чем владеет: analytics, data, ML, backend, MLOps, QA/risk.

## Термины и короткие пояснения

### North Star metric
Главная бизнес-метрика продукта или инициативы: revenue, GMV, margin, retention, SLA или cost reduction. Она объясняет, ради чего вообще строится ML-система.

### Guardrail metrics
Метрики, которые не должны ухудшиться при росте основной метрики: latency, error rate, complaint rate, fairness, infra cost, long-term retention.

### Train-serving skew
Расхождение между тем, как фичи считаются на train, и тем, как они доступны в production. Частая причина сильного падения качества после запуска.

## Быстрый ответ
Я бы вел ответ по цепочке Business → Metrics → Data → Model → Validation → Production → A/B → Monitoring → Team. Так я показываю, что дизайн системы начинается с impact, а модель является только одним из компонентов решения.

## Файл диаграммы
`uml/01_universal_answer_flow.uml`
