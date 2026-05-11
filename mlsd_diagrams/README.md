# ML System Design Diagrams

Здесь лежит база диаграмм для подготовки к ML System Design секции Lead DS / Analytics Developer.

## Что где лежит

- `ml_system_design_lead_ds_plantuml_cheatsheet.md` — исходный markdown с PlantUML-блоками.
- `catalog.json` — учебные пояснения к каждой диаграмме: что проговорить на интервью, термины и короткий ответ.
- `uml/` — отдельные `.uml` файлы, по одному на диаграмму.
- `notes/` — markdown-конспекты к каждой диаграмме.
- `manifest.json` — сгенерированный manifest для сайта.

## Пересобрать UML и заметки

```bash
python3 scripts/build_mlsd_diagrams.py
```

## Отрендерить PDF локально

Нужны Java, Graphviz и PlantUML jar/CLI.

```bash
plantuml -tpdf mlsd_diagrams/uml/*.uml
```

Если используешь jar:

```bash
java -jar plantuml.jar -tpdf mlsd_diagrams/uml/*.uml
```

SVG для сайта сейчас строится через PlantUML server из исходника `.uml`; сами `.uml` остаются локальными и пригодны для отдельного PDF-рендера.
