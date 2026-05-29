# Phase 0 — Team setup (real data only)

## Prerequisites

- Python 3.10+
- Node.js 18+ (Member A live discovery)
- Git

## Environment (do not commit secrets)

Create `.env` in project root (optional):

```
GITHUB_TOKEN=your_token_here
# Dev only — never for final demo:
# INROAD_ALLOW_MOCK_FALLBACK=true
```

## Run every day

**Terminal 1 — API**

```bash
cd Let-s-hack-in
pip install -r requirements.txt
python main.py
```

**Terminal 2 — Frontend**

```bash
cd Let-s-hack-in/frontend
python -m http.server 5500
```

| Page | URL |
|------|-----|
| Home | http://localhost:5500/index.html |
| Analyze | http://localhost:5500/analyze.html |
| Agents | http://localhost:5500/agents.html |
| Opportunity detail | http://localhost:5500/opportunity.html?i=0 |

## Production API URL

Edit `frontend/scripts/config.js`:

```js
window.INROAD_API_BASE = "https://your-api-host.example.com";
```

## Policy

- No sample/fill buttons in production UI
- No fake metrics on landing
- Do not enable `INROAD_ALLOW_MOCK_FALLBACK` for demos unless discovery is broken
