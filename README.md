# PC Finder Telegram Mini App (MVP)

A minimal production-like MVP for selecting **prebuilt computers** by user task.

Users can:
- choose a predefined category,
- or enter free text (EN/RU),
- get category classification,
- and browse only existing prebuilt PC offers from database.

## Stack
- Python 3.12
- FastAPI
- Jinja2 templates
- Vanilla JS/CSS/HTML
- SQLAlchemy + SQLite
- Uvicorn
- Docker + Docker Compose

## Categories
Predefined category codes:
- `office`
- `study`
- `programming`
- `gaming`
- `video_editing`
- `design_3d`

## Run locally (without Docker)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run with Docker Compose
```bash
cp .env.example .env
docker compose up --build -d
docker compose logs -f
```

Open:
- App: `http://localhost:8000/`
- Admin login: `http://localhost:8000/admin/login`

## Admin login
- Admin password is read from env variable `ADMIN_PASSWORD`.
- Default in `.env.example` is `admin123`.
- Change both `SECRET_KEY` and `ADMIN_PASSWORD` for production.

## Classifier logic
Classifier priority:
1. Uses Hugging Face Inference API if `HUGGINGFACE_API_KEY` is provided.
2. Falls back to built-in keyword classifier (English + Russian) if key is missing/fails.

This means app is fully usable without Hugging Face credentials.

Relevant env:
- `HUGGINGFACE_API_KEY=`
- `HF_MODEL=facebook/bart-large-mnli`

## SQLite persistence
- Database URL default: `sqlite:////data/app.db`
- In Docker Compose, `/data` is a named volume (`app_data`), so DB survives restarts/redeploys.
- DB file in container: `/data/app.db`

## Startup behavior
On app startup:
- creates tables automatically,
- seeds demo computers only if DB is empty,
- seed is idempotent (won't duplicate after restart).

## Where to edit categories
- Category labels/codes: `app/config.py`
- Validation checks in routes/services also reference these codes.

## Where to edit classifier behavior
- Classifier logic and keyword lists: `app/services/classifier.py`
- Add/edit EN/RU keywords in `KEYWORDS` dict.
- Change Hugging Face model via `HF_MODEL` env.

## VPS deployment (single command flow)
1. Copy project to VPS.
2. Install Docker + Compose plugin.
3. Run:
```bash
cp .env.example .env
# edit .env for production secrets
docker compose up --build -d
docker compose logs -f
```

## API routes
- `POST /api/classify`
- `GET /api/computers?category=office`
- `GET /health`

## Telegram Mini App compatibility
- Telegram WebApp script is included in base template.
- JS safely initializes `Telegram.WebApp` when available and still works in normal browser.
