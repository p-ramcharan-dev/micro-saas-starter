# Micro-SaaS Starter

A full-stack boilerplate for building SaaS products with AI agent capabilities. SvelteKit frontend, FastAPI backend, LangGraph AI workflows.

## Architecture

### System Overview

```mermaid
graph TB
    subgraph Client
        Browser["Browser"]
    end

    subgraph Frontend["Frontend — SvelteKit :5173"]
        SSR["SSR / Hydration"]
        Pages["Routes & Pages"]
        TQ["TanStack Query"]
    end

    subgraph Auth["Auth — Clerk"]
        ClerkFE["Svelte SDK"]
        ClerkBE["JWT Validation"]
    end

    subgraph Backend["Backend — FastAPI :8000"]
        API["REST API /v1/"]
        Agents["LangGraph Agents"]
    end

    subgraph Data["Data Layer"]
        PG["PostgreSQL :5432"]
        Redis["Redis :6379"]
    end

    subgraph External["External Services"]
        LLM["LLM Provider"]
        Pay["Lemon Squeezy / Stripe"]
        Mail["Mailhog :8025 (dev)"]
    end

    Browser --> SSR
    SSR --> Pages
    Pages --> TQ
    Pages --> ClerkFE
    TQ -- "HTTP /v1/*" --> API
    ClerkFE -. "session token" .-> ClerkBE
    ClerkBE --> API
    API --> Agents
    Agents --> LLM
    API --> PG
    API --> Redis
    Pay -- "webhooks" --> API
    API --> Mail
```

### Request Flow

```mermaid
sequenceDiagram
    participant B as Browser
    participant SK as SvelteKit
    participant CL as Clerk
    participant FA as FastAPI
    participant DB as PostgreSQL
    participant AG as LangGraph Agent

    B->>SK: Page request
    SK->>B: SSR HTML + hydrate

    B->>CL: Authenticate
    CL->>B: Session JWT

    B->>FA: GET /v1/resource (+ JWT)
    FA->>CL: Validate token
    CL-->>FA: User identity
    FA->>DB: Query
    DB-->>FA: Result
    FA-->>B: JSON response

    B->>FA: POST /v1/agents/run (+ JWT)
    FA->>AG: Execute workflow
    AG->>AG: LLM calls + tool use
    AG-->>FA: Agent result
    FA-->>B: Streamed response
```

### Frontend Architecture

```mermaid
graph LR
    subgraph Routes["src/routes/"]
        direction TB
        MKT["(marketing)/<br/>Landing, Pricing, Blog"]
        APP["(app)/<br/>Dashboard, Settings"]
    end

    subgraph Lib["src/lib/"]
        direction TB
        Components["components/<br/>Shadcn-Svelte UI"]
        Stores["stores/<br/>Svelte 5 runes"]
        APIClient["api/<br/>Fetch wrappers"]
    end

    subgraph External["External"]
        ClerkSDK["Clerk Svelte SDK"]
        TQ["TanStack Query"]
    end

    APP -- "auth guard" --> ClerkSDK
    MKT --> Components
    APP --> Components
    APP --> Stores
    APP --> APIClient
    APIClient --> TQ
    TQ -- "HTTP" --> Backend["FastAPI /v1/"]
```

### Backend Architecture

```mermaid
graph TB
    subgraph Entrypoint
        Main["main.py<br/>CORS, middleware, router registration"]
    end

    subgraph Routers["routers/"]
        Health["health.py — /v1/health"]
        Resources["... — /v1/*"]
    end

    subgraph Core["core/"]
        Config["config.py<br/>Pydantic Settings"]
        Security["security.py<br/>Clerk JWT deps"]
    end

    subgraph Domain
        Models["models/<br/>SQLModel entities"]
        Schemas["schemas/<br/>Pydantic DTOs"]
    end

    subgraph AI["agents/"]
        Graph["LangGraph workflows"]
        Tools["Agent tool definitions"]
    end

    subgraph Infra["Infrastructure"]
        PG[(PostgreSQL)]
        Redis[(Redis)]
        Alembic["migrations/<br/>Alembic versions"]
    end

    Main --> Routers
    Routers --> Core
    Routers --> Schemas
    Routers --> Models
    Routers --> AI
    Models --> PG
    Alembic --> PG
    AI --> Graph
    Graph --> Tools
    Core --> Config
```

### Data Model Separation

```mermaid
graph LR
    Request["Incoming JSON"] --> Schema["schemas/<br/>Pydantic DTO<br/>(validation)"]
    Schema --> Router["routers/<br/>(business logic)"]
    Router --> Model["models/<br/>SQLModel<br/>(DB read/write)"]
    Model --> DB[(PostgreSQL)]
    DB --> Model
    Model --> ResponseSchema["schemas/<br/>Pydantic DTO<br/>(serialization)"]
    ResponseSchema --> Response["JSON Response"]
```

## Quick Start

```bash
# Start infrastructure (Postgres, Redis, Mailhog)
docker compose up -d

# Backend
cd backend
uv sync
uv run fastapi dev app/main.py

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | SvelteKit + Svelte 5 | App framework with runes reactivity |
| UI | Shadcn-Svelte + Tailwind CSS | Components and styling |
| Data Fetching | TanStack Query | Caching and optimistic updates |
| Backend | FastAPI + UV | Async API server |
| ORM | SQLModel | Type-safe models (Pydantic + SQLAlchemy) |
| Migrations | Alembic | Database schema versioning |
| AI | LangGraph | Stateful AI agent workflows |
| Auth | Clerk | Authentication and multi-tenancy |
| Payments | Lemon Squeezy / Stripe | Billing and subscriptions |
| Infra | Docker + Railway | Local dev and deployment |

## Project Structure

```
.
├── frontend/              # SvelteKit app
│   └── src/
│       ├── lib/           # Components, stores, API clients
│       └── routes/        # (app)/ for dashboard, (marketing)/ for public pages
│
├── backend/               # FastAPI app
│   ├── app/
│   │   ├── routers/       # API endpoints (versioned under /v1/)
│   │   ├── agents/        # LangGraph AI workflows
│   │   ├── core/          # Config, security, utils
│   │   ├── models/        # SQLModel database entities
│   │   └── schemas/       # Pydantic request/response DTOs
│   └── migrations/        # Alembic migration history
│
├── docs/                  # Project documentation
└── docker-compose.yml     # Local dev services
```

## Development

### Frontend

```bash
cd frontend
npm run dev       # Dev server at localhost:5173
npm run build     # Production build
npm run check     # Type checking
npm run lint      # Lint + format check
```

### Backend

```bash
cd backend
uv run fastapi dev app/main.py                  # Dev server at localhost:8000
uv run pytest                                   # Run all tests
uv run pytest tests/test_foo.py::test_bar       # Run single test
uv run alembic upgrade head                     # Apply migrations
uv run alembic revision --autogenerate -m "description"  # New migration
```

### Infrastructure

```bash
docker compose up -d     # Start Postgres, Redis, Mailhog
docker compose down      # Stop services
```

See [docs/setup.md](docs/setup.md) for detailed environment configuration.
