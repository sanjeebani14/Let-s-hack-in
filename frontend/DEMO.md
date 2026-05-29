# Demo script (Phase 10)

2–3 minute walkthrough for judges or teammates.

## Before you start

1. Terminal 1: `python main.py`
2. Terminal 2: `cd frontend && npm run dev`
3. Optional: set `GITHUB_TOKEN` in root `.env` for better discovery
4. Have resume + projects text ready (see team sample profile)

## Script

### 1. Landing (15s)

- Open http://localhost:5500/
- Point out: **five agents**, live API badge, no fake placement stats
- Click **Analyze My Profile**

### 2. Analyze (60–90s)

- Paste **name**, **resume**, **projects**
- Click **Run analysis**
- While waiting, mention pipeline: Discovery → Match → Chemistry → Proof → Outreach
- When results load:
  - Summary chips (evaluated / matched / scores)
  - Agent 2 profile
  - Top opportunity: **Fit**, **InRoad**, **Way in**
  - **Outreach ready** teaser → **Full detail**

### 3. Opportunity detail (30s)

- Open **Full detail** on best match
- Scroll: Agent 1 scores, Agent 3 chemistry, Agent 4 proof, Agent 5 outreach
- Click **Copy** on LinkedIn message

### 4. History (15s)

- Nav → **History**
- Show run saved on device
- **View results** → back to analyze without re-running API

### 5. Agents page (15s)

- Nav → **Agents**
- Quick map of all five agents and flow

## If something breaks

| Issue | Fix |
|-------|-----|
| API offline on landing | Start `python main.py` |
| Analyze fetch failed | Same; check http://localhost:8000/docs |
| No opportunities | Check discovery logs; optional `GITHUB_TOKEN` |
| Blank styles | Use `npm run dev`, not `python -m http.server` |
| Timeout | Wait or retry; first run is slowest |

## One-liner pitch

> InRoad doesn’t search job boards — it discovers hidden signals, scores your fit and chemistry, proves your skills per opportunity, and drafts outreach so you know exactly how to get in.
