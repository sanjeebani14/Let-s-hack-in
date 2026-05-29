# Deploy InRoad frontend (Phase 6)

## Build

```bash
cd frontend
npm ci
cp .env.example .env.production   # edit API URL
npm run build
```

Set production API URL in `.env.production`:

```
VITE_INROAD_API_BASE=https://your-api.example.com
```

Output is in `frontend/dist/` — upload that folder to any static host.

## Netlify

1. Connect repo → **Base directory:** `frontend`
2. **Build command:** `npm ci && npm run build`
3. **Publish directory:** `dist`
4. **Environment variables:** `VITE_INROAD_API_BASE` = your hosted FastAPI URL

`netlify.toml` in this folder configures the above.

## Vercel

1. Import project → root `frontend`
2. Framework: **Vite**
3. Add env var `VITE_INROAD_API_BASE`
4. Deploy

## GitHub Pages

```bash
cd frontend
npm run build
# Push dist/ to gh-pages branch or use GitHub Actions
```

Set `base` in `vite.config.js` if the site is not at domain root:

```js
base: "/Let-s-hack-in/",
```

## After deploy

- Frontend must reach a **CORS-enabled** API (`main.py` allows `*` in dev).
- Run backend separately (Railway, Render, etc.) and point `VITE_INROAD_API_BASE` at it.

## Local production preview

```bash
npm run build
npm run preview
```

Open http://localhost:5500 — same as dev server port.
