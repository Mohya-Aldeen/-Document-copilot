# Document Copilot

An internal AI chatbot that lets analysts query a corpus of SEC filings in plain English and receive sourced, citable answers.

## Live Demo

- **Frontend:** [Add your Vercel URL]
- **Backend health:** [Add your Render URL]/health

> The free Render backend may take approximately 30–60 seconds to wake up after inactivity. The first request can be slow.

## Architecture

```text
React + Vite (Vercel)
        |
        | HTTPS + Supabase Auth JWT
        v
FastAPI (Render)
   |           |
   v           v
Supabase     OpenAI
Postgres     Chat + embeddings
(pgvector)   (LLM + vectorization)
```

## Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript + Vite |
| Backend | Python 3.12 + FastAPI + Uvicorn |
| Database | Supabase PostgreSQL + pgvector |
| Authentication | Supabase Auth |
| Retrieval | Hybrid vector + full-text search |
| LLM | OpenAI |
| Embeddings | OpenAI `text-embedding-3-small` |
| Frontend hosting | Vercel |
| Backend hosting | Render free Web Service |

## Screenshots

Add 3–4 screenshots here:

1. Sign-in / sign-up screen
2. Main chat interface
3. Answer with source citations
4. Evidence / filing passage panel

## Required environment variables

### Frontend (Vercel)

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Public Render backend URL, without trailing slash |
| `VITE_SUPABASE_URL` | Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase publishable/anon key only |

Only the Supabase anon/publishable key belongs in the browser. Never expose the service-role key, database password, or OpenAI key in frontend variables.

### Backend (Render)

| Variable | Purpose |
|---|---|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_ANON_KEY` | Supabase anon/publishable key |
| `SUPABASE_SERVICE_ROLE_KEY` | Backend-only privileged Supabase key |
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | Backend-only OpenAI API key |
| `OPENAI_CHAT_MODEL` | Chat model (default: `gpt-4o-mini`) |
| `OPENAI_EMBEDDING_MODEL` | Embedding model (default: `text-embedding-3-small`) |
| `OPENAI_EMBEDDING_DIMENSIONS` | Embedding dimensions (default: `1536`) |
| `ASSISTANT_MAX_TOOL_ROUNDS` | Maximum agent tool rounds (default: `24`) |
| `INGEST_CHUNK_MAX_TOKENS` | Ingestion chunk token budget (default: `512`) |
| `ALLOWED_ORIGINS` | Comma-separated allowed frontend origins |

Render supplies `PORT` automatically. The backend also accepts `PORT` locally (default `8000`).

## Local setup

### Backend

From `backend/`:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Fill the backend environment variables in `.env` before starting the API. Never commit `.env`.

### Frontend

From `frontend/`:

```bash
corepack enable
pnpm install --frozen-lockfile
cp .env.example .env
pnpm build
pnpm dev
```

Set `VITE_API_BASE_URL`, `VITE_SUPABASE_URL`, and `VITE_SUPABASE_ANON_KEY` in the frontend environment.

## Deployment

- **Vercel:** Import this repository and set the Root Directory to `frontend`. Framework preset: Vite. Build command: `pnpm build`. Output directory: `dist`.
- **Render:** Create a Blueprint from the root `render.yaml`, or create a Python Web Service with Root Directory `backend`, build command `pip install -r requirements.txt`, and start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- **Supabase:** Resume the existing project and confirm Auth settings before testing sign-up.

## Free-tier notes

Free hosting tiers have limits and are not guaranteed to remain continuously available. Render free web services can sleep after inactivity; the first request after sleep can be delayed. GitHub Actions scheduled workflows can be delayed or skipped, so keep-alive pings are best-effort, not an uptime guarantee. Supabase free projects can pause under their inactivity policy; a daily lightweight API/database request may help demonstrate activity but does not guarantee the project will never pause. Provider quotas, usage limits, and free-tier policies can change.

## Project background

Document Copilot is a demonstration of an internal research assistant for a fictional investment research firm. It answers questions using a defined corpus of SEC filings, cites supporting passages, and avoids unsupported claims or investment advice.
