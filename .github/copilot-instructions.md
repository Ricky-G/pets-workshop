# GitHub Copilot Instructions — Tailspin Shelter

## Project Overview
This is the **Tailspin Shelter** application — a fictional dog adoption shelter website used as a teaching project for GitHub workshops. It has two parts:

- **Backend** (`server/`): Python + Flask REST API with SQLAlchemy ORM, backed by a SQLite database (`dogshelter.db`).
- **Frontend** (`client/`): Astro framework with Svelte components for dynamic pages, styled with Tailwind CSS.

---

## Repository Structure

```
server/         # Flask API
  app.py        # Route definitions — all API endpoints live here
  models/       # SQLAlchemy models: Dog, Breed (with AdoptionStatus enum)
  utils/        # Database seeding utilities
  test_app.py   # Unit tests using unittest + mocks

client/         # Astro + Svelte frontend
  src/
    pages/      # Astro page routes
    components/ # Svelte components (DogList, DogDetails)
    layouts/    # Shared Astro layouts
  e2e-tests/    # Playwright end-to-end tests
```

---

## Backend Conventions (server/**/*.py)

Detailed rules are in `.github/instructions/python-flask-best-practices.instructions.md` and are automatically applied when editing Python files in `server/`. Key technologies: Flask routes, SQLAlchemy ORM, `jsonify()` responses, `unittest` + `unittest.mock` for tests.

## Frontend Conventions (client/src/**/*.svelte, **/*.astro)

- Use **TypeScript** with explicit interfaces for data shapes (see `Dog` interface in `DogList.svelte`).
- Fetch data from the Flask API via relative `/api/...` paths (proxied by Astro).
- Handle loading and error states in every component that fetches data.
- Use Tailwind CSS utility classes for all styling — no custom CSS unless in `global.css`.
- Prefer `client:only="svelte"` for Svelte components that use browser APIs (e.g. `fetch`, `onMount`).

---

## Data Models

**Dog** fields: `id`, `name`, `breed_id` (FK), `age`, `gender` (`Male`/`Female`/`Unknown`), `description`, `status` (`AdoptionStatus` enum: `AVAILABLE`, `ADOPTED`, `PENDING`), `intake_date`, `adoption_date`.

**Breed** fields: `id`, `name`.

**API endpoints:**
- `GET /api/dogs` — list all dogs (id, name, breed)
- `GET /api/dogs/<id>` — single dog with full details
- `GET /api/dogs/breed/<breed_name>` — dogs filtered by breed name (case-insensitive)

---

## Testing

- **Backend**: `unittest` with `unittest.mock` (patch `db.session.query`). Run with `python -m pytest` from `server/`.
- **Frontend E2E**: Playwright tests in `client/e2e-tests/`. Run with `npm run test:e2e` from `client/`.
- When adding a new API endpoint, add corresponding unit tests in `server/test_app.py`.
- When adding a new page or component, consider adding a Playwright spec in `client/e2e-tests/`.

---

## Running the App

- **Backend**: `cd server && flask run --port 5100`
- **Frontend**: `cd client && npm run dev`
- **Seed database**: use scripts in `scripts/` (`seed-database.ps1` / `seed-database.sh`)

## Code Reviews
- Follow the conventions outlined in this document and the linked instruction files.
- The code review instruction are located in code-review.md