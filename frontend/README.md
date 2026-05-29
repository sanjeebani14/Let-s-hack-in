# InRoad Frontend

Static multi-page site for the InRoad Opportunity Engine — wired to the live FastAPI pipeline (all 5 agents via `POST /analyze`).

## Pages

| Page | File | Purpose |
|------|------|---------|
| Landing | `index.html` | Product story, agent-aligned features, API status |
| Analyze | `analyze.html` | Resume + projects → full pipeline results |
| Agents | `agents.html` | How each agent works |
| Opportunity | `opportunity.html?i=N` | Single opportunity detail (from last analyze) |

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
python -m http.server 5500
```

| URL | Page |
|-----|------|
| http://localhost:5500/index.html | Home |
| http://localhost:5500/analyze.html | Analyze |
| http://localhost:5500/agents.html | Agents |
| http://localhost:5500/opportunity.html?i=0 | Opportunity detail |

## Structure

```
frontend/
├── index.html
├── analyze.html
├── agents.html
├── opportunity.html
├── SETUP.md
├── styles/
│   ├── base.css
│   └── components.css
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

Change API URL in `scripts/config.js` for production.

## Implementation phases

| Phase | Status |
|-------|--------|
| 0 Setup docs | Done (`SETUP.md`) |
| 1 Site map + shared layout | Done |
| 2 Landing polish (agents, API, no fake stats) | Done |
| 3 Analyze (loading, copy, sessionStorage) | Done |
| 4 Opportunity detail | Done |
| 5–6 Vite build + deploy | Not started |
| 7–10 Dashboard, saved runs, QA | Not started |

## Next

1. Production build (Vite + Tailwind instead of CDN)
2. Deploy frontend + set `INROAD_API_BASE` to hosted API
3. Saved analyses dashboard (needs backend storage)
