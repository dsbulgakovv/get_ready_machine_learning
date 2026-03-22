# NLP / LLM: архитектуры, attention и transformers

> Study-версия модуля: сначала учебная часть, потом все точные вопросы из ноутбука в конце модуля.

Этот модуль стоит учить как самостоятельный пласт: именно здесь находится большая часть архитектурных вопросов про attention, позиционное кодирование и типы трансформеров.

## Учебник

### Теория и архитектуры NLP

RNN последовательно обновляет скрытое состояние по токенам. Классические варианты:

- vanilla RNN;
- LSTM;
- GRU;
- bidirectional RNN.

Сейчас они уступили Transformers в большинстве крупных NLP-задач.

Это архитектура, которая заменяет рекуррентность механизмом внимания. Она обрабатывает последовательность через слои self-attention и feed-forward блоков с residual connections и normalization.

Идея: каждый токен смотрит на остальные и агрегирует полезную информацию. Формула scaled dot-product attention:

$$
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

### Transformer подробно

Классический encoder block:

1. multi-head self-attention;
2. residual connection;
3. normalization;
4. feed-forward network;
5. residual connection;
6. normalization.

Декодер добавляет masked self-attention и cross-attention к выходам энкодера.

Декодер:

- не видит будущие токены из-за causal mask;
- при seq2seq может смотреть на выход энкодера через cross-attention.

Сначала токены превращаются в embeddings, затем в них добавляется позиционная информация, и уже после этого последовательность идёт в attention-блоки.

### Ускорение Transformer

- FlashAttention;
- KV cache;
- sparse/window attention;
- grouped-query attention;
- linear attention approximations;
- mixed precision;
- quantization.

Это реализация attention, оптимизированная под память и I/O. Она не меняет математическую идею attention, а делает вычисление эффективнее на GPU.

При генерации мы сохраняем keys и values для уже обработанных токенов и не пересчитываем их заново. Это сильно ускоряет autoregressive inference.

### Эмбеддинги и tricky-вопросы

- one-hot + embedding layer;
- Word2Vec;
- GloVe;
- FastText;
- contextual embeddings из BERT/Transformer;
- domain-specific embeddings.

FastText строит слово из символьных \(n\)-грамм, поэтому умеет лучше обрабатывать редкие и OOV-слова. Это особенно полезно для морфологически богатых языков.

Разбивает их на subword-токены, чаще всего через WordPiece-подобную схему. Поэтому полного OOV в современном смысле там обычно нет.

## Вопросы из ноутбука

### Теория и архитектуры NLP

<details>
<summary>Что такое RNN и какие её варианты существуют?</summary>

RNN последовательно обновляет скрытое состояние по токенам. Классические варианты:

- vanilla RNN;
- LSTM;
- GRU;
- bidirectional RNN.

Сейчас они уступили Transformers в большинстве крупных NLP-задач.

</details>

<details>
<summary>Что такое Transformer?</summary>

Это архитектура, которая заменяет рекуррентность механизмом внимания. Она обрабатывает последовательность через слои self-attention и feed-forward блоков с residual connections и normalization.

</details>

<details>
<summary>Как работает attention?</summary>

Идея: каждый токен смотрит на остальные и агрегирует полезную информацию. Формула scaled dot-product attention:

$$
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

</details>

<details>
<summary>Что такое positional encoding в трансформерах?</summary>

Это способ добавить информации о порядке токенов. Без него модель знала бы, какие токены есть, но не знала бы, в каком порядке.

</details>

<details>
<summary>Что такое perplexity?</summary>

Perplexity — это экспонента от средней отрицательной log-likelihood:

$$
\mathrm{PPL} = \exp\left(-\frac{1}{N}\sum_{i=1}^N \log p(x_i \mid x_{<i})\right)
$$

Чем меньше perplexity, тем лучше модель предсказывает следующий токен на тесте. Но низкая perplexity не гарантирует хороший пользовательский текст.

</details>

### Tricky

<details>
<summary>Какие способы построения эмбеддингов для слов знаешь?</summary>

- one-hot + embedding layer;
- Word2Vec;
- GloVe;
- FastText;
- contextual embeddings из BERT/Transformer;
- domain-specific embeddings.

</details>

<details>
<summary>Чем FastText лучше Word2Vec?</summary>

FastText строит слово из символьных \(n\)-грамм, поэтому умеет лучше обрабатывать редкие и OOV-слова. Это особенно полезно для морфологически богатых языков.

</details>

<details>
<summary>Может ли FastText работать с out-of-vocabulary словами?</summary>

FastText строит слово из символьных \(n\)-грамм, поэтому умеет лучше обрабатывать редкие и OOV-слова. Это особенно полезно для морфологически богатых языков.

</details>

<details>
<summary>Как BERT обрабатывает слова, которых нет в словаре?</summary>

Разбивает их на subword-токены, чаще всего через WordPiece-подобную схему. Поэтому полного OOV в современном смысле там обычно нет.

</details>

<details>
<summary>Как получить эмбеддинг для слова из нескольких токенов?</summary>

Варианты:

- взять первый subword;
- усреднить subword embeddings;
- max pooling;
- контекстно-зависимо выбирать по задаче.

</details>

<details>
<summary>Как получить эмбеддинг всего предложения?</summary>

- `[CLS]` токен;
- mean pooling;
- max pooling;
- отдельная sentence embedding модель.

</details>

<details>
<summary>Какие бывают архитектуры трансформеров (энкодер, декодер, энкодер-декодер)?</summary>

- encoder-only;
- decoder-only;
- encoder-decoder.

</details>

<details>
<summary>Как работает self-attention?</summary>

Self-attention связывает токены внутри одной последовательности. Cross-attention связывает две разные последовательности.

</details>

<details>
<summary>Чем отличается self-attention от cross-attention?</summary>

Self-attention связывает токены внутри одной последовательности. Cross-attention связывает две разные последовательности.

</details>

<details>
<summary>Зачем нужен positional encoding в трансформере?</summary>

Это способ добавить информации о порядке токенов. Без него модель знала бы, какие токены есть, но не знала бы, в каком порядке.

</details>

<details>
<summary>Какие способы позиционного кодирования знаешь?</summary>

- one-hot + embedding layer;
- Word2Vec;
- GloVe;
- FastText;
- contextual embeddings из BERT/Transformer;
- domain-specific embeddings.

</details>

<details>
<summary>Меняется ли эмбеддинг токена в зависимости от его позиции в предложении?</summary>

Да, итоговое представление токена зависит от его позиции. Варианты PE: sinusoidal, learned, relative, RoPE, ALiBi.

</details>

<details>
<summary>Как распараллелить обработку миллиарда событий с BERT, чтобы уложиться хотя бы в час?</summary>

- батчить запросы;
- использовать GPU/многопроцессный inference;
- квантовать/дистиллировать модель;
- перейти на более лёгкий encoder;
- заранее вычислять эмбеддинги там, где это возможно;
- использовать distributed inference pipeline.

</details>

### Transformer

<details>
<summary>Расскажи про архитектуры трансформера и из каких частей они состоят.</summary>

Классический encoder block:

1. multi-head self-attention;
2. residual connection;
3. normalization;
4. feed-forward network;
5. residual connection;
6. normalization.

Декодер добавляет masked self-attention и cross-attention к выходам энкодера.

</details>

<details>
<summary>Это описание было про энкодер — что насчёт декодера?</summary>

Декодер:

- не видит будущие токены из-за causal mask;
- при seq2seq может смотреть на выход энкодера через cross-attention.

</details>

<details>
<summary>Что используется перед attention в трансформере?</summary>

Сначала токены превращаются в embeddings, затем в них добавляется позиционная информация, и уже после этого последовательность идёт в attention-блоки.

</details>

<details>
<summary>Что такое attention и как он работает?</summary>

Смысл — позволить каждому токену выбирать, на какие другие токены ему опереться. Это даёт глобальный контекст и лучшее моделирование зависимостей, чем фиксированное окно.

</details>

<details>
<summary>Как в attention учитывается расположение слов?</summary>

Через positional encoding или relative position schemes вроде RoPE/ALiBi.

</details>

<details>
<summary>Расскажи про трансформер: как работает, что внутри происходит?</summary>

Классический encoder block:

1. multi-head self-attention;
2. residual connection;
3. normalization;
4. feed-forward network;
5. residual connection;
6. normalization.

Декодер добавляет masked self-attention и cross-attention к выходам энкодера.

</details>

<details>
<summary>Что такое self attention слой, формула? Разница между query, keys, values</summary>

Для каждого токена считаются три проекции:

- `Q`: что я ищу;
- `K`: чем я могу быть полезен другим;
- `V`: какую информацию я отдаю.

Потом similarity между Q и K определяет веса, с которыми усредняются V.

</details>

<details>
<summary>Какая формула у self attention?</summary>

Та же базовая:

$$
\mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

</details>

<details>
<summary>Чем отличаются mask attention, cross attention, full attention?</summary>

- `Full self-attention`: токен может смотреть на все токены.
- `Masked / causal attention`: токен видит только прошлое и себя.
- `Cross-attention`: queries приходят из одной последовательности, keys/values — из другой.

</details>

<details>
<summary>Что такое multihead attention?</summary>

Это несколько параллельных attention-голов, каждая из которых работает в своей подпространственной проекции. Потом результаты голов конкатенируются и снова проецируются.

</details>

<details>
<summary>Как разделяем последовательность между головами?</summary>

Сама последовательность не делится по токенам. Для каждого токена строятся разные линейные проекции \(Q, K, V\) для каждой головы. То есть головы видят одни и те же токены, но в разных пространствах признаков.

</details>

<details>
<summary>Что такое attention score?</summary>

Это значение похожести между query и key до softmax. После softmax scores превращаются в attention weights.

</details>

<details>
<summary>Как растёт сложность вычислений от увеличения входной последовательности?</summary>

Классический self-attention по времени и памяти масштабируется как \(O(n^2)\) по длине последовательности \(n\).

</details>

<details>
<summary>Что обучается в трансформере?</summary>

Все линейные проекции, embedding matrices, параметры FFN, LayerNorm и другие обучаемые веса. Если fine-tuning частичный, то обучается только выбранное подмножество.

</details>

<details>
<summary>Как получаем финальный ответ в трансформере?</summary>

Зависит от архитектуры:

- encoder-only: берём `[CLS]`, pooled representation или токеновые выходы;
- decoder-only: генерируем следующий токен по logits последней позиции;
- encoder-decoder: декодер генерирует выходную последовательность, используя память энкодера.

</details>

<details>
<summary>Зачем в формуле attention используется деление на sqrt(d_k)?</summary>

Чтобы скалярные произведения не росли слишком сильно с размерностью и softmax не входил в насыщение.

</details>

<details>
<summary>Что произойдет, если из трансформера убрать FFN-слои и оставить только self-attention с нормализациями?</summary>

Модель сильно потеряет выразительность. Attention хорошо смешивает информацию между токенами, но без position-wise нелинейного FFN сложнее строить богатые преобразования признаков.

</details>

<details>
<summary>Зачем в трансформере используется LayerNorm вместо BatchNorm?</summary>

LayerNorm не зависит от batch size и длины батча, работает стабильно при переменной длине последовательностей и автрорегрессивной генерации. BatchNorm хуже сочетается с переменными последовательностями и малыми batch size.

</details>

<details>
<summary>Почему BatchNorm сложно применять при обучении трансформеров?</summary>

LayerNorm не зависит от batch size и длины батча, работает стабильно при переменной длине последовательностей и автрорегрессивной генерации. BatchNorm хуже сочетается с переменными последовательностями и малыми batch size.

</details>

<details>
<summary>Чем отличается GPT от BERT?</summary>

- `BERT`: encoder-only, двусторонний контекст, задачи понимания текста.
- `GPT`: decoder-only, causal attention, автрорегрессивная генерация.

</details>

<details>
<summary>Что такое DistilBERT, RoBERTa, чем отличаются от BERT?</summary>

- `DistilBERT`: уменьшенная и дистиллированная версия BERT.
- `RoBERTa`: улучшенная схема обучения BERT без NSP, с большим корпусом и изменённым masking pipeline.

</details>

<details>
<summary>Что такое attention и его формула?</summary>

Это значение похожести между query и key до softmax. После softmax scores превращаются в attention weights.

</details>

<details>
<summary>Почему attention делим на sqrt(d)?</summary>

См. выше: ради численной стабильности softmax.

</details>

<details>
<summary>Сложность attention (O(n²)), какие есть оптимизации?</summary>

Классический self-attention требует матрицу попарных взаимодействий токенов, поэтому по памяти и времени растёт как \(O(n^2)\). Ускоряют через:

- FlashAttention;
- sparse attention;
- линейные аппроксимации;
- chunking и window attention.

Подробно тема раскрыта в NLP/LLM модуле.

</details>

<details>
<summary>Что такое multi-head attention? Почему головы дают разные эмбеддинги?</summary>

Это несколько параллельных attention-голов, каждая из которых работает в своей подпространственной проекции. Потом результаты голов конкатенируются и снова проецируются.

</details>

<details>
<summary>Что такое cross-attention? Encoder/decoder attention в T5?</summary>

Cross-attention позволяет декодеру смотреть на энкодерные представления. В T5 это ключевой механизм seq2seq.

</details>

<details>
<summary>Bi-encoder vs Cross-encoder — в чем разница?</summary>

- `Bi-encoder`: кодирует объекты независимо, быстро подходит для retrieval.
- `Cross-encoder`: кодирует пару совместно, медленнее, но качественнее для reranking.

</details>

### Ускорение Transformer

<details>
<summary>Какие улушения архитекуры для ускорения обучения знаешь?</summary>

- FlashAttention;
- KV cache;
- sparse/window attention;
- grouped-query attention;
- linear attention approximations;
- mixed precision;
- quantization.

</details>

<details>
<summary>Расскажи про Flash Attention</summary>

Это реализация attention, оптимизированная под память и I/O. Она не меняет математическую идею attention, а делает вычисление эффективнее на GPU.

</details>

<details>
<summary>Расскажи про KV cache</summary>

При генерации мы сохраняем keys и values для уже обработанных токенов и не пересчитываем их заново. Это сильно ускоряет autoregressive inference.

</details>

### Разное

<details>
<summary>Какие ограничения у attention? Сложность – O(n²), способы ускорения, flash-attention</summary>

Классический self-attention требует матрицу попарных взаимодействий токенов, поэтому по памяти и времени растёт как \(O(n^2)\). Ускоряют через:

- FlashAttention;
- sparse attention;
- линейные аппроксимации;
- chunking и window attention.

Подробно тема раскрыта в NLP/LLM модуле.

</details>

<details>
<summary>Расскажите про трансформер: как он устроен и что внутри происходит</summary>

Классический encoder block:

1. multi-head self-attention;
2. residual connection;
3. normalization;
4. feed-forward network;
5. residual connection;
6. normalization.

Декодер добавляет masked self-attention и cross-attention к выходам энкодера.

</details>

<details>
<summary>Что обучается в трансформере?</summary>

Все линейные проекции, embedding matrices, параметры FFN, LayerNorm и другие обучаемые веса. Если fine-tuning частичный, то обучается только выбранное подмножество.

</details>

<details>
<summary>В чём смысл attention-слоя, формула, разница между query, key и value</summary>

Для каждого токена считаются три проекции:

- `Q`: что я ищу;
- `K`: чем я могу быть полезен другим;
- `V`: какую информацию я отдаю.

Потом similarity между Q и K определяет веса, с которыми усредняются V.

</details>

<details>
<summary>Как рассчитывается TF-IDF?</summary>

TF-IDF отражает, насколько слово важно для конкретного документа и одновременно не слишком часто встречается в корпусе:

$$
\mathrm{TF}(t, d) = \frac{\text{число вхождений } t \text{ в } d}{\text{общее число токенов в } d}
$$

$$
\mathrm{IDF}(t) = \log \frac{N}{df(t) + 1}
$$

$$
\mathrm{TFIDF}(t, d) = \mathrm{TF}(t, d)\cdot \mathrm{IDF}(t)
$$

Это sparse-представление, полезное для поиска и базового классического NLP.

</details>

<details>
<summary>Расскажите про LoRA (Low-Rank Adaptation)</summary>

Это реализация attention, оптимизированная под память и I/O. Она не меняет математическую идею attention, а делает вычисление эффективнее на GPU.

</details>
