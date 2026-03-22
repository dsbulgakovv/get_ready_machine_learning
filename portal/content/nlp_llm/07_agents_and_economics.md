# NLP / LLM: агенты и экономика

> Study-версия модуля: сначала учебная часть, потом все точные вопросы из ноутбука в конце модуля.

В этом модуле собраны оркестрация, multi-agent patterns, tools и экономическая сторона LLM-систем. Эти темы хорошо учатся вместе, потому что обе уже находятся на уровне системы, а не отдельной модели.

## Учебник

### AI Agents

Агент — это система, где LLM не просто выдаёт текст, а умеет планировать, вызывать инструменты и использовать наблюдения из внешнего мира для достижения цели.

Типичный цикл:

1. получить цель;
2. спланировать шаг;
3. выбрать tool или действие;
4. получить observation;
5. обновить состояние;
6. повторять до завершения.

Это и есть базовый reasoning loop: thought -> action -> observation. Он лежит в основе паттернов Act/ReAct.

- чистое реагирование;
- планирование;
- рефлексия и самопроверка;
- decomposition на подзадачи;
- вызов внешних инструментов.

### Экономическая целесообразность

Нужно сравнить:

- объём запросов;
- latency;
- требования к качеству;
- privacy / compliance;
- стоимость токенов;
- стоимость GPU/инженерной поддержки;
- риск vendor lock-in.

Примерно:

$$
\text{Cost}_{API} = N_{\text{in}} \cdot p_{\text{in}} + N_{\text{out}} \cdot p_{\text{out}}
$$

где \(N_{\text{in}}, N_{\text{out}}\) — число входных и выходных токенов, \(p\) — цена за токен.

Нужно учитывать:

- GPU/CPU;
- storage;
- orchestration;
- разработку и поддержку;
- MLOps/monitoring;
- время инженеров;
- простой и резервирование.

Грубо:

$$
\text{Cost}_{self} = \text{infra} + \text{ops} + \text{engineering} + \text{downtime risk}
$$

## Вопросы из ноутбука

### AI Agents

<details>
<summary>Что такое Агенты? Как работает? Какие основные шаги работы?</summary>

Агент — это система, где LLM не просто выдаёт текст, а умеет планировать, вызывать инструменты и использовать наблюдения из внешнего мира для достижения цели.

Типичный цикл:

1. получить цель;
2. спланировать шаг;
3. выбрать tool или действие;
4. получить observation;
5. обновить состояние;
6. повторять до завершения.

</details>

<details>
<summary>Как построить multi-agent систему? (бейзлайн решение)</summary>

Базовый вариант:

1. один supervisor/router;
2. несколько специализированных worker-агентов;
3. shared memory или state store;
4. правила handoff между агентами;
5. мониторинг и fallback.

</details>

<details>
<summary>Знаешь ли паттерны типа React/Act?</summary>

- `Act`: выбрать действие.
- `ReAct`: чередовать reasoning и action.
- `Reflexion`: после шага оценивать себя и корректировать стратегию.
- `Planning`: сначала строить план.
- `Planning + ReAct + Reflect`: комбинировать планирование, tool use и самопроверку.

</details>

<details>
<summary>Какие типы мышлений у Агента есть?</summary>

- чистое реагирование;
- планирование;
- рефлексия и самопроверка;
- decomposition на подзадачи;
- вызов внешних инструментов.

</details>

<details>
<summary>Какой обычно цикл работы у агента? (Мысль → Действие → Наблюдение)</summary>

Это и есть базовый reasoning loop: thought -> action -> observation. Он лежит в основе паттернов Act/ReAct.

</details>

<details>
<summary>Что такое tools в агентах?</summary>

Tools — это функции, API, базы, поисковые движки, интерпретаторы кода, браузер, калькулятор и т.д., которые LLM может вызывать.

</details>

<details>
<summary>Какие tools бывают?</summary>

Tools — это функции, API, базы, поисковые движки, интерпретаторы кода, браузер, калькулятор и т.д., которые LLM может вызывать.

</details>

<details>
<summary>Как мы задаём tools в агентах?</summary>

Обычно через schema: имя, описание, аргументы, типы полей. Модель генерирует структурированный вызов, оркестратор исполняет функцию и возвращает observation.

</details>

<details>
<summary>Как мы вызываем tools агентом?</summary>

Обычно через schema: имя, описание, аргументы, типы полей. Модель генерирует структурированный вызов, оркестратор исполняет функцию и возвращает observation.

</details>

<details>
<summary>Что такое structured output? Зачем нужен? Для чего ещё можем использовать кроме tools?</summary>

Чтобы получить контролируемый формат. Кроме tools, structured output полезен для:

- извлечения сущностей;
- классификации;
- маршрутизации запросов;
- заполнения объектов для downstream-систем.

</details>

<details>
<summary>Что такое Shared Memory?</summary>

Это общее состояние, доступное нескольким агентам или шагам. Там могут храниться план, промежуточные результаты, history, контекст пользователя.

</details>

<details>
<summary>Какие паттерны создания агентов знаешь?</summary>

- `Act`: выбрать действие.
- `ReAct`: чередовать reasoning и action.
- `Reflexion`: после шага оценивать себя и корректировать стратегию.
- `Planning`: сначала строить план.
- `Planning + ReAct + Reflect`: комбинировать планирование, tool use и самопроверку.

</details>

<details>
<summary>Act</summary>

- `Act`: выбрать действие.
- `ReAct`: чередовать reasoning и action.
- `Reflexion`: после шага оценивать себя и корректировать стратегию.
- `Planning`: сначала строить план.
- `Planning + ReAct + Reflect`: комбинировать планирование, tool use и самопроверку.

</details>

<details>
<summary>ReAct</summary>

- `Act`: выбрать действие.
- `ReAct`: чередовать reasoning и action.
- `Reflexion`: после шага оценивать себя и корректировать стратегию.
- `Planning`: сначала строить план.
- `Planning + ReAct + Reflect`: комбинировать планирование, tool use и самопроверку.

</details>

<details>
<summary>Reflixion</summary>

- `Act`: выбрать действие.
- `ReAct`: чередовать reasoning и action.
- `Reflexion`: после шага оценивать себя и корректировать стратегию.
- `Planning`: сначала строить план.
- `Planning + ReAct + Reflect`: комбинировать планирование, tool use и самопроверку.

</details>

<details>
<summary>Planing</summary>

- `Act`: выбрать действие.
- `ReAct`: чередовать reasoning и action.
- `Reflexion`: после шага оценивать себя и корректировать стратегию.
- `Planning`: сначала строить план.
- `Planning + ReAct + Reflect`: комбинировать планирование, tool use и самопроверку.

</details>

<details>
<summary>Planing + ReAct + Reflect</summary>

- `Act`: выбрать действие.
- `ReAct`: чередовать reasoning и action.
- `Reflexion`: после шага оценивать себя и корректировать стратегию.
- `Planning`: сначала строить план.
- `Planning + ReAct + Reflect`: комбинировать планирование, tool use и самопроверку.

</details>

<details>
<summary>Что такое MCP? Для чего он нужен?</summary>

MCP — протокол для стандартизированного доступа модели/агента к инструментам и внешним ресурсам. Он делает интеграцию tools более унифицированной.

</details>

<details>
<summary>Какие виды Multi Agent system знаешь?</summary>

- `Sequential`: агенты работают по цепочке.
- `Hierarchical`: supervisor + workers.
- `Parallel`: несколько агентов делают независимые части одновременно.
- `Async`: агенты не блокируют друг друга по времени.
- `Graph`: свободный граф переходов между узлами.
- `Hybrid`: смесь нескольких схем.

</details>

<details>
<summary>Sequential</summary>

- `Sequential`: агенты работают по цепочке.
- `Hierarchical`: supervisor + workers.
- `Parallel`: несколько агентов делают независимые части одновременно.
- `Async`: агенты не блокируют друг друга по времени.
- `Graph`: свободный граф переходов между узлами.
- `Hybrid`: смесь нескольких схем.

</details>

<details>
<summary>Hierarchical</summary>

- `Sequential`: агенты работают по цепочке.
- `Hierarchical`: supervisor + workers.
- `Parallel`: несколько агентов делают независимые части одновременно.
- `Async`: агенты не блокируют друг друга по времени.
- `Graph`: свободный граф переходов между узлами.
- `Hybrid`: смесь нескольких схем.

</details>

<details>
<summary>Hybrid</summary>

- `Sequential`: агенты работают по цепочке.
- `Hierarchical`: supervisor + workers.
- `Parallel`: несколько агентов делают независимые части одновременно.
- `Async`: агенты не блокируют друг друга по времени.
- `Graph`: свободный граф переходов между узлами.
- `Hybrid`: смесь нескольких схем.

</details>

<details>
<summary>Parallel</summary>

- `Sequential`: агенты работают по цепочке.
- `Hierarchical`: supervisor + workers.
- `Parallel`: несколько агентов делают независимые части одновременно.
- `Async`: агенты не блокируют друг друга по времени.
- `Graph`: свободный граф переходов между узлами.
- `Hybrid`: смесь нескольких схем.

</details>

<details>
<summary>Async</summary>

- `Sequential`: агенты работают по цепочке.
- `Hierarchical`: supervisor + workers.
- `Parallel`: несколько агентов делают независимые части одновременно.
- `Async`: агенты не блокируют друг друга по времени.
- `Graph`: свободный граф переходов между узлами.
- `Hybrid`: смесь нескольких схем.

</details>

<details>
<summary>Graph</summary>

- `Sequential`: агенты работают по цепочке.
- `Hierarchical`: supervisor + workers.
- `Parallel`: несколько агентов делают независимые части одновременно.
- `Async`: агенты не блокируют друг друга по времени.
- `Graph`: свободный граф переходов между узлами.
- `Hybrid`: смесь нескольких схем.

</details>

<details>
<summary>Какие бибилиотеки для создания агентов знаешь? Какими пользовался?</summary>

Да, это частые примеры:

- `LangGraph`;
- `smolagents`;
- `CrewAI`.

На интервью важно не только назвать библиотеку, но и объяснить её место: orchestration, graph state, tools, memory, multi-agent patterns.

</details>

<details>
<summary>LangGraph</summary>

Да, это частые примеры:

- `LangGraph`;
- `smolagents`;
- `CrewAI`.

На интервью важно не только назвать библиотеку, но и объяснить её место: orchestration, graph state, tools, memory, multi-agent patterns.

</details>

<details>
<summary>smolagents</summary>

Да, это частые примеры:

- `LangGraph`;
- `smolagents`;
- `CrewAI`.

На интервью важно не только назвать библиотеку, но и объяснить её место: orchestration, graph state, tools, memory, multi-agent patterns.

</details>

<details>
<summary>LangGraph</summary>

Да, это частые примеры:

- `LangGraph`;
- `smolagents`;
- `CrewAI`.

На интервью важно не только назвать библиотеку, но и объяснить её место: orchestration, graph state, tools, memory, multi-agent patterns.

</details>

<details>
<summary>Crew AI</summary>

Да, это частые примеры:

- `LangGraph`;
- `smolagents`;
- `CrewAI`.

На интервью важно не только назвать библиотеку, но и объяснить её место: orchestration, graph state, tools, memory, multi-agent patterns.

</details>

### Экономическая целесообразность

<details>
<summary>Как оценить, что выгоднее — использовать API LLM или развернуть свою модель?</summary>

Нужно сравнить:

- объём запросов;
- latency;
- требования к качеству;
- privacy / compliance;
- стоимость токенов;
- стоимость GPU/инженерной поддержки;
- риск vendor lock-in.

</details>

<details>
<summary>Как посчитать стоимость при использовании API?</summary>

Примерно:

$$
\text{Cost}_{API} = N_{\text{in}} \cdot p_{\text{in}} + N_{\text{out}} \cdot p_{\text{out}}
$$

где \(N_{\text{in}}, N_{\text{out}}\) — число входных и выходных токенов, \(p\) — цена за токен.

</details>

<details>
<summary>Как посчитать стоимость при разворачивании своей модели?</summary>

Нужно учитывать:

- GPU/CPU;
- storage;
- orchestration;
- разработку и поддержку;
- MLOps/monitoring;
- время инженеров;
- простой и резервирование.

Грубо:

$$
\text{Cost}_{self} = \text{infra} + \text{ops} + \text{engineering} + \text{downtime risk}
$$

</details>

<details>
<summary>В какой момент выгоднее перейти на собственный сервер?</summary>

Когда:

- объём трафика стабильно большой;
- API-стоимость превышает владение собственной инфраструктурой;
- требования по privacy или latency не закрываются внешним API;
- команда готова поддерживать inference stack.

</details>
