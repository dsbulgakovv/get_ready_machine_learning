from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge_base"
STUDY_ROOT = KB / "study"
NOTEBOOK_PATH = ROOT / "others" / "questions" / "СБОРНИК ВОПРОСОВ ПО ML НА РУССКОМ.ipynb"


@dataclass
class SourceSubsection:
    title: str
    body: str


@dataclass
class SourceSection:
    title: str
    intro: str
    core_explanations: list[str]
    subsections: list[SourceSubsection]

    def theory_text(self) -> str:
        chunks: list[str] = []
        if self.intro.strip():
            chunks.append(self.intro.strip())
        for core in self.core_explanations:
            core = core.strip()
            if core:
                chunks.append(core)
        if not chunks:
            # If the source section has no explicit theory block,
            # take the first few answers to make the top part readable as a textbook.
            for subsection in self.subsections[:3]:
                if subsection.body.strip():
                    chunks.append(subsection.body.strip())
        return "\n\n".join(chunks).strip()


@dataclass
class SourceModule:
    title: str
    intro: str
    sections: dict[str, SourceSection]


@dataclass
class NotebookGroup:
    path: tuple[str, ...]
    questions: list[str] = field(default_factory=list)


@dataclass
class NotebookGroupSpec:
    path: tuple[str, ...]
    source_sections: list[str]
    title_override: str | None = None


@dataclass
class TheorySectionSpec:
    source_file: str
    section_title: str


@dataclass
class StudyModuleSpec:
    output_rel: str
    title: str
    intro: str
    theory_sections: list[TheorySectionSpec]
    notebook_groups: list[NotebookGroupSpec]


def clean_text(text: str) -> str:
    return text.strip()


def normalize(text: str) -> str:
    text = text.lower().replace("ё", "е")
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> set[str]:
    return set(normalize(text).split())


def parse_source_module(path: Path) -> SourceModule:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"Invalid module header in {path}")

    title = lines[0][2:].strip()
    module_intro_lines: list[str] = []
    sections: dict[str, SourceSection] = {}

    current_section_title: str | None = None
    current_section_intro: list[str] = []
    current_core_explanations: list[str] = []
    current_subsections: list[SourceSubsection] = []
    current_subsection_title: str | None = None
    current_subsection_body: list[str] = []

    def flush_subsection() -> None:
        nonlocal current_subsection_title, current_subsection_body, current_core_explanations, current_subsections
        if current_subsection_title is None:
            return
        body = clean_text("\n".join(current_subsection_body))
        if current_subsection_title == "Core explanation":
            if body:
                current_core_explanations.append(body)
        else:
            current_subsections.append(SourceSubsection(current_subsection_title, body))
        current_subsection_title = None
        current_subsection_body = []

    def flush_section() -> None:
        nonlocal current_section_title, current_section_intro, current_core_explanations, current_subsections
        flush_subsection()
        if current_section_title is None:
            return
        sections[current_section_title] = SourceSection(
            title=current_section_title,
            intro=clean_text("\n".join(current_section_intro)),
            core_explanations=current_core_explanations[:],
            subsections=current_subsections[:],
        )
        current_section_title = None
        current_section_intro = []
        current_core_explanations = []
        current_subsections = []

    for line in lines[1:]:
        if line.startswith("## "):
            flush_section()
            current_section_title = line[3:].strip()
            continue
        if line.startswith("### "):
            flush_subsection()
            current_subsection_title = line[4:].strip()
            continue
        if current_section_title is None:
            module_intro_lines.append(line)
        elif current_subsection_title is None:
            current_section_intro.append(line)
        else:
            current_subsection_body.append(line)

    flush_section()

    return SourceModule(
        title=title,
        intro=clean_text("\n".join(module_intro_lines)),
        sections=sections,
    )


def extract_notebook_groups() -> dict[tuple[str, ...], NotebookGroup]:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    stack: list[str] = []
    groups: dict[tuple[str, ...], NotebookGroup] = {}

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        lines = [line.rstrip() for line in "".join(cell.get("source", [])).splitlines() if line.strip()]
        if not lines:
            continue
        first = lines[0].strip()
        if first.startswith("#"):
            level = len(first) - len(first.lstrip("#"))
            title = first[level:].strip()
            stack = stack[: level - 1]
            stack.append(title)
        path = tuple(stack)
        for line in lines[1:] if first.startswith("#") else lines:
            s = line.strip()
            question: str | None = None
            if s.startswith("- "):
                question = s[2:].strip()
            else:
                match = re.match(r"^\d+\.\s+(.*)$", s)
                if match:
                    question = match.group(1).strip()
            if question:
                groups.setdefault(path, NotebookGroup(path)).questions.append(question)
    return groups


SOURCE_MODULES = {
    rel: parse_source_module(path)
    for rel, path in {
        "classic_ml/01_models.md": KB / "classic_ml" / "01_models.md",
        "classic_ml/02_advanced.md": KB / "classic_ml" / "02_advanced.md",
        "recsys/01_handbook.md": KB / "recsys" / "01_handbook.md",
        "deep_learning/01_core.md": KB / "deep_learning" / "01_core.md",
        "nlp_llm/01_handbook.md": KB / "nlp_llm" / "01_handbook.md",
        "cv/01_handbook.md": KB / "cv" / "01_handbook.md",
        "metrics/01_handbook.md": KB / "metrics" / "01_handbook.md",
        "python/01_handbook.md": KB / "python" / "01_handbook.md",
        "databases/01_handbook.md": KB / "databases" / "01_handbook.md",
        "production/01_handbook.md": KB / "production" / "01_handbook.md",
        "statistics/01_handbook.md": KB / "statistics" / "01_handbook.md",
    }.items()
    if path.exists()
}

NOTEBOOK_GROUPS = extract_notebook_groups()

CATEGORY_ORDER = [
    "classic_ml",
    "deep_learning",
    "nlp_llm",
    "cv",
    "recsys",
    "metrics",
    "statistics",
    "python",
    "production",
    "databases",
]
CATEGORY_ORDER_INDEX = {name: idx for idx, name in enumerate(CATEGORY_ORDER)}


MODULE_SPECS = [
    StudyModuleSpec(
        output_rel="classic_ml/01_models.md",
        title="Classic ML: базовые модели",
        intro="Этот модуль удобно читать как базовый фундамент по классическим моделям. Сначала идёт учебная часть по каждому блоку, а затем в конце модуля собраны точные вопросы из ноутбука с раскрывающимися ответами.",
        theory_sections=[
            TheorySectionSpec("classic_ml/01_models.md", "Ключевые термины"),
            TheorySectionSpec("classic_ml/01_models.md", "Линейная и полиномиальная регрессия"),
            TheorySectionSpec("classic_ml/01_models.md", "Логистическая регрессия"),
            TheorySectionSpec("classic_ml/01_models.md", "Метод опорных векторов (SVM)"),
            TheorySectionSpec("classic_ml/01_models.md", "KNN"),
            TheorySectionSpec("classic_ml/01_models.md", "Деревья решений"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Базовые модели регрессии и классификации", "Линейная и полиномиальная регрессия"),
                ["Линейная и полиномиальная регрессия"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Базовые модели регрессии и классификации", "Логистическая регрессия"),
                ["Логистическая регрессия"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Базовые модели регрессии и классификации", "Метод опорных векторов"),
                ["Метод опорных векторов (SVM)"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Базовые модели регрессии и классификации", "KNN"),
                ["KNN"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Базовые модели регрессии и классификации", "Деревья решений"),
                ["Деревья решений"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="classic_ml/02_ensembles_and_unsupervised.md",
        title="Classic ML: ансамбли, кластеризация и понижение размерности",
        intro="Этот модуль лучше учить как связку методов, которые работают уже не с одной базовой моделью, а с ансамблями и структурой данных без учителя.",
        theory_sections=[
            TheorySectionSpec("classic_ml/02_advanced.md", "Ансамбли моделей"),
            TheorySectionSpec("classic_ml/02_advanced.md", "Кластеризация и понижение размерности"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Ансамбли моделей"),
                ["Ансамбли моделей"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Кластеризация"),
                ["Кластеризация и понижение размерности"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Понижение размерности"),
                ["Кластеризация и понижение размерности"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="classic_ml/03_anomaly_detection.md",
        title="Classic ML: детекция аномалий",
        intro="Это отдельный тяжёлый блок, который удобнее учить отдельно от остального classic ML. Здесь важно держать в голове постановку задачи, типы методов и выбор порога.",
        theory_sections=[
            TheorySectionSpec("classic_ml/02_advanced.md", "Детекция аномалий"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Детекция аномалий"),
                ["Детекция аномалий"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="classic_ml/04_ml_fundamentals.md",
        title="Classic ML: общая теория и работа с данными",
        intro="В этом модуле собраны общие вопросы, которые часто всплывают независимо от конкретной модели: bias-variance, регуляризация, работа с признаками, дисбаланс и общие принципы ML.",
        theory_sections=[
            TheorySectionSpec("classic_ml/02_advanced.md", "Общая ML-теория"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Разное", "Доменные вопросы & дисбаланс"),
                ["Общая ML-теория"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Разное", "Переобучение, недообучение и bias–variance"),
                ["Общая ML-теория"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Разное", "Регуляризация"),
                ["Общая ML-теория"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Разное", "Градиентный спуск & аналитические решения"),
                ["Общая ML-теория"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Разное", "Выбор признаков и работа с данными"),
                ["Общая ML-теория"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Разное", "Общие ML-концепции"),
                ["Общая ML-теория"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="recsys/01_handbook.md",
        title="Recsys, Search and Retrieval Handbook",
        intro="Этот модуль удобнее учить отдельно от общего classic ML, потому что retrieval и ranking образуют свой инженерный стек: кандидаты, индекс, ранжирование, latency и метрики.",
        theory_sections=[
            TheorySectionSpec("recsys/01_handbook.md", "Collaborative Filtering и ALS"),
            TheorySectionSpec("recsys/01_handbook.md", "ANN и векторный поиск"),
            TheorySectionSpec("recsys/01_handbook.md", "Retrieval, ranking и two-tower"),
            TheorySectionSpec("recsys/01_handbook.md", "Search system design"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Ранжирование и рекомендации", "Общие вопросы по рексистемам и CF"),
                ["Collaborative Filtering и ALS"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Ранжирование и рекомендации", "Ретривал / ANN (FAISS)"),
                ["ANN и векторный поиск"],
            ),
            NotebookGroupSpec(
                ("Classic Machine Learning (ML)", "Ранжирование и рекомендации", "Двухбашенные модели (Two-Tower)"),
                ["Retrieval, ranking и two-tower", "Search system design"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="deep_learning/01_core.md",
        title="Deep Learning: core",
        intro="Это базовый DL-модуль: как обучаются нейросети, что происходит с оптимизацией, нормализацией и регуляризацией, и какие продовые вопросы отсюда вырастают.",
        theory_sections=[
            TheorySectionSpec("deep_learning/01_core.md", "Как в целом обучаются нейросети"),
            TheorySectionSpec("deep_learning/01_core.md", "Регуляризация и нормализация"),
            TheorySectionSpec("deep_learning/01_core.md", "Batch Normalization"),
            TheorySectionSpec("deep_learning/01_core.md", "Градиентный спуск и оптимизаторы"),
            TheorySectionSpec("deep_learning/01_core.md", "Функции активации"),
            TheorySectionSpec("deep_learning/01_core.md", "Distributed training"),
            TheorySectionSpec("deep_learning/01_core.md", "Разное"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "General", "Регуляризация в нейросетях"),
                ["Регуляризация и нормализация"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "General", "Batch Normalization"),
                ["Batch Normalization"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "General", "Градиентный спуск"),
                ["Градиентный спуск и оптимизаторы"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "General", "Функции активации"),
                ["Функции активации"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "General", "Распределёное обучение"),
                ["Distributed training"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "General", "Разное"),
                [
                    "Разное",
                    "Как в целом обучаются нейросети",
                    "Регуляризация и нормализация",
                    "Batch Normalization",
                    "Градиентный спуск и оптимизаторы",
                    "Функции активации",
                ],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="nlp_llm/01_text_and_tokenization.md",
        title="NLP / LLM: представление текста и токенизация",
        intro="Это первый NLP-модуль. Его лучше проходить отдельно, потому что здесь закладывается весь фундамент: как текст подаётся в модель, как строятся эмбеддинги и как работает токенизация.",
        theory_sections=[
            TheorySectionSpec("nlp_llm/01_handbook.md", "Представление текста и базовый NLP"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "Токенизация"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Общее"),
                ["Представление текста и базовый NLP"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Токенайзер"),
                ["Токенизация"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="nlp_llm/02_transformers_and_architectures.md",
        title="NLP / LLM: архитектуры, attention и transformers",
        intro="Этот модуль стоит учить как самостоятельный пласт: именно здесь находится большая часть архитектурных вопросов про attention, позиционное кодирование и типы трансформеров.",
        theory_sections=[
            TheorySectionSpec("nlp_llm/01_handbook.md", "Теория и архитектуры NLP"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "Transformer подробно"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "Ускорение Transformer"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "Эмбеддинги и tricky-вопросы"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Теория и архитектуры NLP"),
                ["Теория и архитектуры NLP"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Tricky"),
                ["Эмбеддинги и tricky-вопросы"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Transformer"),
                ["Transformer подробно"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Ускорение Transformer"),
                ["Ускорение Transformer"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Разное"),
                ["Transformer подробно", "Ускорение Transformer", "Эмбеддинги и tricky-вопросы", "Методы дообучения и LoRA"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="nlp_llm/03_inference_prompting_and_llm.md",
        title="NLP / LLM: инференс, prompting и общая картина LLM",
        intro="Это модуль про использование LLM на практике: как модель генерирует, как ею управлять через prompting и structured output, и как понимать базовую картину decoder-only систем.",
        theory_sections=[
            TheorySectionSpec("nlp_llm/01_handbook.md", "Инференс и декодирование"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "Метрики и базовый анализ NLP-моделей"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "LLM как инструмент"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "Prompting и structured output"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "LLM: общая картина"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Инференс"),
                ["Инференс и декодирование"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Метрики и анализ моделей NLP"),
                ["Метрики и базовый анализ NLP-моделей"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Задачи для LLM"),
                ["LLM как инструмент"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Prompting и structured output"),
                ["Prompting и structured output"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "LLM"),
                ["LLM: общая картина"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="nlp_llm/04_finetuning_and_lora.md",
        title="NLP / LLM: дообучение, SFT и LoRA",
        intro="Этот модуль собран отдельно, потому что fine-tuning и parameter-efficient adaptation очень удобно повторять как единый блок: SFT, LoRA, адаптеры, граф вычислений и training setup.",
        theory_sections=[
            TheorySectionSpec("nlp_llm/01_handbook.md", "Обучение и дообучение LLM"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "Методы дообучения и LoRA"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Оптимизация и обучение LLM"),
                ["Обучение и дообучение LLM"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Методы дообучения моделей"),
                ["Методы дообучения и LoRA"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "LoRA"),
                ["Методы дообучения и LoRA"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="nlp_llm/05_generation_and_summarization.md",
        title="NLP / LLM: генерация и суммаризация",
        intro="Суммаризация и управляемая генерация лучше запоминаются отдельным модулем: здесь полезно держать в голове и training pipeline, и decoding, и ограничения автоматических метрик.",
        theory_sections=[
            TheorySectionSpec("nlp_llm/01_handbook.md", "Суммаризация и генерация"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Суммаризация и генерация"),
                ["Суммаризация и генерация"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="nlp_llm/06_rag.md",
        title="NLP / LLM: RAG",
        intro="RAG слишком объёмен для большого общего NLP-файла, поэтому этот модуль лучше учить отдельно: retrieval, reranking, chunking, evaluation и продуктовая архитектура.",
        theory_sections=[
            TheorySectionSpec("nlp_llm/01_handbook.md", "RAG"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "RAG"),
                ["RAG"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="nlp_llm/07_agents_and_economics.md",
        title="NLP / LLM: агенты и экономика",
        intro="В этом модуле собраны оркестрация, multi-agent patterns, tools и экономическая сторона LLM-систем. Эти темы хорошо учатся вместе, потому что обе уже находятся на уровне системы, а не отдельной модели.",
        theory_sections=[
            TheorySectionSpec("nlp_llm/01_handbook.md", "AI Agents"),
            TheorySectionSpec("nlp_llm/01_handbook.md", "Экономическая целесообразность"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "AI Agents"),
                ["AI Agents"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Nature Language Processing (NLP)", "Экономическая целесообразность"),
                ["Экономическая целесообразность"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="cv/01_handbook.md",
        title="Computer Vision Handbook",
        intro="CV-модуль остаётся цельным: внутри уже есть понятная логика от свёрток к архитектурам, attention в vision и трекингу.",
        theory_sections=[
            TheorySectionSpec("cv/01_handbook.md", "База по свёрткам"),
            TheorySectionSpec("cv/01_handbook.md", "Архитектуры"),
            TheorySectionSpec("cv/01_handbook.md", "Vision Transformers и attention в CV"),
            TheorySectionSpec("cv/01_handbook.md", "Сегментация и задачи CV"),
            TheorySectionSpec("cv/01_handbook.md", "Трекинг"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Computer Vision (CV)", "Свертки"),
                ["База по свёрткам"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Computer Vision (CV)", "Архитектуры нейросетей"),
                ["Архитектуры"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Computer Vision (CV)", "Transformers и Attention"),
                ["Vision Transformers и attention в CV"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Computer Vision (CV)", "Трекинг"),
                ["Трекинг"],
            ),
            NotebookGroupSpec(
                ("Deep Learning (DL)", "Computer Vision (CV)", "Разное"),
                ["Сегментация и задачи CV"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="metrics/01_handbook.md",
        title="Metrics and Loss Functions Handbook",
        intro="Модуль по метрикам лучше пока оставить единым справочником: его чаще учат как reference, а не как линейный учебник. Но вопросы в конце собраны точно по исходным формулировкам из ноутбука.",
        theory_sections=[
            TheorySectionSpec("metrics/01_handbook.md", "Функции потерь"),
            TheorySectionSpec("metrics/01_handbook.md", "Метрики бинарной классификации"),
            TheorySectionSpec("metrics/01_handbook.md", "Мультиклассовая классификация"),
            TheorySectionSpec("metrics/01_handbook.md", "Метрики регрессии"),
            TheorySectionSpec("metrics/01_handbook.md", "Метрики ранжирования"),
            TheorySectionSpec("metrics/01_handbook.md", "Метрики кластеризации"),
            TheorySectionSpec("metrics/01_handbook.md", "Метрики CV"),
            TheorySectionSpec("metrics/01_handbook.md", "Метрики NLP"),
            TheorySectionSpec("metrics/01_handbook.md", "Пороги и модерация"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Metrics and loss functions", "Функции потерь"),
                ["Функции потерь"],
            ),
            NotebookGroupSpec(
                ("Metrics and loss functions", "Метрики классификации", "Бинарная классификация"),
                ["Метрики бинарной классификации"],
            ),
            NotebookGroupSpec(
                ("Metrics and loss functions", "Метрики классификации", "Мльтиклассовая классификация"),
                ["Мультиклассовая классификация"],
            ),
            NotebookGroupSpec(
                ("Metrics and loss functions", "Метрики классификации", "Метрики регрессии"),
                ["Метрики регрессии"],
            ),
            NotebookGroupSpec(
                ("Metrics and loss functions", "Метрики ранжирования"),
                ["Метрики ранжирования"],
            ),
            NotebookGroupSpec(
                ("Metrics and loss functions", "Метрики ранжирования", "Метрики кластеризации"),
                ["Метрики кластеризации"],
            ),
            NotebookGroupSpec(
                ("Metrics and loss functions", "Метрики ранжирования", "Метрики CV"),
                ["Метрики CV"],
            ),
            NotebookGroupSpec(
                ("Metrics and loss functions", "Метрики ранжирования", "Метрики NLP"),
                ["Метрики NLP"],
            ),
            NotebookGroupSpec(
                ("Metrics and loss functions", "Метрики ранжирования", "Разное"),
                ["Пороги и модерация"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="python/01_handbook.md",
        title="Python Handbook for ML Engineer Interviews",
        intro="Python-модуль пока оставляю цельным, потому что вопросы из ноутбука уже перемешивают язык, память, concurrency и задачки. В конце собраны точные вопросы из ноутбука по исходным формулировкам.",
        theory_sections=[
            TheorySectionSpec("python/01_handbook.md", "База языка"),
            TheorySectionSpec("python/01_handbook.md", "Функции, декораторы, контекстные менеджеры"),
            TheorySectionSpec("python/01_handbook.md", "ООП и data model"),
            TheorySectionSpec("python/01_handbook.md", "Итераторы и генераторы"),
            TheorySectionSpec("python/01_handbook.md", "Асинхронность, потоки, процессы"),
            TheorySectionSpec("python/01_handbook.md", "Память и GC"),
            TheorySectionSpec("python/01_handbook.md", "Практические инженерные вопросы"),
            TheorySectionSpec("python/01_handbook.md", "Небольшие coding patterns"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Python",),
                ["Асинхронность, потоки, процессы", "Практические инженерные вопросы"],
                title_override="Python: общие вопросы",
            ),
            NotebookGroupSpec(
                ("Python", "Типы данных"),
                [
                    "База языка",
                    "Функции, декораторы, контекстные менеджеры",
                    "ООП и data model",
                    "Итераторы и генераторы",
                    "Асинхронность, потоки, процессы",
                    "Память и GC",
                    "Практические инженерные вопросы",
                    "Небольшие coding patterns",
                ],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="databases/01_handbook.md",
        title="Databases Handbook",
        intro="Короткий модуль по БД оставляю единым: это удобнее как справочник и он уже достаточно компактный.",
        theory_sections=[
            TheorySectionSpec("databases/01_handbook.md", "Основы"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Databases",),
                ["Основы"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="production/01_handbook.md",
        title="Production Handbook",
        intro="Продовый модуль тоже лучше оставлять цельным: он короткий и логически идёт от контейнеризации к архитектуре и concurrency.",
        theory_sections=[
            TheorySectionSpec("production/01_handbook.md", "Контейнеризация"),
            TheorySectionSpec("production/01_handbook.md", "Архитектура сервисов"),
            TheorySectionSpec("production/01_handbook.md", "Async, threads, processes"),
            TheorySectionSpec("production/01_handbook.md", "Практический сценарий"),
            TheorySectionSpec("production/01_handbook.md", "Базы данных в проде"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Production",),
                ["Контейнеризация", "Архитектура сервисов", "Async, threads, processes", "Практический сценарий", "Базы данных в проде"],
            ),
        ],
    ),
    StudyModuleSpec(
        output_rel="statistics/01_handbook.md",
        title="Statistics and Probability Handbook",
        intro="Статистику пока тоже оставляю единым модулем: здесь важнее цельная цепочка от гипотез и p-value до мощности теста и выбора критерия.",
        theory_sections=[
            TheorySectionSpec("statistics/01_handbook.md", "Базовые определения"),
            TheorySectionSpec("statistics/01_handbook.md", "Закон больших чисел и ЦПТ"),
            TheorySectionSpec("statistics/01_handbook.md", "Проверка гипотез"),
            TheorySectionSpec("statistics/01_handbook.md", "Планирование эксперимента"),
            TheorySectionSpec("statistics/01_handbook.md", "Статистические критерии"),
            TheorySectionSpec("statistics/01_handbook.md", "Прочие вопросы"),
        ],
        notebook_groups=[
            NotebookGroupSpec(
                ("Statistics and Probability", "Какие тесты используются для сравнения выборок?"),
                ["Базовые определения", "Закон больших чисел и ЦПТ", "Проверка гипотез", "Планирование эксперимента", "Статистические критерии", "Прочие вопросы"],
            ),
        ],
    ),
]


def module_sort_key(spec: StudyModuleSpec) -> tuple[int, str]:
    category = spec.output_rel.split("/", 1)[0]
    order = CATEGORY_ORDER_INDEX.get(category, len(CATEGORY_ORDER_INDEX) + 1)
    return (order, spec.output_rel)


def ordered_module_specs() -> list[StudyModuleSpec]:
    return sorted(MODULE_SPECS, key=module_sort_key)

QUESTION_ALIAS_TITLES: dict[str, list[str]] = {
    "Где “градиент” в градиентном бустинге и какая целевая переменная у n-ого дерева?": [
        "На что обучается N+1-е дерево в градиентном бустинге?",
        "Градиент чего используется в градиентном бустинге?",
    ],
    "Почему не пользуемся аналитической формулой при решении задачи регрессии со среднеквадратичной ошибкой, а пользуемся градиентным спуском? Что здесь самое тяжелое в плане вычислений? Может быть еще какие-нибудь минусы есть?": [
        "Почему для регрессии с MSE часто используют градиентный спуск, а не аналитическую формулу?",
    ],
    "Какой глубины деревья используются в случайном лесе и в градиентном бустинге? Насколько бы мы ограничивали глубину в обоих вариантах?": [
        "Какой глубины деревья используются в случайном лесе и в градиентном бустинге?",
    ],
    "Есть случайный лес, есть градиентный бустинг, почему в промышленной среде, особенно в задачах, где нужен быстрый инференс, используют бустинг, а не случайный лес?": [
        "Почему в продакшене для быстрого инференса часто предпочитают бустинг, а не случайный лес?",
    ],
    "Предстваим, что мы хотим обучаться на батч сайз 2048, но мало памяти и хватает только на батч сайз 32. Как можем поступить, чтобы приблизиться к картинке с батч сайз 2048?": [
        "Предстваим, что мы хотим обучаться на batch size 2048, но хватает памяти только на 32. Как поступить?",
    ],
    "Задача классификации изображений на kaggle, получилась некоторая модель на свёрточной нейронной сети, хочется выжать из нее максимальный скор, при этом не переобучая ее?": [
        "Есть CNN-модель на Kaggle, хочется выжать максимум, но не переобучить. Что делать?",
    ],
    "Как обучаются нейронки? Полный процесс от инициализации до финального результата.": [
        "Как в целом обучаются нейросети",
    ],
    "Как разбивать текст на чанки?": [
        "Chunking Strategies",
    ],
    "Какие алгоритмы поиска использовать (например, ANN + косинусная близость)?": [
        "FAISS: как работает, что внутри",
        "Какие знаешь виды ANN?",
    ],
    "Какие этапы в работе токенайзера есть?": [
        "Как работает токенайзер? Какие этапы есть?",
    ],
    "Зачем нужен positional encoding в трансформере?": [
        "Что такое positional encoding в трансформерах?",
    ],
    "Меняется ли эмбеддинг токена в зависимости от его позиции в предложении?": [
        "Какие способы позиционного кодирования знаешь? Меняется ли эмбеддинг токена в зависимости от позиции?",
    ],
    "Как распараллелить обработку миллиарда событий с BERT, чтобы уложиться хотя бы в час?": [
        "Как распараллелить обработку миллиарда событий с BERT, чтобы уложиться хотя бы в час?",
    ],
    "Расскажи про трансформер: как работает, что внутри происходит?": [
        "Расскажи про архитектуры трансформера и из каких частей они состоят",
    ],
    "Расскажите про трансформер: как он устроен и что внутри происходит": [
        "Расскажи про архитектуры трансформера и из каких частей они состоят",
    ],
    "Почему BatchNorm сложно применять при обучении трансформеров?": [
        "Зачем в трансформере используется LayerNorm вместо BatchNorm? Почему BatchNorm сложно применять?",
    ],
    "Сложность attention (O(n²)), какие есть оптимизации?": [
        "Какие ограничения у attention? Сложность \\(O(n^2)\\), способы ускорения, flash-attention",
    ],
    "Какие ограничения у attention? Сложность – O(n²), способы ускорения, flash-attention": [
        "Какие ограничения у attention? Сложность \\(O(n^2)\\), способы ускорения, flash-attention",
    ],
    "Как рассчитывается TF-IDF?": [
        "Что такое TF-IDF и как считается?",
    ],
    "Пример: задать правильный промпт (\"Есть ли мат в данном предложении {предложение}? Ответь да или нет\")": [
        "Как заставить LLM выполнять любую задачу, допустим классификацию?",
    ],
    "Задать промпт с правилом.": [
        "Как заставить LLM выполнять любую задачу, допустим классификацию?",
    ],
    "Что такое SFT, LoRA, дистилляция, pruning?": [
        "Что такое SFT, LoRA, дистилляция, pruning?",
    ],
    "Structured output (наивный и продвинутый варианты).": [
        "Как влиять на генерацию ответа при инференсе LLM? Температура, Beam-search, Prompt engineering, Structured output",
    ],
    "Как обучал эмбеддинги (роберта + триплет-лосс)?": [
        "Как мы обучаем эмбеддер? Как обучал эмбеддинги (RoBERTa + triplet loss)?",
    ],
    "Какие оффлайн-метрики можно использовать (BLEU, Rouge, Similarity)?": [
        "Как оценивать качество ответа модели в оффлайне и онлайне?",
    ],
    "Какие метрики применяются для оценки генерации итогового ответа?": [
        "Как оценивать качество ответа модели в оффлайне и онлайне?",
    ],
    "Reflixion": [
        "Какие паттерны создания агентов знаешь? Act, ReAct, Reflexion, Planning, Planning + ReAct + Reflect",
    ],
    "Planing": [
        "Какие паттерны создания агентов знаешь? Act, ReAct, Reflexion, Planning, Planning + ReAct + Reflect",
    ],
    "Planing + ReAct + Reflect": [
        "Какие паттерны создания агентов знаешь? Act, ReAct, Reflexion, Planning, Planning + ReAct + Reflect",
    ],
    "Crew AI": [
        "Какие библиотеки для создания агентов знаешь? LangGraph, smolagents, CrewAI",
    ],
    "Как считать mAP в задаче детекции объектов?": [
        "Детекция: mAP при различных порогах IoU. Как считать mAP?",
    ],
    "Какие типы являются изменяемыми (list, dict, set) и какие — неизменяемыми (числа, строки, tuple и др.)? В чём их различие? (ссылочная модель данных, присваивание, copy vs deepcopy)": [
        "Какие типы являются изменяемыми (list, dict, set) и какие — неизменяемыми (числа, строки, tuple и др.)? В чём их различие? (ссылочная модель данных, присваивание, copy vs deepcopy)",
    ],
    "Что такое GIL и почему Python называют однопоточным?": [
        "Почему в Python нет полноценной многопоточности? Для чего нужен GIL?",
    ],
    "Зачем вообще нужен мультитрединг, если есть гил, который блокирует исполнение больше чем одного треда внутри одного процесса?": [
        "Зачем вообще нужен мультитрединг, если есть GIL?",
    ],
    "Уровень значимости (α): Обычно выбирается 5% (или 0,05), что означает, что вероятность ошибочно отклонить нулевую гипотезу (ложноположительный результат) равна 5%.": [
        "Что такое уровень значимости \\(\\alpha\\) и как он связан с ошибками I и II рода?",
    ],
    "Мощность теста (1−β): Мощность теста обычно составляет 80% или 90%. Она показывает вероятность обнаружения реального эффекта, если он существует.": [
        "Что такое статистическая мощность теста и почему она важна?",
    ],
    "Центральная предельная теорема (ЦПТ): при достаточно большом размере выборки распределение средних значений случайных выборок из любого распределения (с конечной дисперсией) будет стремиться к нормальному распределению. Это справедливо вне зависимости от начального распределения данных.": [
        "Что такое центральная предельная теорема (ЦПТ) и закон больших чисел (ЗБЧ)?",
    ],
    "Закон больших чисел: по мере увеличения размера выборки среднее значение выборки приближается к математическому ожиданию генеральной совокупности. Это означает, что среднее значение выборки становится более точным представлением среднего значения всей популяции при увеличении количества наблюдений.": [
        "Что такое центральная предельная теорема (ЦПТ) и закон больших чисел (ЗБЧ)?",
    ],
    "Есть функция y = x³ - 2x² + 100 — как обучить нейросеть находить y для любых x, если функции активации линейные?": [
        "Есть функция \\(y=x^3 - 2x^2 + 100\\). Как обучить нейросеть находить \\(y\\) для любых \\(x\\), если функции активации линейные?",
    ],
}

QUESTION_MANUAL_ANSWERS: dict[str, str] = {
    "Что будет с bias/variance при:": "Это вводный вопрос к трём частным случаям ниже. На собеседовании после этой фразы обычно отдельно разбирают, что произойдёт при увеличении `K` в KNN, ограничении глубины дерева и использовании dropout.",
    "Продвинутое использование Python": "Это скорее маркер следующего блока вопросов, а не самостоятельный теоретический вопрос. Обычно после него спрашивают про межпроцессное взаимодействие, работу с API, type hints и небольшие алгоритмические задачи.",
    "Какие типы являются изменяемыми (list, dict, set) и какие — неизменяемыми (числа, строки, tuple и др.)? В чём их различие? (ссылочная модель данных, присваивание, copy vs deepcopy)": "Изменяемые типы можно менять на месте, и это изменение увидят все ссылки на тот же объект. Классические примеры: `list`, `dict`, `set`. Неизменяемые типы нельзя менять на месте, при 'изменении' создаётся новый объект: `int`, `float`, `str`, `tuple`. Это важно из-за ссылочной модели Python и разницы между присваиванием, `copy` и `deepcopy`.",
}


def get_section(source_file: str, section_title: str) -> SourceSection:
    module = SOURCE_MODULES[source_file]
    if section_title not in module.sections:
        raise KeyError(f"Section '{section_title}' not found in {source_file}")
    return module.sections[section_title]


def find_subsection_answer_by_title(title: str) -> str | None:
    target = normalize(title)
    for source_module in SOURCE_MODULES.values():
        for section in source_module.sections.values():
            for subsection in section.subsections:
                sub_norm = normalize(subsection.title)
                if sub_norm == target or (target and (target in sub_norm or sub_norm in target)):
                    return subsection.body.strip()
    return None


def find_section_theory_by_title(title: str) -> str | None:
    target = normalize(title)
    for source_module in SOURCE_MODULES.values():
        for section in source_module.sections.values():
            sec_norm = normalize(section.title)
            if sec_norm == target or (target and (target in sec_norm or sec_norm in target)):
                theory = section.theory_text().strip()
                if theory:
                    return theory
    return None


def find_best_answer(question: str, sections: list[SourceSection]) -> tuple[str, str]:
    if question in QUESTION_MANUAL_ANSWERS:
        return "matched", QUESTION_MANUAL_ANSWERS[question]

    for alias_title in QUESTION_ALIAS_TITLES.get(question, []):
        alias_answer = find_subsection_answer_by_title(alias_title)
        if alias_answer:
            return "matched", alias_answer
        section_answer = find_section_theory_by_title(alias_title)
        if section_answer:
            return "matched", section_answer

    q_norm = normalize(question)
    q_tokens = tokenize(question)

    candidates: list[tuple[float, str]] = []
    for section in sections:
        for subsection in section.subsections:
            title_norm = normalize(subsection.title)
            title_tokens = tokenize(subsection.title)
            body_norm = normalize(subsection.body)
            score = 0.0

            if q_norm == title_norm:
                score = 1.0
            elif q_norm and (q_norm in title_norm or title_norm in q_norm):
                score = 0.95
            else:
                if q_tokens:
                    token_overlap = len(q_tokens & title_tokens) / max(1, len(q_tokens))
                    if token_overlap > score:
                        score = token_overlap * 0.9
                    if len(q_tokens) == 1:
                        token = next(iter(q_tokens))
                        if token in title_tokens:
                            score = max(score, 0.92)
                        elif token and token in body_norm.split():
                            score = max(score, 0.75)
                ratio = SequenceMatcher(None, q_norm, title_norm).ratio()
                score = max(score, ratio)

            if score > 0:
                candidates.append((score, subsection.body))

    if candidates:
        score, answer = max(candidates, key=lambda x: x[0])
        if score >= 0.55:
            label = "exact" if score >= 0.99 else "matched"
            return label, answer.strip()

    fallback_chunks: list[str] = []
    for section in sections:
        theory = section.theory_text()
        if theory:
            fallback_chunks.append(theory)
    fallback = "\n\n".join(fallback_chunks).strip()
    if not fallback:
        fallback = "Ответ по этому вопросу лучше восстанавливать из общей теории модуля. Отдельный короткий ответ ещё стоит дописать вручную."
    return "fallback", fallback


def render_details(question: str, answer: str) -> str:
    return "\n".join(
        [
            "<details>",
            f"<summary>{question}</summary>",
            "",
            answer.strip(),
            "",
            "</details>",
        ]
    )


def collect_candidate_sections(spec: StudyModuleSpec, group_spec: NotebookGroupSpec) -> list[SourceSection]:
    candidates: list[SourceSection] = []
    for section_title in group_spec.source_sections:
        for theory_ref in spec.theory_sections:
            source_module = SOURCE_MODULES[theory_ref.source_file]
            if section_title in source_module.sections:
                section = source_module.sections[section_title]
                if section not in candidates:
                    candidates.append(section)
        for source_module in SOURCE_MODULES.values():
            if section_title in source_module.sections:
                section = source_module.sections[section_title]
                if section not in candidates:
                    candidates.append(section)
    if not candidates:
        for theory_ref in spec.theory_sections:
            section = get_section(theory_ref.source_file, theory_ref.section_title)
            if section not in candidates:
                candidates.append(section)
    return candidates


def render_study_module(spec: StudyModuleSpec, stats: dict[str, int]) -> str:
    lines = [
        f"# {spec.title}",
        "",
        "> Study-версия модуля: сначала учебная часть, потом все точные вопросы из ноутбука в конце модуля.",
        "",
        spec.intro.strip(),
        "",
        "## Учебник",
        "",
    ]

    for theory_ref in spec.theory_sections:
        section = get_section(theory_ref.source_file, theory_ref.section_title)
        lines.append(f"### {section.title}")
        lines.append("")
        theory_text = section.theory_text()
        if theory_text:
            lines.append(theory_text)
        else:
            lines.append("Короткая учебная часть по этому блоку пока сводится к вопросам ниже.")
        lines.append("")

    lines.extend(["## Вопросы из ноутбука", ""])

    for group_spec in spec.notebook_groups:
        group = NOTEBOOK_GROUPS.get(group_spec.path)
        if not group:
            lines.append(f"### {group_spec.title_override or group_spec.path[-1]}")
            lines.append("")
            lines.append("В исходном ноутбуке эта группа не нашлась при автоматическом разборе.")
            lines.append("")
            continue

        group_title = group_spec.title_override or group_spec.path[-1]
        candidate_sections = collect_candidate_sections(spec, group_spec)

        lines.append(f"### {group_title}")
        lines.append("")
        for question in group.questions:
            status, answer = find_best_answer(question, candidate_sections)
            stats["questions"] += 1
            stats[status] += 1
            lines.append(render_details(question, answer))
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_readme() -> None:
    lines = [
        "# Study Version",
        "",
        "Это учебная сборка модулей: в каждом файле сначала идёт теория, а в самом конце модуля собраны точные вопросы из ноутбука с раскрывающимися ответами.",
        "",
        "Рекомендуемый режим:",
        "",
        "1. Пройти учебную часть модуля сверху вниз.",
        "2. Потом перейти к блоку `Вопросы из ноутбука` в конце файла.",
        "3. Пробовать ответить самому и только потом раскрывать `<details>`.",
        "",
        "Основные файлы:",
        "",
    ]
    for spec in ordered_module_specs():
        rel = spec.output_rel
        target = STUDY_ROOT / rel
        lines.append(f"- [{rel}]({target.as_posix()})")
    lines.append("")
    lines.append("- [HANDBOOK.md](" + (STUDY_ROOT / "HANDBOOK.md").as_posix() + ")")
    (STUDY_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_modules() -> dict[str, int]:
    stats = {"questions": 0, "exact": 0, "matched": 0, "fallback": 0}
    for spec in ordered_module_specs():
        target = STUDY_ROOT / spec.output_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_study_module(spec, stats), encoding="utf-8")
    return stats


def build_handbook() -> None:
    output = STUDY_ROOT / "HANDBOOK.md"
    parts = ["# ML Interview Study Handbook\n"]
    for spec in ordered_module_specs():
        target = STUDY_ROOT / spec.output_rel
        parts.append(f"\n\n---\n\n<!-- source: {target.relative_to(ROOT)} -->\n\n")
        parts.append(target.read_text(encoding="utf-8").strip())
        parts.append("\n")
    output.write_text("".join(parts), encoding="utf-8")


def main() -> None:
    stats = build_modules()
    build_readme()
    build_handbook()
    print(f"Built study modules under {STUDY_ROOT.relative_to(ROOT)}")
    print(
        "coverage",
        json.dumps(
            {
                "questions": stats["questions"],
                "exact": stats["exact"],
                "matched": stats["matched"],
                "fallback": stats["fallback"],
            },
            ensure_ascii=False,
        ),
    )


if __name__ == "__main__":
    main()
