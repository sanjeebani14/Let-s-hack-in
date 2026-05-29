# InRoad frontend — QA checklist (Phase 9)

Run before hackathon demo. Requires API + frontend dev servers.

## Setup

- [ ] `python main.py` running on port 8000
- [ ] `cd frontend && npm run dev` on port 5500
- [ ] Landing shows **API online** (not offline)
- [ ] `INROAD_ALLOW_MOCK_FALLBACK` is **not** set for demo (unless discovery is broken)

## Pages load

- [ ] http://localhost:5500/ — Home
- [ ] http://localhost:5500/analyze.html
- [ ] http://localhost:5500/history.html
- [ ] http://localhost:5500/agents.html
- [ ] Mobile nav opens and closes (hamburger)
- [ ] Nav links work on all pages

## Analyze flow

- [ ] Submit with empty fields → validation error
- [ ] Submit with resume + projects (10+ chars each) → loading steps appear
- [ ] Results show summary chips (Evaluated, Matched, Avg fit, Best InRoad)
- [ ] Agent 2 skill profile renders
- [ ] At least one opportunity card with Fit + InRoad scores
- [ ] **Way in** box has text
- [ ] Outreach teaser shows on cards
- [ ] **Saved to History** banner after successful run
- [ ] **Full detail** opens opportunity page with proof + outreach
- [ ] **Copy** buttons work for LinkedIn / email

## History (Phase 8)

- [ ] After analyze, run appears on History page
- [ ] **View results** reopens analyze with same data
- [ ] **Delete** removes one run
- [ ] **Clear all** removes all runs (confirm dialog)
- [ ] Empty state shows when no runs

## Session / navigation

- [ ] Refresh analyze page → last results still visible (sessionStorage)
- [ ] Opportunity `?i=1` shows second card when available
- [ ] Back link from opportunity → analyze

## Production build

- [ ] `npm run build` succeeds with no errors
- [ ] `npm run preview` — repeat smoke test on http://localhost:5500

## Deploy (if using Netlify/Vercel)

- [ ] `VITE_INROAD_API_BASE` set to hosted API URL
- [ ] Hosted API has CORS enabled for frontend origin
- [ ] Analyze works against production API (not localhost)

## Known limitations (OK for demo)

- History is **browser-only** (clears if user clears site data)
- GitHub issue titles may look raw; cards trim `[FEATURE]:` prefixes
- First analyze can take 30–60s

## Sign-off

| Tester | Date | Pass? |
|--------|------|-------|
|        |      |       |
