# InRoad Frontend

Static multi-page site for the InRoad Opportunity Engine — wired to the live FastAPI pipeline (all 5 agents via `POST /analyze`).

## Pages

| Page | File | Purpose |
|------|------|---------|
| Landing | `index.html` | Product story, agent-aligned features, API status |
| Analyze | `analyze.html` | Resume + projects → full pipeline results |
| Agents | `agents.html` | How each agent works |
| Opportunity | `opportunity.html?i=N` | Single opportunity detail (from last analyze) |
| History | `history.html` | Saved runs on this device (localStorage) |

## Run locally

See **`SETUP.md`** for env vars and team policy (no mock fallback for demos).

**Terminal 1 — API**

```bash
cd /path/to/Let-s-hack-in
pip install -r requirements.txt
python main.py
```

**Terminal 2 — Frontend**

```bash
cd frontend
npm install
npm run dev
```

Production build: `npm run build` → output in `dist/`. See **`DEPLOY.md`**.

| URL | Page |
|-----|------|
| http://localhost:5500/index.html | Home |
| http://localhost:5500/analyze.html | Analyze |
| http://localhost:5500/agents.html | Agents |
| http://localhost:5500/opportunity.html?i=0 | Opportunity detail |
| http://localhost:5500/history.html | Saved runs |

## Structure

```
frontend/
├── package.json          # npm run dev | build | preview
├── vite.config.js
├── tailwind.config.js
├── index.html
├── analyze.html
├── agents.html
├── opportunity.html
├── SETUP.md
├── DEPLOY.md
├── styles/
│   ├── main.css          # Tailwind entry
│   ├── base.css
│   └── components.css
├── src/entries/          # Vite page bundles
└── scripts/
    ├── config.js           # INROAD_API_BASE
    ├── api.js
    ├── layout.js           # Shared nav/footer
    ├── landing.js          # Home API badge
    ├── analyze.js          # Form + pipeline loading steps
    ├── results-render.js   # Cards, proof, outreach, copy
    ├── opportunity.js      # Detail from sessionStorage
    ├── interactions.js
    └── tailwind-config.js
```

## API

`POST /analyze` body:

- `resume_text` (min 10 chars)
- `project_descriptions` (min 10 chars)
- `candidate_name` (optional, used in outreach)

Response includes `matched_opportunities[]` with `chemistry`, `scores`, `proof`, `outreach`, `opportunity_url`, and `summary.discovery_mode`.

Set `VITE_INROAD_API_BASE` in `.env.production` before `npm run build` (see `DEPLOY.md`).

## Implementation phases

| Phase | Status |
|-------|--------|
| 0 Setup docs | Done (`SETUP.md`) |
| 1 Site map + shared layout | Done |
| 2 Landing polish (agents, API, no fake stats) | Done |
| 3 Analyze (loading, copy, sessionStorage) | Done |
| 4 Opportunity detail | Done |
| 5 Vite + Tailwind build | Done |
| 6 Deploy config + env API URL | Done (`DEPLOY.md`, `netlify.toml`) |
| 7 UI polish (titles, outreach teaser) | Done |
| 8 History (localStorage) | Done |
| 9 QA checklist | Done (`QA.md`) |
| 10 Demo script + hardening | Done (`DEMO.md`, timeouts, restore) |

## Next

1. Deploy `dist/` (Netlify/Vercel) with `VITE_INROAD_API_BASE`
2. Optional: backend-persisted history (needs API)
