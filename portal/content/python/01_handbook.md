# Python Handbook for ML Engineer Interviews

> Study-версия модуля: сначала учебная часть, потом все точные вопросы из ноутбука в конце модуля.

Python-модуль пока оставляю цельным, потому что вопросы из ноутбука уже перемешивают язык, память, concurrency и задачки. В конце собраны точные вопросы из ноутбука по исходным формулировкам.

## Учебник

### База языка

Основные:

- `int`, `float`, `bool`, `complex`;
- `str`, `bytes`;
- `list`, `tuple`, `set`, `dict`;
- `NoneType`;
- пользовательские классы.

Python динамически типизирован: тип присваивается объекту, а не имени переменной. При желании можно добавлять type hints:

```python
name: str = "Alice"
scores: list[int] = [1, 2, 3]
```

- `mutable`: list, dict, set, большинство пользовательских объектов;
- `immutable`: int, float, str, tuple, frozenset.

Различие важно из-за ссылочной модели: изменение mutable-объекта видно через все ссылки на него.

### Функции, декораторы, контекстные менеджеры

Метод — это функция, связанная с объектом или классом. При вызове экземплярного метода первым аргументом передаётся `self`.

Это анонимная функция из одного выражения. Удобна для коротких inline-операций, но для сложной логики лучше обычный `def`.

Обе концепции нужны для оборачивания поведения:

- декоратор оборачивает функцию/метод;
- контекстный менеджер оборачивает блок кода.

### ООП и data model

Это специальные методы Python data model: `__init__`, `__str__`, `__repr__`, `__len__`, `__iter__`, `__next__`, `__enter__`, `__exit__` и т.д. Они позволяют объекту "вписаться" в язык.

Инкапсуляция, наследование, полиморфизм, абстракция.

Класс — шаблон для создания объектов.

```python
class User:
    def __init__(self, name: str):
        self.name = name
```

### Итераторы и генераторы

Итератор — объект с методами `__iter__` и `__next__`.

```python
class Counter:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        value = self.i
        self.i += 1
        return value
```

Генератор — это функция с `yield`. Он сам реализует протокол итератора и позволяет лениво выдавать значения без ручного класса.

Да.

### Асинхронность, потоки, процессы

Корутина — функция, объявленная через `async def`, которую исполняет event loop. Она умеет добровольно отдавать управление в точках `await`.

`event loop` — диспетчер задач, который переключает выполнение между корутинами. `await` говорит: "здесь можно подождать неблокирующую операцию и пока дать поработать другим задачам".

Для I/O-bound задач:

- HTTP-запросы;
- сокеты;
- БД;
- чтение сетевых сервисов.

Для CPU-bound задач async не решает проблему производительности сам по себе.

### Память и GC

В CPython есть reference counting плюс garbage collector для циклических ссылок. Объект удаляется, когда счётчик ссылок падает до нуля, а циклы добирает GC.

Сразу при `refcount == 0`, либо позже проходом cyclic GC, если есть циклические ссылки.

### Практические инженерные вопросы

Нужно построить устойчивый pipeline:

1. читать ссылки батчами;
2. ограничивать concurrency;
3. делать retries и таймауты;
4. логировать неудачи отдельно;
5. сохранять метаданные и статус скачивания;
6. отделить скачивание от постобработки через очередь.

Для сетевого I/O хорошо подходят:

- `asyncio` + `aiohttp`;
- thread pool;
- очередь задач.

Если нужно ещё и CPU-предобработка, скачивание можно делать async/threaded, а тяжёлую обработку вынести в процессы.

Лучший ответ: сделать producer-consumer pipeline с retry, backoff, rate limiting, checkpointing и идемпотентной записью результатов.

### Небольшие coding patterns

```python
def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]
```

```python
def merge_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out
```

Идея:

1. найти `min`, `max`;
2. проверить, что \((max-min)\) делится на \(n-1\);
3. вычислить шаг;
4. проверить, что все ожидаемые элементы есть.

## Вопросы из ноутбука

### Python: общие вопросы

<details>
<summary>Как организуешь процесс скачивания очень большого количества изображений по списку ссылок?</summary>

Нужно построить устойчивый pipeline:

1. читать ссылки батчами;
2. ограничивать concurrency;
3. делать retries и таймауты;
4. логировать неудачи отдельно;
5. сохранять метаданные и статус скачивания;
6. отделить скачивание от постобработки через очередь.

</details>

<details>
<summary>Как распараллелить процесс скачивания?</summary>

Для сетевого I/O хорошо подходят:

- `asyncio` + `aiohttp`;
- thread pool;
- очередь задач.

Если нужно ещё и CPU-предобработка, скачивание можно делать async/threaded, а тяжёлую обработку вынести в процессы.

</details>

<details>
<summary>Чем отличаются потоки от процессов?</summary>

- `Thread`: общий адресный space, дешевле переключение, но ограничение GIL для Python bytecode.
- `Process`: отдельная память, дороже, но даёт реальный параллелизм на CPU.

</details>

<details>
<summary>Как работает async в Python?</summary>

Корутина — функция, объявленная через `async def`, которую исполняет event loop. Она умеет добровольно отдавать управление в точках `await`.

</details>

<details>
<summary>Почему в Python нет полноценной многопоточности?</summary>

GIL — Global Interpreter Lock, который позволяет только одному потоку выполнять Python bytecode одновременно в процессе CPython. Он упрощает внутреннюю работу интерпретатора и управление памятью.

</details>

<details>
<summary>Для чего нужен GIL?</summary>

GIL — Global Interpreter Lock, который позволяет только одному потоку выполнять Python bytecode одновременно в процессе CPython. Он упрощает внутреннюю работу интерпретатора и управление памятью.

</details>

<details>
<summary>Можно ли обойти ограничение GIL при работе с потоками? Каким образом?</summary>

Да, частично:

- использовать C-расширения, которые отпускают GIL;
- I/O-bound потоки часто не страдают сильно;
- для CPU-bound задач лучше multiprocessing.

</details>

### Типы данных

<details>
<summary>Какие типы данных есть в Python?</summary>

Основные:

- `int`, `float`, `bool`, `complex`;
- `str`, `bytes`;
- `list`, `tuple`, `set`, `dict`;
- `NoneType`;
- пользовательские классы.

</details>

<details>
<summary>Как задаём типы данных в Python?</summary>

Python динамически типизирован: тип присваивается объекту, а не имени переменной. При желании можно добавлять type hints:

```python
name: str = "Alice"
scores: list[int] = [1, 2, 3]
```

</details>

<details>
<summary>Какие типы являются изменяемыми (list, dict, set) и какие — неизменяемыми (числа, строки, tuple и др.)? В чём их различие? (ссылочная модель данных, присваивание, copy vs deepcopy)</summary>

Изменяемые типы можно менять на месте, и это изменение увидят все ссылки на тот же объект. Классические примеры: `list`, `dict`, `set`. Неизменяемые типы нельзя менять на месте, при 'изменении' создаётся новый объект: `int`, `float`, `str`, `tuple`. Это важно из-за ссылочной модели Python и разницы между присваиванием, `copy` и `deepcopy`.

</details>

<details>
<summary>В чём разница между list и tuple?</summary>

- `list`: изменяемый;
- `tuple`: неизменяемый и обычно легче по памяти.

Tuple можно использовать как ключ словаря, если все его элементы хешируемы.

</details>

<details>
<summary>Какова скорость поиска в списке, множестве и словаре? (O(n) vs O(1))</summary>

- `list`: \(O(n)\)
- `set`: в среднем \(O(1)\)
- `dict`: в среднем \(O(1)\)

</details>

<details>
<summary>Как работает словарь (хеш-таблица)? Что такое хеш-функция и коллизии? Как с ними бороться?</summary>

Ключ преобразуется в hash, по нему выбирается бакет/ячейка. Коллизия — ситуация, когда разные ключи попадают в один бакет. В CPython они разрешаются внутренней схемой адресации и probing.

</details>

<details>
<summary>Что может быть ключом словаря?</summary>

Хешируемый объект: обычно immutable-объекты, например числа, строки, tuple из хешируемых элементов.

</details>

<details>
<summary>Какие условные операторы вы знаете? (if, else, elif, тернарный оператор)</summary>

`if`, `elif`, `else`, тернарный оператор:

```python
x = a if cond else b
```

</details>

<details>
<summary>Какие циклы существуют? (for, while)</summary>

`for` и `while`.

</details>

<details>
<summary>Для чего служат конструкции try, except, else, finally?</summary>

- `try`: код, где может быть исключение;
- `except`: обработка исключения;
- `else`: выполняется, если исключения не было;
- `finally`: выполняется всегда.

</details>

<details>
<summary>В чём разница между == и is?</summary>

- `==`: сравнение значений;
- `is`: сравнение идентичности объектов.

</details>

<details>
<summary>Декораторы и контекстные менеджеры</summary>

Обе концепции нужны для оборачивания поведения:

- декоратор оборачивает функцию/метод;
- контекстный менеджер оборачивает блок кода.

</details>

<details>
<summary>Что такое декоратор? Для чего он нужен?</summary>

Это функция, которая принимает функцию и возвращает новую функцию. Нужен для логирования, кэша, авторизации, ретраев и т.д.

</details>

<details>
<summary>Какие виды декораторов вы знаете? (@classmethod, @staticmethod, @property и др.)</summary>

- пользовательские декораторы;
- `@classmethod`;
- `@staticmethod`;
- `@property`;
- декораторы с аргументами.

</details>

<details>
<summary>Как устроен декоратор внутри? Что он принимает на вход и что возвращает?</summary>

Он принимает функцию и возвращает wrapper-функцию.

```python
def deco(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

</details>

<details>
<summary>Реализуйте простой декоратор.</summary>

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

</details>

<details>
<summary>Что такое менеджер контекста? Зачем он нужен?</summary>

Это объект, который управляет ресурсом на время блока `with`. Частый пример — файл, соединение, лок, временная настройка.

</details>

<details>
<summary>Как работают методы __enter__ и __exit__?</summary>

- `__enter__` вызывается при входе в `with`;
- `__exit__` — при выходе, даже если было исключение.

</details>

<details>
<summary>Реализуйте простой контекстный менеджер.</summary>

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc, tb):
        import time
        self.elapsed = time.time() - self.start
        print(self.elapsed)
```

</details>

<details>
<summary>В чём отличие функции от метода?</summary>

Метод — это функция, связанная с объектом или классом. При вызове экземплярного метода первым аргументом передаётся `self`.

</details>

<details>
<summary>Что такое lambda-функция? Чем она отличается от обычной функции и когда создаётся?</summary>

Это анонимная функция из одного выражения. Удобна для коротких inline-операций, но для сложной логики лучше обычный `def`.

</details>

<details>
<summary>Что такое магические методы? Почему они нужны и какие вы знаете? (например, __str__, __repr__)</summary>

Это специальные методы Python data model: `__init__`, `__str__`, `__repr__`, `__len__`, `__iter__`, `__next__`, `__enter__`, `__exit__` и т.д. Они позволяют объекту "вписаться" в язык.

</details>

<details>
<summary>Что такое итератор? Как создать класс-итератор? (методы __iter__ и __next__)</summary>

Итератор — объект с методами `__iter__` и `__next__`.

```python
class Counter:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        value = self.i
        self.i += 1
        return value
```

</details>

<details>
<summary>Что такое генератор? Чем он отличается от итератора? (функция с yield vs класс)</summary>

Генератор — это функция с `yield`. Он сам реализует протокол итератора и позволяет лениво выдавать значения без ручного класса.

</details>

<details>
<summary>Верно ли, что любой генератор является итератором?</summary>

Да.

</details>

<details>
<summary>Реализуйте итератор, который возводит значения в квадрат.</summary>

```python
class SquareIter:
    def __init__(self, values):
        self.values = values
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx >= len(self.values):
            raise StopIteration
        value = self.values[self.idx] ** 2
        self.idx += 1
        return value
```

</details>

<details>
<summary>Реализуйте итератор для чисел Фибоначчи.</summary>

```python
class Fib:
    def __init__(self, n):
        self.n = n
        self.i = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        val = self.a
        self.a, self.b = self.b, self.a + self.b
        return val
```

</details>

<details>
<summary>Что такое ООП и его основные принципы?</summary>

Инкапсуляция, наследование, полиморфизм, абстракция.

</details>

<details>
<summary>Что такое класс? Как объявить и использовать?</summary>

Класс — шаблон для создания объектов.

```python
class User:
    def __init__(self, name: str):
        self.name = name
```

</details>

<details>
<summary>Что такое super? Когда и зачем его применять?</summary>

Позволяет обратиться к реализации родительского класса, обычно в наследовании.

</details>

<details>
<summary>В чём разница между @classmethod и @staticmethod?</summary>

- `@classmethod` получает `cls` и работает с классом;
- `@staticmethod` не получает ни `self`, ни `cls`, это просто функция внутри namespace класса.

</details>

<details>
<summary>Что такое @dataclass? Зачем нужен?</summary>

Это удобный способ объявлять классы-структуры данных без лишнего boilerplate. Автоматически генерирует `__init__`, `__repr__`, сравнение и другое.

</details>

<details>
<summary>Как проверить, есть ли у объекта атрибут? (getattr, setattr, delattr)</summary>

- `hasattr(obj, "x")`
- `getattr(obj, "x", default)`
- `setattr(obj, "x", value)`
- `delattr(obj, "x")`

</details>

<details>
<summary>Чем отличаются методы __str__ и __repr__?</summary>

- `__str__`: человекочитаемое представление;
- `__repr__`: более техническое представление, желательно пригодное для отладки.

</details>

<details>
<summary>Как работает асинхронность в Python? Что такое корутина?</summary>

Корутина — функция, объявленная через `async def`, которую исполняет event loop. Она умеет добровольно отдавать управление в точках `await`.

</details>

<details>
<summary>Что такое event loop и оператор await?</summary>

`event loop` — диспетчер задач, который переключает выполнение между корутинами. `await` говорит: "здесь можно подождать неблокирующую операцию и пока дать поработать другим задачам".

</details>

<details>
<summary>Для каких задач эффективна асинхронность?</summary>

Для I/O-bound задач:

- HTTP-запросы;
- сокеты;
- БД;
- чтение сетевых сервисов.

Для CPU-bound задач async не решает проблему производительности сам по себе.

</details>

<details>
<summary>Что такое GIL и почему Python называют однопоточным?</summary>

GIL — Global Interpreter Lock, который позволяет только одному потоку выполнять Python bytecode одновременно в процессе CPython. Он упрощает внутреннюю работу интерпретатора и управление памятью.

</details>

<details>
<summary>Чем отличается многопоточность от мультипроцессинга?</summary>

Многопоточность удобна для I/O-bound, multiprocessing — для CPU-bound.

</details>

<details>
<summary>В чём различие между потоком и процессом?</summary>

Потоки делят память одного процесса. Процессы изолированы друг от друга.

</details>

<details>
<summary>Какие проблемы возникают при многопоточности?</summary>

- race conditions;
- deadlocks;
- starvation;
- сложности отладки;
- состояние, разделяемое между потоками.

</details>

<details>
<summary>Как организовать обмен данными между процессами?</summary>

- `multiprocessing.Queue`;
- `Pipe`;
- shared memory;
- сокеты;
- внешняя БД/брокер сообщений.

</details>

<details>
<summary>Что такое ссылочная модель в Python?</summary>

Имя переменной хранит ссылку на объект. Операция присваивания не копирует объект, а привязывает имя к существующему объекту.

</details>

<details>
<summary>В чём разница между copy и deepcopy?</summary>

- `copy.copy`: поверхностная копия, вложенные объекты общие;
- `copy.deepcopy`: рекурсивно копирует и вложенные объекты.

</details>

<details>
<summary>Как работает память в Python и сборщик мусора?</summary>

В CPython есть reference counting плюс garbage collector для циклических ссылок. Объект удаляется, когда счётчик ссылок падает до нуля, а циклы добирает GC.

</details>

<details>
<summary>Когда и как объекты удаляются сборщиком мусора?</summary>

Сразу при `refcount == 0`, либо позже проходом cyclic GC, если есть циклические ссылки.

</details>

<details>
<summary>Как происходит управление памятью при использовании multiprocessing?</summary>

У каждого процесса своя память. На Unix возможен copy-on-write после fork, но после изменений память дублируется. Передача больших объектов между процессами может быть дорогой.

</details>

<details>
<summary>Продвинутое использование Python</summary>

Это скорее маркер следующего блока вопросов, а не самостоятельный теоретический вопрос. Обычно после него спрашивают про межпроцессное взаимодействие, работу с API, type hints и небольшие алгоритмические задачи.

</details>

<details>
<summary>Как организовать передачу информации между двумя приложениями на Python?</summary>

- HTTP/gRPC;
- очередь сообщений;
- shared DB;
- Redis;
- сокеты;
- файл/pipe, если это локальный простой сценарий.

</details>

<details>
<summary>Как скачать и обработать датасет изображений через API сервиса?</summary>

Лучший ответ: сделать producer-consumer pipeline с retry, backoff, rate limiting, checkpointing и идемпотентной записью результатов.

</details>

<details>
<summary>Что такое Type Hints и как они используются?</summary>

Это аннотации типов для читаемости, IDE, статического анализа и документации. На рантайме Python не становится строго типизированным автоматически.

</details>

<details>
<summary>Напишите функцию для умножения матрицы на вектор.</summary>

```python
def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]
```

</details>

<details>
<summary>Объедините два отсортированных списка в один без использования внешних библиотек.</summary>

```python
def merge_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out
```

</details>

<details>
<summary>Напишите функцию для проверки, является ли массив арифметической прогрессией (массив не отсортирован).</summary>

Идея:

1. найти `min`, `max`;
2. проверить, что \((max-min)\) делится на \(n-1\);
3. вычислить шаг;
4. проверить, что все ожидаемые элементы есть.

</details>

<details>
<summary>Как отсортировать файл размером 100 GB при ограничении RAM 120 GB?</summary>

Если RAM действительно 120 GB, файл можно уместить целиком. Если бы файл был больше памяти, использовали бы external sort:

1. сортировать чанки;
2. писать временные файлы;
3. делать k-way merge.

</details>

<details>
<summary>Как найти медиану, если в SQL или Python нет встроенной функции для этого?</summary>

Нужно либо отсортировать и взять середину, либо использовать two-heaps / quickselect, если нужен более эффективный вариант по времени.

</details>

<details>
<summary>Реализуйте функцию подсчёта recall для двух NumPy-массивов.</summary>

```python
import numpy as np

def recall_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp / (tp + fn) if (tp + fn) else 0.0
```

</details>

<details>
<summary>Что нужно, чтобы отсортировать список элементов в Python? Какова сложность встроенной сортировки?</summary>

Нужно, чтобы элементы были сравнимы или был задан `key`. Встроенная сортировка — Timsort, сложность \(O(n \log n)\) в среднем и лучшем реальном поведении на частично отсортированных данных.

</details>

<details>
<summary>Напишите функцию, определяющую максимальную высоту, достигнутую велосипедом (задача с высотой).</summary>

Если есть массив изменений высоты, надо идти префиксной суммой и брать максимум.

</details>

<details>
<summary>Задача: найдите максимальную длину монотонного подмассива и верните его индексы.</summary>

Идея — один проход двумя счётчиками: длина текущего неубывающего и невозрастающего отрезка, с обновлением лучшего ответа.

</details>
