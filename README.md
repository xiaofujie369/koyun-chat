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

3. Start the app services:

   ```bash
   docker compose up -d --build postgres redis backend frontend
   ```

   This exposes the backend on `127.0.0.1:18000` and the frontend on `127.0.0.1:13000` by default.

4. Open the app:

   - Frontend: `http://127.0.0.1:13000`
   - Backend health: `http://127.0.0.1:18000/api/health`

The backend runs Alembic migrations on container start. Default plans are seeded by the first migration.

## Bundled Caddy Option

The default compose file does not start the bundled Caddy service, so it can run behind an existing host Caddy/Nginx without port conflicts. To use the bundled Caddy instead, run:

```bash
docker compose --profile bundled-caddy up -d --build
```

## Host Caddy Example

When using an existing host Caddy, reverse proxy the app like this:

```caddy
chat.koyun.edu.kg {
    tls you@example.com

    encode gzip zstd

    handle_path /api/* {
        reverse_proxy http://127.0.0.1:18000
    }

    handle_path /ws/* {
        reverse_proxy http://127.0.0.1:18000
    }

    handle /widget.js {
        root * /data/koyun-chat-widget
        file_server
    }

    handle /widget.css {
        root * /data/koyun-chat-widget
        file_server
    }

    handle /widget/* {
        root * /data/koyun-chat-widget
        try_files {path} /iframe.html
        file_server
    }

    handle {
        reverse_proxy http://127.0.0.1:13000
    }
}
```

If Caddy is running in Docker, make sure the widget files are available inside that Caddy container at the path used by `root`.

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

For local bundled Caddy testing, use:

```html
<script src="http://localhost/widget.js" data-site-id="site_xxxxx" async></script>
```

## Admin Bootstrap

After creating a user, promote it to platform admin from PostgreSQL:

```bash
docker compose exec postgres psql -U koyunchat -d koyunchat -c "UPDATE users SET is_platform_admin = true WHERE email = 'admin@example.com';"
```

Then open `/admin` after logging in.

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
- `ALLOWED_ORIGINS` supports comma-separated values such as `https://chat.koyun.edu.kg,http://localhost`.
- AI replies use an OpenAI-compatible `/chat/completions` API when `OPENAI_API_KEY` is configured.
- The first AI implementation uses enabled knowledge base entries directly in the system prompt. It does not require a vector database.
