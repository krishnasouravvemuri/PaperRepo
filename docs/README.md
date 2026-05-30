# PaperRepo

Academic resource archive (question papers, important topics, study materials), split into:

- **`backend/`** — Django REST Framework API. Cookie-JWT auth, Supabase Postgres + Supabase Storage (DB stores file paths only). Mirrors the `aiocr_flows` design: thin CBV → service class in each app's `models.py` → `ApiResponse` envelope; all ORM models centralized in `core/client_model_app/models.py`.
- **`frontend/`** — Vite + React (JS) + Tailwind SPA. Feature-folder layout, axios API layer, cookie-based auth.

## Backend

```bash
cd backend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in Supabase creds; leave SUPABASE_DB_PASSWORD empty for local sqlite
python manage.py migrate
python manage.py runserver
```

API root: `http://127.0.0.1:8000/api/v2/`. Apps: `user_management`, `subject_management`,
`question_paper_management`, `important_topic_management`, `material_management`.
File uploads/serving require Supabase Storage env vars (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_BUCKET`).

## Frontend

```bash
cd frontend
npm install
npm run dev          # http://localhost:5173, proxies /api → backend :8000
```

## DB schema (normalized)

`users`, `subjects` (lookup), `faculties` (lookup), `question_papers`, `important_topics`,
`materials`. UUID PKs, `fk_` foreign keys, soft-delete via `*_deleted_at`. Enums
(`exam_type`, `semester`) kept as choice columns.
