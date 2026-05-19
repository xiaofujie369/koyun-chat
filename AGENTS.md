# AGENTS.md

## Project

This repository is KoyunChat, a lightweight SaaS live chat platform similar to tawk.to, with visitor tracking, AI auto-reply, lead collection, and multi-tenant billing.

## Language

Use English for code, comments, variables, database columns, and API paths.
User-facing text can support English and Chinese.

## Stack

Backend:
- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Redis
- JWT
- WebSocket

Frontend:
- Next.js
- React
- TypeScript
- TailwindCSS

Widget:
- Plain JavaScript
- iframe-based chat UI

Deployment:
- Docker Compose
- Caddy

## Code Rules

- Keep the project production-ready.
- Use clear module boundaries.
- Do not hardcode secrets.
- Read config from environment variables.
- Use database migrations.
- Add useful error handling.
- Add basic tests when possible.
- Keep APIs RESTful.
- Use UUID primary keys where suitable.
- All tenant-owned resources must be scoped by workspace_id or site_id.
- Never expose one workspace's data to another workspace.

## Security Rules

- Hash passwords using bcrypt or passlib.
- Use JWT for auth.
- Validate all user input.
- Protect dashboard APIs with authentication.
- Widget APIs may be public but must validate site_key and allowed domains.
- Do not leak internal errors to clients.
- Add CORS rules carefully.
- Rate limit public widget APIs if possible.

## Product Rules

The core product is:
- One script tag integration
- Live chat widget
- Visitor tracking
- Dashboard inbox
- AI auto-reply
- Knowledge base
- Lead collection
- Plans and subscriptions

## Development Order

1. Docker Compose
2. Backend skeleton
3. Database models
4. Auth
5. Site management
6. Widget init and tracking
7. Conversations and messages
8. WebSocket
9. AI reply
10. Frontend dashboard
11. Billing placeholders
12. Admin panel

## Output Expectations

When implementing a task:
- Modify only relevant files.
- Keep changes small and reviewable.
- Explain what changed.
- Mention how to test it.
