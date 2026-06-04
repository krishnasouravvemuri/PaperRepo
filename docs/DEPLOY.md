# Deploying PaperRepo

Architecture: **Frontend on Vercel · Backend on Render · DB + Storage on Supabase.**

```
Vercel (Next.js UI)  --/api/* proxy-->  Render (Django + DRF)  --pooler-->  Supabase (Postgres + Storage)
```

The frontend proxies `/api/*` to the backend via `DJANGO_ORIGIN`
(see [next.config.js](../frontend/next.config.js)), so cookies stay
same-origin and no CORS/cookie cross-domain config is needed in the browser.

---

## 1. Push the repo to GitHub

```bash
git push origin main
```

## 2. Backend → Render

Two ways:

### Option A — Blueprint (one click)
Repo already has [render.yaml](../render.yaml). In Render: **New → Blueprint →
pick the repo**. It provisions the web service with all non-secret env vars.
Then set the three secrets in the dashboard:
- `SUPABASE_DB_PASSWORD`
- `SUPABASE_SERVICE_KEY`
- `CORS_ALLOWED_ORIGINS` = your Vercel URL (after step 3)

### Option B — Manual
New → Web Service → connect repo:
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
- **Plan:** Free
- **Env vars:** copy from `backend/.env`, but set:
  - `DJANGO_DEBUG=False`
  - `DJANGO_ALLOWED_HOSTS=.onrender.com`
  - `AUTH_COOKIE_SECURE=True`
  - new strong `DJANGO_SECRET_KEY` and `JWT_SECRET`
  - DB host/user/port already point at the Supabase **pooler** (`aws-1-ap-northeast-1...:6543`)

Deploy → note the URL, e.g. `https://paperrepo-api.onrender.com`.

## 3. Frontend → Vercel

New Project → import the repo:
- **Root Directory:** `frontend`
- **Framework:** Next.js (auto-detected)
- **Env var:** `DJANGO_ORIGIN = https://paperrepo-api.onrender.com`

Deploy → note the URL, e.g. `https://paperrepo.vercel.app`.

## 4. Wire CORS back

In Render, set `CORS_ALLOWED_ORIGINS = https://paperrepo.vercel.app` and redeploy.
(The browser talks only to Vercel, but the proxy means Render sees the Vercel
origin on forwarded requests.)

## 5. Verify

- `https://paperrepo.vercel.app` — UI loads
- `https://paperrepo.vercel.app/api/v2/subject_management/` — returns `{"meta":{"code":200,...}}`
- Sign up → log in → upload a small file → download it (downloads with the title as filename).

---

## Notes / gotchas
- **Render free tier sleeps** after ~15 min idle → first request is slow (~30–50s cold start). Upgrade for always-on.
- **Supabase free tier pauses** on inactivity — if the DB host stops resolving, unpause it in the Supabase dashboard.
- **Secrets:** never commit real `DJANGO_SECRET_KEY`, `JWT_SECRET`, `SUPABASE_*` values. `backend/.env` is gitignored.
- DB connection uses the **transaction pooler (port 6543)** — correct for short-lived web requests.

## Why not all-Vercel?
Vercel is serverless: 4.5 MB request-body cap and a short function timeout make
Django file uploads fragile, plus cold starts per request. Render runs Django as
a normal persistent process (gunicorn), so uploads and long requests work without
those limits.
