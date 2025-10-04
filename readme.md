# CatalogFlow – Project Folder Structure & Design Decisions

## Proposed Folder Structure

```CatalogFlow/
├─ alembic/ # Alembic migrations
│ └─ versions/ # Migration files
├─ app/ # Main application code
│ ├─ core/ # App-level configs, constants, settings
│ ├─ database/ # DB layer (sync/async, session, Base)
│ ├─ models/ # SQLAlchemy ORM models
│ ├─ crud/ # Database CRUD functions for each model
│ ├─ api/ # FastAPI API layer
│ │ └─ v1/ # Versioning for API
│ │ ├─ routers/ # Route definitions per entity
│ │ ├─ schemas/ # Pydantic schemas for validation & serialization
│ │ └─ services/ # Business logic, helper functions for routes
│ ├─ utils/ # Utility functions/helpers
│ ├─ tasks/ # Background jobs, Celery tasks, etc.
│ └─ tests/ # Unit and integration tests
├─ docs/ # Documentation (e.g., architecture, scope)
├─ .env # Environment variables
├─ requirements.txt # Python dependencies
└─ README.md # Project README

---

## Design Decisions & Rationale

### 1. `app/`
- Contains all application code, keeping the root clean.
- Ensures everything under `app` is backend logic.

### 2. `app/core/`
- Stores configuration, security, and shared dependencies.
- Centralizes settings (`.env`) and JWT/auth logic for reusability.
- Keeps sensitive logic in one place for maintainability.

### 3. `app/database/`
- Database engine, session, and base declarative models.
- Separation of DB connection from models and CRUD logic.
- Easier to swap configs, run tests, or migrate databases.

### 4. `app/models/`
- SQLAlchemy ORM models for entities: Users, Teams, Products, Categories, etc.
- Modular design with each entity in a separate file.
- Reduces conflicts in team development.

### 5. `app/crud/`
- Encapsulates create, read, update, delete operations.
- Follows repository pattern by separating logic from models.
- Simplifies testing and code maintenance.

### 6. `app/api/v1/`
- Versioned API for forward compatibility.
- Subfolders:
  - `routers/` → HTTP endpoints per entity
  - `schemas/` → Pydantic models for requests/responses
  - `services/` → Business logic not tied directly to DB

### 7. `app/utils/`
- Helper functions such as logging setup or general utilities.
- Keeps core and models clean.

### 8. `app/tasks/`
- Background jobs (caching, bulk updates, notifications).
- Isolated for easier switch between task runners.

### 9. `app/tests/`
- Unit and integration tests.
- Mirrors the app structure for clarity and maintainability.

### 10. `docs/`
- Stores `architecture_and_scope.md`, ER diagrams, API references.
- Centralized location for all project documentation.

### 11. Root Files
- `.env` → environment variables
- `requirements.txt` → Python dependencies
- `README.md` → project overview

---

## Principles Behind the Structure

- **Modularity:** Each major component is isolated.  
- **Separation of Concerns:** Models, CRUD, services, and API logic are distinct.  
- **Scalability & Future-Proofing:** Versioned API, caching, and background tasks.  
- **Team-Friendly:** Reduces merge conflicts, easier onboarding.  
- **Testable & Maintainable:** Clean structure mirrors in `tests`, logic is isolated.
