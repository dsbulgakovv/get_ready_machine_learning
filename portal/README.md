# Portal

Это статический сайт для повторения ML interview modules с телефона и компьютера.

## Как пересобрать

```bash
python3 scripts/build_study_modules.py
python3 scripts/build_portal.py
```

## Как открыть локально

```bash
cd portal
python3 -m http.server 8000
```

Потом открыть `http://localhost:8000`.

## Как деплоить

- Если репозиторий уже лежит на GitHub, удобнее всего включить GitHub Pages и использовать workflow из `.github/workflows/deploy-portal.yml`.
- Если хочешь максимально быстрый внешний хостинг с предпросмотрами и отдельным доменом, удобно использовать Cloudflare Pages.
- Для Cloudflare Pages можно собрать портал локально и публиковать папку `portal/` как статический output.

Для деплоя обычно публикуют содержимое папки `portal/`.
