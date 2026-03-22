# NLP / LLM: инференс, prompting и общая картина LLM

> Study-версия модуля: сначала учебная часть, потом все точные вопросы из ноутбука в конце модуля.

Это модуль про использование LLM на практике: как модель генерирует, как ею управлять через prompting и structured output, и как понимать базовую картину decoder-only систем.

## Учебник

### Инференс и декодирование

- greedy decoding;
- beam search;
- top-k sampling;
- top-p / nucleus sampling;
- temperature sampling;
- repetition penalty;
- constrained decoding.

Полезная собеседовательная оговорка:

- `greedy` и `beam search` больше подходят, когда нужен "самый вероятный" ответ;
- `top-k`, `top-p`, `temperature` — когда нужен управляемый stochastic decoding;
- constrained decoding — когда важен строгий формат или grammar.

Это не равновероятный выбор из словаря. Модель выдаёт распределение вероятностей по следующему токену, и токен сэмплируется из этого распределения после возможных трансформаций вроде temperature и top-k.

Выходные токены дороже. Вход обрабатывается одним проходом по уже известной последовательности, а генерация требует автрорегрессионного шага для каждого нового токена.

### Метрики и базовый анализ NLP-моделей

Для бинарной классификации:

$$
\mathrm{Precision} = \frac{TP}{TP+FP}
$$

$$
\mathrm{Recall} = \frac{TP}{TP+FN}
$$

$$
F_1 = 2 \cdot \frac{\mathrm{Precision}\cdot \mathrm{Recall}}{\mathrm{Precision}+\mathrm{Recall}}
$$

`Macro` усредняет метрику по классам, `Micro` считает глобальные TP/FP/FN по всем классам сразу.

ROC строится по TPR/FPR при изменении порога. Для случайной модели ROC-AUC примерно равен \(0.5\).

PR-AUC, F1, recall, precision, macro-F1, balanced accuracy. Выбор зависит от цены ошибок.

### LLM как инструмент

Нужно перевести задачу в корректный prompt с чётким форматом выхода и критериями. Например:

`Определи, содержит ли текст токсичность. Ответь только YES или NO.`

То есть LLM можно использовать как универсальный conditional model, если правильно задать инструкцию.

- явно описать формат;
- дать few-shot примеры;
- использовать structured output / JSON schema;
- частично "подсказать" начало ответа;
- ограничить decoding.

- `Temperature`: сглаживает или заостряет распределение logits.
- `top_k`: оставляет только \(k\) наиболее вероятных токенов.

Формально temperature действует так:

$$
p_i = \mathrm{softmax}\left(\frac{z_i}{T}\right)
$$

Где \(T < 1\) делает распределение более острым, а \(T > 1\) — более плоским.

Низкая temperature и маленький `top_k` делают ответ более детерминированным. Высокая temperature без ограничений резко повышает риск мусора и галлюцинаций.

### Prompting и structured output

- zero-shot instruction;
- few-shot;
- chain-of-thought по необходимости;
- self-consistency;
- role/system prompting;
- retrieval-augmented prompting;
- tool-use prompting.

На интервью полезно добавить, когда что уместно:

- `few-shot` — когда формат или reasoning pattern нестандартный;
- `structured prompting` — когда ответ должен идти в схему;
- `tool prompting` — когда знание нужно вынести наружу;
- `RAG prompting` — когда нельзя полагаться на параметры модели.

Чтобы ответ был машинно читаемым и предсказуемым: JSON, schema, function call. Это важно для интеграции модели в сервисы и пайплайны.

Не любая и не всегда. Она может с высокой вероятностью следовать шаблону, если её хорошо проинструктировать, но гарантии без constrained decoding нет.

### LLM: общая картина

Трансформер — архитектурный шаблон на attention и FFN. Encoder-only решает задачи понимания, decoder-only — генерации, encoder-decoder — seq2seq.

См. раздел выше: токенизация переводит текст в токены; BPE жадно сливает частые пары.

Токены -> embeddings -> positional information -> стек attention/FFN-блоков -> выходные скрытые состояния -> logits или downstream head.

## Вопросы из ноутбука

### Инференс

<details>
<summary>Какие есть варианты сэмплирования на инференсе?</summary>

- greedy decoding;
- beam search;
- top-k sampling;
- top-p / nucleus sampling;
- temperature sampling;
- repetition penalty;
- constrained decoding.

Полезная собеседовательная оговорка:

- `greedy` и `beam search` больше подходят, когда нужен "самый вероятный" ответ;
- `top-k`, `top-p`, `temperature` — когда нужен управляемый stochastic decoding;
- constrained decoding — когда важен строгий формат или grammar.

</details>

<details>
<summary>Что значит “выбираем случайный токен”?</summary>

Это не равновероятный выбор из словаря. Модель выдаёт распределение вероятностей по следующему токену, и токен сэмплируется из этого распределения после возможных трансформаций вроде temperature и top-k.

</details>

<details>
<summary>Какие токены для модели дороже — на входе или на выходе?</summary>

Выходные токены дороже. Вход обрабатывается одним проходом по уже известной последовательности, а генерация требует автрорегрессионного шага для каждого нового токена.

</details>

<details>
<summary>Почему генерация токенов дороже, чем обработка входной последовательности?</summary>

Потому что выход строится последовательно: чтобы сгенерировать токен \(t+1\), нужно сначала сгенерировать \(t\). Это ограничивает распараллеливание.

</details>

### Метрики и анализ моделей NLP

<details>
<summary>Какие метрики классификации существуют? Формулы Precision, Recall, F1, макро- и микро-усреднение</summary>

Для бинарной классификации:

$$
\mathrm{Precision} = \frac{TP}{TP+FP}
$$

$$
\mathrm{Recall} = \frac{TP}{TP+FN}
$$

$$
F_1 = 2 \cdot \frac{\mathrm{Precision}\cdot \mathrm{Recall}}{\mathrm{Precision}+\mathrm{Recall}}
$$

`Macro` усредняет метрику по классам, `Micro` считает глобальные TP/FP/FN по всем классам сразу.

</details>

<details>
<summary>Как строится ROC-AUC и какой результат будет для случайных данных?</summary>

ROC строится по TPR/FPR при изменении порога. Для случайной модели ROC-AUC примерно равен \(0.5\).

</details>

<details>
<summary>Какие метрики устойчивы к дисбалансу классов?</summary>

PR-AUC, F1, recall, precision, macro-F1, balanced accuracy. Выбор зависит от цены ошибок.

</details>

### Задачи для LLM

<details>
<summary>Как заставить LLM выполнять любую задачу, допустим задачу классификации?</summary>

Нужно перевести задачу в корректный prompt с чётким форматом выхода и критериями. Например:

`Определи, содержит ли текст токсичность. Ответь только YES или NO.`

То есть LLM можно использовать как универсальный conditional model, если правильно задать инструкцию.

</details>

<details>
<summary>Пример: задать правильный промпт ("Есть ли мат в данном предложении {предложение}? Ответь да или нет")</summary>

Нужно перевести задачу в корректный prompt с чётким форматом выхода и критериями. Например:

`Определи, содержит ли текст токсичность. Ответь только YES или NO.`

То есть LLM можно использовать как универсальный conditional model, если правильно задать инструкцию.

</details>

<details>
<summary>Как можно заставить модель генерировать по шаблону текст?</summary>

- явно описать формат;
- дать few-shot примеры;
- использовать structured output / JSON schema;
- частично "подсказать" начало ответа;
- ограничить decoding.

</details>

<details>
<summary>Задать промпт с правилом.</summary>

Нужно перевести задачу в корректный prompt с чётким форматом выхода и критериями. Например:

`Определи, содержит ли текст токсичность. Ответь только YES или NO.`

То есть LLM можно использовать как универсальный conditional model, если правильно задать инструкцию.

</details>

<details>
<summary>Поиграться с параметрами top_k и temperature.</summary>

- `Temperature`: сглаживает или заостряет распределение logits.
- `top_k`: оставляет только \(k\) наиболее вероятных токенов.

Формально temperature действует так:

$$
p_i = \mathrm{softmax}\left(\frac{z_i}{T}\right)
$$

Где \(T < 1\) делает распределение более острым, а \(T > 1\) — более плоским.

Низкая temperature и маленький `top_k` делают ответ более детерминированным. Высокая temperature без ограничений резко повышает риск мусора и галлюцинаций.

</details>

<details>
<summary>Во время генерации подсунуть токены модели (например, “json generation: {”).</summary>

Да, это нормальный приём. Префикс или forced prefix снижает энтропию начала ответа и помогает модели зайти в нужный формат.

</details>

<details>
<summary>Как оценить уверенность модели в своём ответе (лосс-функция, распределение логитов)?</summary>

Можно смотреть:

- log-probability токенов;
- разницу между top-1 и top-2 логитами;
- sequence log-likelihood;
- self-consistency между несколькими сэмплами;
- калибровку на валидации.

Важно: высокая локальная уверенность по токенам не гарантирует фактическую корректность ответа.

На собеседовании полезно проговорить distinction:

- `model confidence` — насколько модель уверена в своей следующей токеновой последовательности;
- `factual correctness` — верно ли содержание относительно мира или контекста.

Это не одно и то же.

</details>

### Prompting и structured output

<details>
<summary>Какие паттерны prompting ты используешь?</summary>

- zero-shot instruction;
- few-shot;
- chain-of-thought по необходимости;
- self-consistency;
- role/system prompting;
- retrieval-augmented prompting;
- tool-use prompting.

На интервью полезно добавить, когда что уместно:

- `few-shot` — когда формат или reasoning pattern нестандартный;
- `structured prompting` — когда ответ должен идти в схему;
- `tool prompting` — когда знание нужно вынести наружу;
- `RAG prompting` — когда нельзя полагаться на параметры модели.

</details>

<details>
<summary>Зачем нужен structured output?</summary>

Чтобы ответ был машинно читаемым и предсказуемым: JSON, schema, function call. Это важно для интеграции модели в сервисы и пайплайны.

</details>

<details>
<summary>Почему любая LLM может выдавать корректный JSON на выход?</summary>

Не любая и не всегда. Она может с высокой вероятностью следовать шаблону, если её хорошо проинструктировать, но гарантии без constrained decoding нет.

</details>

<details>
<summary>Как можно ограничить выбор следующего токена, чтобы сохранить корректный формат?</summary>

- grammar-constrained decoding;
- JSON schema constrained generation;
- function calling;
- токен-фильтрация по валидным продолжениям автомата.

</details>

### LLM

<details>
<summary>Что такое трансформер, encoder-only, decoder-only?</summary>

Трансформер — архитектурный шаблон на attention и FFN. Encoder-only решает задачи понимания, decoder-only — генерации, encoder-decoder — seq2seq.

</details>

<details>
<summary>Что такое токенизация (определение) и как работает BPE?</summary>

См. раздел выше: токенизация переводит текст в токены; BPE жадно сливает частые пары.

</details>

<details>
<summary>Как обрабатывается последовательность токенов в трансформере?</summary>

Токены -> embeddings -> positional information -> стек attention/FFN-блоков -> выходные скрытые состояния -> logits или downstream head.

</details>

<details>
<summary>Что такое positional encoding?</summary>

Positional encoding сообщает порядок. `RoPE` кодирует позицию вращением векторов \(Q\) и \(K\), что хорошо работает для относительных позиций и длинных контекстов.

</details>

<details>
<summary>Что такое RoPE?</summary>

Positional encoding сообщает порядок. `RoPE` кодирует позицию вращением векторов \(Q\) и \(K\), что хорошо работает для относительных позиций и длинных контекстов.

</details>

<details>
<summary>Что такое multi-head attention?</summary>

Потому что каждая голова имеет свои обучаемые проекции и может фокусироваться на разных паттернах: синтаксис, дальние зависимости, копирование, формат и т.д.

</details>

<details>
<summary>Почему attention’ы разные?</summary>

Потому что каждая голова имеет свои обучаемые проекции и может фокусироваться на разных паттернах: синтаксис, дальние зависимости, копирование, формат и т.д.

</details>

<details>
<summary>Какие задачи решаются encoder-only архитектурами?</summary>

Классификация, NER, извлечение признаков, retrieval-эмбеддинги, reranking, extractive QA.

</details>

<details>
<summary>Что такое LLM? Какие этапы обучения?</summary>

Обычно:

1. pretraining на больших корпусах;
2. instruction/SFT;
3. alignment-этапы;
4. optional domain tuning;
5. inference-time control через prompting/tools.

Если говорить современным языком, alignment-этапы могут включать:

- SFT;
- preference learning / DPO / RLHF / RLAIF;
- safety tuning;
- tool-use tuning.

</details>

<details>
<summary>Что такое SFT, LoRA, дистилляция, pruning?</summary>

- `SFT`: supervised fine-tuning.
- `LoRA`: параметрически дешёвый fine-tuning.
- `Дистилляция`: перенос поведения большой модели в меньшую.
- `Pruning`: удаление части параметров или структур ради ускорения/сжатия.

</details>

<details>
<summary>Как сделать так чтобы LLM решала математические задачи с максимальной точностью? (Function calling)</summary>

Лучше не заставлять её "считать в уме", а отдавать вычисления внешнему инструменту: калькулятору, CAS, Python. Function calling — это механизм, при котором модель выдаёт структурированный вызов инструмента, а не финальный текст.

</details>

<details>
<summary>Что такое Function calling?</summary>

Лучше не заставлять её "считать в уме", а отдавать вычисления внешнему инструменту: калькулятору, CAS, Python. Function calling — это механизм, при котором модель выдаёт структурированный вызов инструмента, а не финальный текст.

</details>
