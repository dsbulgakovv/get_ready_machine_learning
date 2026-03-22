# NLP / LLM: генерация и суммаризация

> Study-версия модуля: сначала учебная часть, потом все точные вопросы из ноутбука в конце модуля.

Суммаризация и управляемая генерация лучше запоминаются отдельным модулем: здесь полезно держать в голове и training pipeline, и decoding, и ограничения автоматических метрик.

## Учебник

### Суммаризация и генерация

Нужно:

1. собрать пары `документ -> summary`;
2. очистить и нормализовать данные;
3. выбрать метрики;
4. обучить seq2seq или decoder-only модель;
5. валидировать не только по ROUGE, но и по factuality.

Полезно явно добавить выбор постановки:

- `extractive`, если важна максимальная опора на текст;
- `abstractive`, если нужен более естественный пересказ;
- long-document summarization с chunking/hierarchical strategy для длинных входов.

- extractive summarization;
- TextRank;
- sentence ranking по TF-IDF/BM25;
- классические seq2seq модели меньшего масштаба.

Через instruction tuning или supervised fine-tuning на парах `текст -> краткое описание`. Важно контролировать hallucinations.

## Вопросы из ноутбука

### Суммаризация и генерация

<details>
<summary>Как строить pipeline обучения суммаризации?</summary>

Нужно:

1. собрать пары `документ -> summary`;
2. очистить и нормализовать данные;
3. выбрать метрики;
4. обучить seq2seq или decoder-only модель;
5. валидировать не только по ROUGE, но и по factuality.

Полезно явно добавить выбор постановки:

- `extractive`, если важна максимальная опора на текст;
- `abstractive`, если нужен более естественный пересказ;
- long-document summarization с chunking/hierarchical strategy для длинных входов.

</details>

<details>
<summary>Как сделать суммаризацию без LLM?</summary>

- extractive summarization;
- TextRank;
- sentence ranking по TF-IDF/BM25;
- классические seq2seq модели меньшего масштаба.

</details>

<details>
<summary>Как обучать суммаризацию с LLM?</summary>

Через instruction tuning или supervised fine-tuning на парах `текст -> краткое описание`. Важно контролировать hallucinations.

</details>

<details>
<summary>Как дообучать модель с помощью LoRA?</summary>

Замораживаем базовую модель, добавляем low-rank adapters, учим только их.

</details>

<details>
<summary>Как готовить pretrain?</summary>

Нужны:

- большой чистый корпус;
- deduplication;
- фильтрация токсичности/шума;
- правильная смесь доменов;
- tokenizer и curriculum;
- инфраструктура для масштабного обучения.

</details>

<details>
<summary>Как влиять на генерацию ответа при инференсе LLM?</summary>

- `Temperature`: влияет на случайность;
- `Beam search`: ищет более вероятную последовательность, хорош для задач с чёткой целью, но не всегда для open-ended dialogue;
- `Prompt engineering`: меняет постановку задачи;
- `Structured output`: ограничивает формат.

</details>

<details>
<summary>Температура.</summary>

- `Temperature`: влияет на случайность;
- `Beam search`: ищет более вероятную последовательность, хорош для задач с чёткой целью, но не всегда для open-ended dialogue;
- `Prompt engineering`: меняет постановку задачи;
- `Structured output`: ограничивает формат.

</details>

<details>
<summary>Beam-search.</summary>

- `Temperature`: влияет на случайность;
- `Beam search`: ищет более вероятную последовательность, хорош для задач с чёткой целью, но не всегда для open-ended dialogue;
- `Prompt engineering`: меняет постановку задачи;
- `Structured output`: ограничивает формат.

</details>

<details>
<summary>Prompt engineering.</summary>

- `Temperature`: влияет на случайность;
- `Beam search`: ищет более вероятную последовательность, хорош для задач с чёткой целью, но не всегда для open-ended dialogue;
- `Prompt engineering`: меняет постановку задачи;
- `Structured output`: ограничивает формат.

</details>

<details>
<summary>Structured output (наивный и продвинутый варианты).</summary>

- `Temperature`: влияет на случайность;
- `Beam search`: ищет более вероятную последовательность, хорош для задач с чёткой целью, но не всегда для open-ended dialogue;
- `Prompt engineering`: меняет постановку задачи;
- `Structured output`: ограничивает формат.

</details>
