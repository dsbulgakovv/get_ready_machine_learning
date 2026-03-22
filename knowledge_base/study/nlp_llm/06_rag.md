# NLP / LLM: RAG

> Study-версия модуля: сначала учебная часть, потом все точные вопросы из ноутбука в конце модуля.

RAG слишком объёмен для большого общего NLP-файла, поэтому этот модуль лучше учить отдельно: retrieval, reranking, chunking, evaluation и продуктовая архитектура.

## Учебник

### RAG

Retrieval-Augmented Generation — это система, где LLM отвечает не только из своих параметров, но и на основе найденного внешнего контекста.

Это компонент, который по запросу находит релевантные документы, чанки или объекты.

- `Sparse`: BM25, TF-IDF, exact term match.
- `Dense`: поиск по эмбеддингам.

Sparse лучше ловит точные совпадения терминов, dense — семантическую близость. На практике часто используют hybrid retrieval.

## Вопросы из ноутбука

### RAG

<details>
<summary>Что такое RAG?</summary>

Retrieval-Augmented Generation — это система, где LLM отвечает не только из своих параметров, но и на основе найденного внешнего контекста.

</details>

<details>
<summary>Что такое ретривер?</summary>

Это компонент, который по запросу находит релевантные документы, чанки или объекты.

</details>

<details>
<summary>Dense и Sparse Retrieval? В чём разница, зачем нужны?</summary>

- `Sparse`: BM25, TF-IDF, exact term match.
- `Dense`: поиск по эмбеддингам.

Sparse лучше ловит точные совпадения терминов, dense — семантическую близость. На практике часто используют hybrid retrieval.

</details>

<details>
<summary>Bi-Encoder и Cross-Encoder разница?</summary>

- `Bi-encoder`: быстро кодирует query и doc отдельно, хорошо для retrieval.
- `Cross-encoder`: кодирует пару совместно, медленно, но качественно. Часто используется как reranker.

</details>

<details>
<summary>Как мы обучаем эмбеддер?</summary>

Обычно на парах или триплетах:

- позитивы должны быть ближе;
- негативы — дальше.

Triplet loss:

$$
\mathcal{L} = \max(0, s(q, d^-) - s(q, d^+) + m)
$$

Где \(m\) — margin.

</details>

<details>
<summary>Метрики качества RAG?</summary>

Для retrieval:

- Recall@K;
- MRR;
- NDCG;
- HitRate@K.

Для итогового ответа:

- faithfulness;
- answer relevancy;
- answer precision/recall;
- human evaluation;
- task success rate.

</details>

<details>
<summary>Что такое Reranker? Какие бывают?</summary>

Это компонент, который пересортировывает найденные кандидаты более точной, но более тяжёлой моделью. Бывают cross-encoder reranker, LLM-reranker, hybrid reranker.

</details>

<details>
<summary>LLM-reranking что такое, как работает?</summary>

Это когда LLM оценивает релевантность кандидатов запросу и выстраивает порядок. Качество может быть высоким, но латентность и цена часто хуже, чем у специализированного cross-encoder.

</details>

<details>
<summary>Как проверить качество реранкера?</summary>

Сравнивать ranking-метрики до и после него: MRR, NDCG, Recall@K, Precision@K. И отдельно проверять end-to-end влияние на финальный ответ.

</details>

<details>
<summary>Hybrid Search</summary>

Это сочетание sparse и dense retrieval, например BM25 + эмбеддинги. Часто даёт лучший recall.

</details>

<details>
<summary>Multi-Query Search</summary>

Запрос переформулируется в несколько вариантов, и retrieval идёт по нескольким формулировкам. Это помогает покрыть синонимы и неоднозначности.

</details>

<details>
<summary>Chunking Strategies</summary>

Нужно выбрать размер чанка, overlap, логику разбиения по абзацам/заголовкам/смысловым блокам. Слишком мелкие чанки теряют контекст, слишком большие ухудшают retrieval.

</details>

<details>
<summary>RAGAS? Что такое зачем нужен, как работает?</summary>

Это фреймворк для оценки RAG-пайплайнов. Он использует набор метрик вроде faithfulness, answer relevancy и context precision/recall, иногда с помощью LLM-as-a-judge.

</details>

<details>
<summary>BERT, E5, T5. Разница, какой для чего</summary>

- `BERT`: encoder-only, хороший общий backbone для понимания.
- `E5`: family эмбеддеров, заточенных под retrieval.
- `T5`: encoder-decoder, удобен для seq2seq и text-to-text задач.

</details>

<details>
<summary>Graph RAG</summary>

Это RAG, где поверх документов или сущностей строится граф связей. Он полезен, когда нужны сложные multi-hop связи, а не только локальная похожесть по чанкам.

</details>

<details>
<summary>Как обучались bge-m3, e5?</summary>

Главная идея у современных эмбеддеров — contrastive pretraining/fine-tuning на query-document или instruction-text парах. Для интервью достаточно сказать это, не pretending recall exact recipe.

</details>

<details>
<summary>Что такое cross-encoder?</summary>

- `Bi-encoder`: быстро кодирует query и doc отдельно, хорошо для retrieval.
- `Cross-encoder`: кодирует пару совместно, медленно, но качественно. Часто используется как reranker.

</details>

<details>
<summary>Как реализовать технически базу для ретривера?</summary>

Обычно хранят:

- текст/метаданные документов;
- чанки;
- эмбеддинги;
- ANN-индекс;
- фильтры и служебные поля.

Реализация может быть на FAISS, Milvus, Weaviate, pgvector, Elasticsearch/OpenSearch + dense extension и т.д.

</details>

<details>
<summary>Как хранить базу?</summary>

Обычно хранят:

- текст/метаданные документов;
- чанки;
- эмбеддинги;
- ANN-индекс;
- фильтры и служебные поля.

Реализация может быть на FAISS, Milvus, Weaviate, pgvector, Elasticsearch/OpenSearch + dense extension и т.д.

</details>

<details>
<summary>Как выглядит flow работы RAG в сервисе?</summary>

1. запрос пользователя;
2. optional rewrite/classification;
3. retrieval;
4. reranking;
5. сбор контекста;
6. prompt construction;
7. generation;
8. post-processing, citations, logging.

</details>

<details>
<summary>Как локально подготовить базу для RAG?</summary>

- собрать документы;
- очистить и нормализовать;
- разбить на чанки;
- посчитать эмбеддинги;
- построить индекс;
- завести метаданные;
- прогнать evaluation.

</details>

<details>
<summary>Что делать, если приходят длинные запросы из FAQ?</summary>

- делать query rewriting;
- извлекать intent;
- summary-before-search очень аккуратно;
- multi-query decomposition;
- при необходимости разбивать запрос на подзапросы.

</details>

<details>
<summary>Какие метрики используются?</summary>

Для retrieval:

- Recall@K;
- MRR;
- NDCG;
- HitRate@K.

Для итогового ответа:

- faithfulness;
- answer relevancy;
- answer precision/recall;
- human evaluation;
- task success rate.

</details>

<details>
<summary>Что такое BLEU и ROUGE?</summary>

BLEU и ROUGE — поверхностные overlap-метрики. При синонимии они быстро перестают быть надёжными. Тогда лучше использовать BERTScore, semantic similarity, LLM-based eval и human review.

</details>

<details>
<summary>Если есть синонимы — как тогда замерять метрики?</summary>

BLEU и ROUGE — поверхностные overlap-метрики. При синонимии они быстро перестают быть надёжными. Тогда лучше использовать BERTScore, semantic similarity, LLM-based eval и human review.

</details>

<details>
<summary>Что такое g-Eval?</summary>

G-Eval — это LLM-as-a-judge-подход, где отдельная модель оценивает ответ по критериям. Проверять его нужно корреляцией с человеческой оценкой, устойчивостью к перестановкам и bias/variance judge-модели.

</details>

<details>
<summary>Как оценить, что g-Eval нормально работает?</summary>

G-Eval — это LLM-as-a-judge-подход, где отдельная модель оценивает ответ по критериям. Проверять его нужно корреляцией с человеческой оценкой, устойчивостью к перестановкам и bias/variance judge-модели.

</details>

<details>
<summary>Как бы выглядела архитектура чат-бота поддержки с RAG?</summary>

Запрос -> router -> retrieval -> reranker -> prompt builder -> LLM -> safety/grounding checks -> ответ + ссылки + логирование + feedback loop.

</details>

<details>
<summary>С какими векторными хранилищами работал? Почему иногда не используете FAISS?</summary>

FAISS — это библиотека индекса, а не всегда готовое распределённое хранилище. Когда нужны фильтры, persistence, кластеризация, ACL и удобный продовый слой, выбирают специализированное vector DB или Postgres/Elastic-решение.

</details>

<details>
<summary>Как побить документацию на чанки для векторного поиска?</summary>

Лучше по структуре документа: разделы, подзаголовки, абзацы, списки. Желателен overlap и сохранение ссылок на соседние чанки и родительский раздел.

</details>

<details>
<summary>Какие риски у подхода с суммаризацией перед поиском?</summary>

Суммаризация может выбросить редкую, но важную деталь. Это улучшает сжатие запроса, но ухудшает recall.

</details>

<details>
<summary>Как избежать потери нужной информации при разбиении?</summary>

- overlap;
- метаданные о соседних чанках;
- parent-child retrieval;
- хранение исходного документа и расширение контекста вокруг найденного места.

</details>

<details>
<summary>Что думаешь о подходе с хранением связанных чанков и сборкой целого раздела при поиске?</summary>

Это очень хороший практический приём. Retrieval можно делать по мелким чанкам, а в prompt отдавать связанный родительский раздел или окно соседей.

</details>

<details>
<summary>Как обучал эмбеддинги (роберта + триплет-лосс)?</summary>

Обычно на парах или триплетах:

- позитивы должны быть ближе;
- негативы — дальше.

Triplet loss:

$$
\mathcal{L} = \max(0, s(q, d^-) - s(q, d^+) + m)
$$

Где \(m\) — margin.

</details>

<details>
<summary>Почему выбрали триплет-лосс, а не SimCSE или InfoNCE?</summary>

Triplet loss понятен, прозрачен и удобен, если есть хороший майнинг негативов и конкретная retrieval-задача. InfoNCE и contrastive losses часто эффективнее при больших батчах и in-batch negatives.

</details>

<details>
<summary>Как майнили hard negatives? Что такое hard negative?</summary>

Hard negative — документ, который выглядит релевантным, но на самом деле не должен быть выбран. Искать можно:

- через BM25 или dense retrieval и ручную фильтрацию;
- через соседей по текущему эмбеддеру;
- через cross-encoder reranker;
- через слабую разметку.

</details>

<details>
<summary>Как без разметки можно найти hard negatives?</summary>

Hard negative — документ, который выглядит релевантным, но на самом деле не должен быть выбран. Искать можно:

- через BM25 или dense retrieval и ручную фильтрацию;
- через соседей по текущему эмбеддеру;
- через cross-encoder reranker;
- через слабую разметку.

</details>

<details>
<summary>Как оценивать качество ответа модели в оффлайне и онлайне?</summary>

`Оффлайн`:

- retrieval metrics;
- faithfulness;
- answer relevance;
- semantic similarity;
- judge-based eval;
- разбор конкретных failure cases.

`Онлайн`:

- CTR/usefulness feedback;
- handoff rate на оператора;
- resolution rate;
- deflection rate;
- latency, cost, user satisfaction.

</details>

<details>
<summary>Какие оффлайн-метрики можно использовать (BLEU, Rouge, Similarity)?</summary>

`Оффлайн`:

- retrieval metrics;
- faithfulness;
- answer relevance;
- semantic similarity;
- judge-based eval;
- разбор конкретных failure cases.

`Онлайн`:

- CTR/usefulness feedback;
- handoff rate на оператора;
- resolution rate;
- deflection rate;
- latency, cost, user satisfaction.

</details>

<details>
<summary>Какие онлайн-метрики можно использовать (feedback от операторов, G-Eval, faithfulness, answer precision/recall)?</summary>

- `Faithfulness`: ответ опирается на предоставленный контекст и не галлюцинирует.
- `Answer precision`: доля утверждений ответа, которые поддержаны контекстом.
- `Answer recall`: насколько ответ покрывает важную информацию из эталона или контекста.

</details>

<details>
<summary>Что знаешь про faithfulness и answer precision/recall?</summary>

- `Faithfulness`: ответ опирается на предоставленный контекст и не галлюцинирует.
- `Answer precision`: доля утверждений ответа, которые поддержаны контекстом.
- `Answer recall`: насколько ответ покрывает важную информацию из эталона или контекста.

</details>

<details>
<summary>Как бы сделал RAG, который умеет работать с картинками?</summary>

Нужен мультимодальный pipeline:

- OCR для текста с картинки;
- vision encoder или multimodal LLM для визуальных признаков;
- хранение image embeddings и метаданных;
- объединённый retrieval по тексту и картинкам.

Если пользователь прислал только картинку, можно:

- извлечь OCR-текст;
- сделать captioning;
- построить image embedding;
- использовать multimodal LLM.

</details>

<details>
<summary>Что делать, если пользователь присылает только картинку (без текста)?</summary>

Нужен мультимодальный pipeline:

- OCR для текста с картинки;
- vision encoder или multimodal LLM для визуальных признаков;
- хранение image embeddings и метаданных;
- объединённый retrieval по тексту и картинкам.

Если пользователь прислал только картинку, можно:

- извлечь OCR-текст;
- сделать captioning;
- построить image embedding;
- использовать multimodal LLM.

</details>

<details>
<summary>Как можно извлечь текст с картинки для поиска?</summary>

Практически: Tesseract, PaddleOCR, облачные OCR-сервисы или мультимодальные модели. Главное — нормализовать шумный текст и сохранять связь с исходным изображением.

</details>

<details>
<summary>Есть ли опыт работы с OCR?</summary>

Практически: Tesseract, PaddleOCR, облачные OCR-сервисы или мультимодальные модели. Главное — нормализовать шумный текст и сохранять связь с исходным изображением.

</details>

<details>
<summary>Мультимодальные LLM (например, Qwen-VL)?</summary>

Это модели, которые принимают не только текст, но и изображения, иногда аудио/видео. В RAG-системах они помогают, когда контент не сводится к plain text.

</details>

<details>
<summary>Как работал с распознаванием речи (speech-to-text)?</summary>

Для интервью достаточно знать пайплайн:

- VAD отделяет речь от тишины;
- ASR переводит аудио в текст;
- командные классификаторы работают поверх спектрограмм или эмбеддингов.

Аугментации:

- шум;
- реверберация;
- speed perturbation;
- pitch shift;
- mix with background.

</details>

<details>
<summary>Расскажи про проект с voice activity detection и классификацией команд.</summary>

Для интервью достаточно знать пайплайн:

- VAD отделяет речь от тишины;
- ASR переводит аудио в текст;
- командные классификаторы работают поверх спектрограмм или эмбеддингов.

Аугментации:

- шум;
- реверберация;
- speed perturbation;
- pitch shift;
- mix with background.

</details>

<details>
<summary>Как аугментировал аудиоданные?</summary>

Для интервью достаточно знать пайплайн:

- VAD отделяет речь от тишины;
- ASR переводит аудио в текст;
- командные классификаторы работают поверх спектрограмм или эмбеддингов.

Аугментации:

- шум;
- реверберация;
- speed perturbation;
- pitch shift;
- mix with background.

</details>

<details>
<summary>Что делать, если база уже заполнена, а нужно добавить новые документы?</summary>

Нужно инкрементально:

- обработать новые документы;
- расчитать чанки и эмбеддинги;
- обновить индекс;
- обновить версии метаданных;
- при необходимости переиндексировать частично или целиком.

</details>

<details>
<summary>Какие метрики используются для оценки качества RAG?</summary>

Для retrieval:

- Recall@K;
- MRR;
- NDCG;
- HitRate@K.

Для итогового ответа:

- faithfulness;
- answer relevancy;
- answer precision/recall;
- human evaluation;
- task success rate.

</details>

<details>
<summary>Какие метрики применяются для оценки генерации итогового ответа?</summary>

`Оффлайн`:

- retrieval metrics;
- faithfulness;
- answer relevance;
- semantic similarity;
- judge-based eval;
- разбор конкретных failure cases.

`Онлайн`:

- CTR/usefulness feedback;
- handoff rate на оператора;
- resolution rate;
- deflection rate;
- latency, cost, user satisfaction.

</details>
