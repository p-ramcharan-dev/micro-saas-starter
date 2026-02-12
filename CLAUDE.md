# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Micro-SaaS Starter — a full-stack boilerplate with a SvelteKit frontend and FastAPI backend, designed for rapid SaaS product development with AI agent capabilities.

## Architecture

**Monorepo with two independent apps:**

- `frontend/` — SvelteKit app (Svelte 5 with runes). Uses Shadcn-Svelte for UI, Tailwind CSS for styling, TanStack Query for data fetching/caching.
- `backend/` — FastAPI app managed with UV. Uses SQLModel (Pydantic + SQLAlchemy) for models, Alembic for migrations, LangGraph for AI agent workflows.

**Route groups in SvelteKit:**
- `(app)/` — Authenticated pages (dashboard, settings)
- `(marketing)/` — Public pages (landing, pricing, blog)

**Backend module responsibilities:**
- `routers/` — Versioned API endpoints (prefix with `/v1/`)
- `agents/` — LangGraph AI agent definitions and workflows
- `core/` — Config, security utils, shared dependencies
- `models/` — SQLModel database entities
- `schemas/` — Pydantic request/response DTOs (separate from models)

## Commands

### Frontend (from `frontend/`)
```bash
npm install              # Install dependencies
npm run dev              # Dev server (default: localhost:5173)
npm run build            # Production build
npm run preview          # Preview production build
npm run check            # Svelte type checking
npm run lint             # Lint with ESLint + Prettier
npm run format           # Auto-format with Prettier
```

### Backend (from `backend/`)
```bash
uv sync                  # Install dependencies
uv run fastapi dev app/main.py    # Dev server with hot reload (default: localhost:8000)
uv run fastapi run app/main.py   # Production server
uv run pytest            # Run all tests
uv run pytest tests/test_foo.py::test_bar  # Run single test
uv run alembic upgrade head               # Apply migrations
uv run alembic revision --autogenerate -m "description"  # Create migration
```

### Infrastructure
```bash
docker compose up -d     # Start local services (Postgres, Redis, Mailhog)
docker compose down      # Stop local services
```

## Key Conventions

- **Svelte 5 runes only:** Use `$state`, `$derived`, `$effect` — never legacy `$:` reactive statements or Svelte stores for component state.
- **API versioning:** All backend routes go under `/v1/` prefix.
- **Models vs Schemas:** SQLModel classes in `models/` define DB tables. Pydantic classes in `schemas/` define API contracts. Keep them separate.
- **Auth:** Clerk handles authentication. Frontend uses Clerk's Svelte SDK; backend validates Clerk JWTs.
- **Payments:** Lemon Squeezy (or Stripe) via webhook integration.
- **State management:** TanStack Query for server state; Svelte 5 runes (`$state`) for local UI state. No separate state management library.
- **Package management:** UV for Python (not pip/poetry), npm for frontend.
