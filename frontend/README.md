# InRoad Frontend (integrated)

The teammate Stitch export lives under `stitch_remix_of_inroad_ai_career_dashboard/`. **Integrated, API-connected pages** are in `public/` and are served by the FastAPI backend.

## Run

From the repo root:

```bash
pip install -r requirements.txt
python main.py
```

Open **http://localhost:8000/** (landing) or **http://localhost:8000/analyze.html** to start.

## Flow

1. **Register / Login** — Firebase auth with role: `student`, `recruiter`, or `admin`
2. **Analyze** (`/analyze.html`) — upload resume (PDF/DOCX/TXT), edit extracted skills/experience/internships
3. **Profile** (`/profile.html`) — persist and edit profile sections in Firestore
4. **Dashboard** — InRoad score, fit score, matched opportunities
5. **Opportunity detail** — chemistry, way-in strategy (`?id=`)
6. **Skill graph** — core skills & proof cards from profile
7. **Outreach** — `POST /outreach` (Agent 5) for email/LinkedIn drafts

## Firebase setup

Copy `.env.example` to `.env` in the repo root and fill in values from Firebase Console:

- **Project settings** → Web app: `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`, etc.
- **Project settings** → Service accounts → Generate key → set `GOOGLE_APPLICATION_CREDENTIALS`

Enable sign-in providers under **Authentication → Sign-in method**:
- **Email/Password**
- **Google** (add support email; for local dev, `localhost` is allowed by default)

## API

| Endpoint | Purpose |
|----------|---------|
| `GET /api/health` | Health check |
| `GET /api/config/firebase` | Public Firebase web config |
| `POST /api/auth/sync` | Sync role after register (Bearer token) |
| `GET /api/profile` | Load user profile (auth required) |
| `PUT /api/profile` | Save skills, experience, internships |
| `POST /resume/upload` | Parse resume file |
| `POST /analyze` | Full pipeline (Members A/B + Agent 3) |
| `POST /outreach` | Outreach package (Agent 5) |

Analysis results are in `sessionStorage` (`inroad_analysis_v1`). Profiles are stored in Firestore when Firebase is configured.
