# Пособие по ML / MLE Interview

Это рабочая версия пособия, собранная на основе вопросов из ноутбука
[СБОРНИК ВОПРОСОВ ПО ML НА РУССКОМ.ipynb](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/others/questions/СБОРНИК%20ВОПРОСОВ%20ПО%20ML%20НА%20РУССКОМ.ipynb).

Основная идея:

- единица хранения: модуль, а не одиночный вопрос;
- внутри каждого модуля есть `Core explanation`, список терминов и блоки `Вопрос -> Ответ`;
- формулы записаны в LaTeX, чтобы материал было удобно учить и конвертировать;
- стиль ответа ориентирован на собеседование: понятно, компактно, но без потери сути.

Теперь у пособия есть два режима чтения:

- `Учебник`: обычные модули в `knowledge_base/...`
- `Study-режим`: отдельные учебные версии в [study/README.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/study/README.md), где ответы на вопросы можно сворачивать и разворачивать через `<details>`

## Структура

- [classic_ml/01_models.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/classic_ml/01_models.md)
- [classic_ml/02_advanced.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/classic_ml/02_advanced.md)
- [recsys/01_handbook.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/recsys/01_handbook.md)
- [deep_learning/01_core.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/deep_learning/01_core.md)
- [nlp_llm/01_handbook.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/nlp_llm/01_handbook.md)
- [cv/01_handbook.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/cv/01_handbook.md)
- [metrics/01_handbook.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/metrics/01_handbook.md)
- [python/01_handbook.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/python/01_handbook.md)
- [databases/01_handbook.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/databases/01_handbook.md)
- [production/01_handbook.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/production/01_handbook.md)
- [statistics/01_handbook.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/statistics/01_handbook.md)

## Study-версия

- [study/README.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/study/README.md)
- [study/HANDBOOK.md](/Users/dmitrybulgakov/Desktop/my_repos/get_ready_machine_learning/knowledge_base/study/HANDBOOK.md)

## Как читать

Лучший режим подготовки:

1. Идти по модулям сверху вниз.
2. Сначала читать `Core explanation`, чтобы собрать цельную картину.
3. Потом проходить вопросы и проверять, можешь ли ты ответить до чтения ответа.
4. Отдельно выписывать формулы и пороги/эвристики, которые чаще всего спрашивают.

## Как конвертировать

Рекомендованный основной формат: `Markdown`.

Почему именно он:

- легко редактировать;
- удобно хранить в git;
- просто собирать в HTML;
- нормально конвертируется в PDF;
- поддерживает LaTeX-формулы через MathJax, KaTeX или Pandoc.

Примеры дальнейшей сборки:

- `Markdown -> HTML`: через любой static site generator или простой markdown renderer с MathJax.
- `Markdown -> PDF`: через Pandoc или через печать HTML в PDF.

Если позже захочешь, следующим шагом можно будет:

- сделать единый `HANDBOOK.md`, автоматически собранный из модулей;
- добавить frontmatter и теги для будущего портала;
- собрать HTML-версию со стилями под печать.
