# KoyunChat

KoyunChat is a lightweight live chat SaaS platform inspired by tawk.to. A customer adds one JavaScript snippet to any website to enable live chat, visitor tracking, AI auto-replies, offline lead collection, multi-site management, team seats, billing limits, and private deployment.

## Stack

- Backend: FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL, Redis, JWT, WebSocket
- Frontend: Next.js, React, TypeScript, TailwindCSS
- Widget: plain JavaScript plus iframe chat UI
- Deployment: Docker Compose and Caddy

## Local Development

1. Copy the environment file:

   ```bash
   cp .env.example .env
   ```

2. Update secrets in `.env`, especially `POSTGRES_PASSWORD` and `JWT_SECRET`.

3. Start the full stack:

   ```bash
   docker compose up --build
   ```

4. Open the app:

   - Frontend through Caddy: `http://localhost`
   - Backend health: `http://localhost/api/health`
   - Widget script: `http://localhost/widget.js`

The backend runs Alembic migrations on container start. Default plans are seeded by the first migration.

## Useful Commands

Run only backend dependencies locally:

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Run only frontend locally:

```bash
cd frontend
npm install
npm run dev
```

## Widget Snippet

Customers embed KoyunChat with:

```html
<script src="https://chat.koyun.edu.kg/widget.js" data-site-id="site_xxxxx" async></script>
```

For local Caddy testing, use:

```html
<script src="http://localhost/widget.js" data-site-id="site_xxxxx" async></script>
```

## First API Surface

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/sites`
- `POST /api/sites`
- `GET /api/sites/{site_id}/embed-code`
- `GET /api/widget/site/{site_key}/config`
- `POST /api/widget/init`
- `POST /api/widget/page-view`
- `POST /api/widget/message`
- `GET /api/conversations`
- `GET /api/conversations/{conversation_id}/messages`
- `POST /api/conversations/{conversation_id}/messages`
- `GET /api/billing/plans`
- `GET /api/admin/stats`

## Notes

- Dashboard APIs require JWT authentication.
- Public widget APIs validate `site_key`, active site status, and optional allowed domains.
- AI replies use an OpenAI-compatible `/chat/completions` API when `OPENAI_API_KEY` is configured.
- The first AI implementation uses enabled knowledge base entries directly in the system prompt. It does not require a vector database.
