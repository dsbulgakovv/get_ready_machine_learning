# get_ready_machine_learning

Knowledge base and study portal for ML / MLE interview preparation.

## Main materials

- `knowledge_base/` contains the source handbook modules in Markdown with LaTeX formulas.
- `knowledge_base/study/` contains the study-oriented version: theory first, then exact notebook questions with collapsible answers.
- `portal/` is the generated static website for phone and desktop repetition.

## Build

```bash
python3 scripts/build_study_modules.py
python3 scripts/build_handbook.py
python3 scripts/build_portal.py
```

## Open locally

```bash
cd portal
python3 -m http.server 8000
```

Then open `http://localhost:8000`.
