# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Web application for managing the library of the Société Archéologique de Touraine. It is a Flask REST API backend + Vue 3 SPA frontend.

## Repository Layout

```
sat_biblio_server/   Flask backend (Python package)
sat-biblio-interface/  Vue 3 frontend (npm project)
playbooks/           Ansible deployment playbooks
```

## Development Commands

### Backend (Flask)

```bash
# From repo root — activate venv first
source venv/bin/activate

# Run dev server (port 5000)
cd sat_biblio_server && python app.py

# Database migrations
flask db migrate -m "message"
flask db upgrade
```

### Frontend (Vue 3 / Vite)

```bash
cd sat-biblio-interface

npm run serve      # dev server (hot-reload, Vite)
npm run build      # production build → satbiblio-dist/
npm run lint       # ESLint fix
```

The frontend dev server proxies API calls to `http://localhost:5000/` (set in `.env.development` via `VITE_APP_SITE_API_URL`).

### Deployment (Ansible)

```bash
cd playbooks
ansible-playbook -i inventory.ini update-code.yaml -k
ansible-playbook -i inventory.ini rebuild-web-sites.yaml -k
```

## Architecture

### Backend

**App factory** — `sat_biblio_server/__init__.py` `create_app(config)` wires up Flask extensions (SQLAlchemy, Flask-JWT-Extended, Flask-Login, Flask-Mail, Flask-Migrate, Flask-CORS, Flask-Admin) and registers a single Blueprint `sat_biblio`.

**Blueprint routes** — `sat_biblio_server/routes/__init__.py` imports all route modules via wildcard. Each module (e.g. `author_routes.py`, `record_routes.py`) registers endpoints on the `sat_biblio` blueprint.

**Authentication / authorisation decorators** (defined in `check_routes.py`, imported by route modules via `from sat_biblio_server.routes import …`):
- `@validation_connexion_et_retour_defaut("email", ["POST"])` — checks JWT (preferred) then Flask session; returns 401 if not authenticated.
- `@validation_droit_et_retour_defaut(UserRight.X, ["POST", "PUT", "DELETE"])` — checks right claim in JWT or session; returns 403 if insufficient.

**User rights** (ordered enum in `sat_biblio_server/utils.py`):
`lecteur < contributeur < editeur < gestionnaire < administrateur`

**Database models** — `sat_biblio_server/database/books_2023.py` contains the active models (`Author2023DB`, `ReferenceBibliographiqueLivre2023DB`, `Enregistrement2023DB`, `EmpruntLivre2023DB`). The older `books.py` models are kept but largely superseded. `users.py` holds `UserDB`; `events.py` holds `LogEventDB`; `imports.py` holds `ImportDB` / `ImportedItemsDB`.

**Data layer** — `sat_biblio_server/data/models_2023.py` contains plain Python dataclasses/model helpers that route handlers convert to/from DB models. `sat_biblio_server/data/validation.py` holds input validation helpers.

**Config** — `sat_biblio_server/config/development.py` and `production.py`. Secret files (plain text) are read at import time from `sat_biblio_server/config/`: `email_address`, `mail_password`, `secret_key`, `jwt_secret_key`.

**Pagination** — `routes/utils.py` `get_pagination(request)` returns `(n_page, size, sort_by, sort_desc)` from query params; used uniformly by list endpoints.

**All JSON responses** use the helper `json_result(success: bool, message="", **data)` from `sat_biblio_server/utils.py`.

### Frontend

**Entry** — `src/main.js` → `App.vue`. State: Vuex (`src/store.js`) with `vuex-persistedstate`. Routing: Vue Router (`src/router.js`).

**Auth flow** — JWT is stored in Vuex (`connectionInfo.token`). `isValidJwt()` (`services/authentication.js`) decodes the JWT client-side to check expiry. The router's `beforeEach` guard checks `needAuth` and `reachableFrom` (a `rights` object) against `store.getters.getUserRight`.

**Rights** (mirrors backend, `services/rights.js`): `lecteur(1) < contributeur(2) < editeur(3) < gestionnaire(4) < administrateur(5)`.

**API calls** — all go through the Axios instance in `services/api.js` (baseURL from `VITE_APP_SITE_API_URL`, `withCredentials: true` for cookie-based JWT). CSRF tokens are sent via `X-CSRF-TOKEN-ACCESS` / `X-CSRF-TOKEN-REFRESH` headers.

**UI library** — Bootstrap 5 + BootstrapVueNext. Icons via `unplugin-icons` (Iconify `bi` set). Components auto-imported by `unplugin-vue-components`.

**Key domain concepts visible in the router:**
- `auteur` — library author
- `reference-livre` — bibliographic reference (book)
- `enregistrement` — physical library record (copy on a shelf)
- `catalogue` / `enregistrement-complet` — combined view of reference + record
- `emprunt` — book loan/borrowing
- `import` / `export` — bulk data operations

## Notes

- There are no project-level test files; testing is done manually.
- The `books.py` (non-2023) database models are legacy; prefer `books_2023.py` for any new work.
- Flask-Admin (`/admin`) is wired for direct DB management but is separate from the Vue SPA.
