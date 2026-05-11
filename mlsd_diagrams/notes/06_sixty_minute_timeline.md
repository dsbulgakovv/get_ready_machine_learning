# 60-Minute Interview Answer Timeline

## Как читать схему
Тайминг часового MLSD ответа: сколько времени тратить на clarification, metrics, data/model, architecture, validation, team plan и final summary.

## Что проговорить на интервью
- Первые 5 минут нужны, чтобы не решать не ту задачу: уточнить пользователя, цель, constraints и цену ошибки.
- К 10-й минуте желательно зафиксировать business metric, product proxy, ML metric и guardrails.
- До середины интервью нужно успеть data/formulation/baseline/advanced model, иначе architecture будет висеть в воздухе.
- Production и validation нельзя оставлять на последние 2 минуты: это сильная часть senior/lead ответа.
- Финальная минута должна связать решение с business impact, risks и rollout.

## Термины и короткие пояснения

### MDE
Minimum Detectable Effect: минимальный эффект, который эксперимент способен статистически заметить при заданной мощности и размере выборки.

### SRM
Sample Ratio Mismatch: нарушение ожидаемых долей трафика в A/B. Часто указывает на баг в рандомизации или логировании.

### Shadow mode
Модель считает решения в production-потоке, но не влияет на пользователя. Нужен для проверки latency, логирования и стабильности.

## Быстрый ответ
Я бы управлял временем явно: 5 минут clarification, 5 минут metrics, 20 минут data/model, 10 минут architecture, 8 минут validation, 7 минут team/risk и 5 минут на summary.

## Файл диаграммы
`uml/06_sixty_minute_timeline.uml`
