# 🚀 Complete System Overview

## 🎯 System Architecture

Your project is a **4-component intelligent opportunity-matching platform** that combines AI-driven profile extraction, hidden opportunity discovery, semantic matching, and human network analysis.

```
INPUT (Resume + Projects)
    ↓
MEMBER A: Profile Extraction & Embeddings
    ├─ Extract 7 candidate signals
    └─ Generate vector embeddings
    ↓
MEMBER B: Opportunity Scoring & Discovery
    ├─ Load 10 hidden opportunities
    ├─ Score on 4 algorithmic signals
    └─ Rank top 3
    ↓
AGENT 3: InRoad Chemistry Analysis
    ├─ Detect shared contexts
    ├─ Find connector persons
    ├─ Check engagement signals
    ├─ Analyze team fit
    └─ Generate entry strategy
    ↓
OUTPUT (Matches + Chemistry)
```

---

## 👥 Complete Agent Breakdown

### **MEMBER A — Profile Extraction & Semantic Matching**

**Purpose:** Extract candidate signals and match against opportunities using AI embeddings.

#### Components:

| File                             | Function                                                                   |
| -------------------------------- | -------------------------------------------------------------------------- |
| `member_a/profile_extractor.py`  | Analyzes resume + projects → extracts 7 signals                            |
| `member_a/relevance_matching.py` | Uses embeddings to match profile against opportunities (cosine similarity) |
| `member_a/embeddings.py`         | Generates vector embeddings using Sentence Transformers (local, no API)    |

#### Extracted Profile Signals:

1. **core_skills** — Technical skills (Python, FastAPI, ML, etc.)
2. **ownership_signals** — Evidence of leadership/autonomy
3. **measurable_outcomes** — Quantified impact (users, revenue, etc.)
4. **problem_solving_patterns** — Problem-solving approach
5. **domain_expertise** — Primary technical domains
6. **seniority_level** — Career stage classification
7. **semantic_summary** — 2-3 sentence AI-generated summary

#### Matching Algorithm:

```
fit_score = cosine_similarity(candidate_embedding, opportunity_embedding) × 100

Range: 0-100 (higher = better match)
```

---

### **MEMBER B — The Opportunity Engine**

**Purpose:** Discover and rank hidden job opportunities using algorithmic signals.

#### Components:

| File                  | Function                                              |
| --------------------- | ----------------------------------------------------- |
| `member_b/dataset.py` | Returns 10 mock opportunities with realistic metadata |
| `member_b/scorer.py`  | Scores opportunities and ranks by quality             |

#### Data Model:

Each opportunity contains:

- `id` — Unique identifier
- `title` — Job title
- `company` — Company name
- `source_type` — Discovery channel (founder_post, github_repo, employee_post, newsletter, hackathon)
- `description` — Full job description
- `team_size` — Team headcount
- `stage` — Company stage (seed, series_a, series_b, growth, late_stage)
- `posted_date` — Publication date

#### Opportunity Scoring Algorithm:

**4 Signals (each 0.0–1.0 scale):**

| Signal                   | Description                                 | Scoring Logic                                                                                 |
| ------------------------ | ------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **competition_index**    | How hidden/uncompetitive?                   | founder_post: 0.85, github_repo: 0.75, employee_post: 0.80, newsletter: 0.70, hackathon: 0.65 |
| **response_probability** | Likelihood of reply based on source + stage | seed: 0.80, series_a: 0.75, series_b: 0.65, growth: 0.50, late_stage: 0.40                    |
| **growth_potential**     | Career acceleration value                   | seed: 0.90, series_a: 0.85, series_b: 0.75, growth: 0.60, late_stage: 0.50                    |
| **referral_likelihood**  | Probability of warm intro                   | employee_post: 0.85, founder_post: 0.75, github_repo: 0.70, newsletter: 0.60, hackathon: 0.80 |

**Final Score Calculation:**

```
opportunity_score = (
    competition_index × 0.25 +
    response_probability × 0.25 +
    growth_potential × 0.25 +
    referral_likelihood × 0.25
)

Range: 0.0-1.0 (converted to 0-100 in output)
```

#### Ranking:

- Scores all 10 opportunities
- Sorts by `opportunity_score` descending
- Returns top **3** by default

---

### **AGENT 3 — InRoad Chemistry Analyzer** ⭐

**Purpose:** Detect human bridges and real entry strategies to opportunities.

**Innovation:** While Members A & B focus on skill/opportunity matching, Agent 3 answers the real question: _"How do I actually get introduced to this company?"_

#### Components:

| Module                        | Function                                                                                                       |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `agent_3/context_detector.py` | Finds shared touchpoints (hackathons, communities, open-source, conferences) between candidate and target team |
| `agent_3/connector.py`        | Identifies 2nd-degree connections who can make introductions                                                   |
| `agent_3/engagement.py`       | Checks if company employees have interacted with candidate's code/work                                         |
| `agent_3/team_analyzer.py`    | Analyzes team composition fit (complements/neutral/overlaps)                                                   |
| `agent_3/calculator.py`       | Combines all signals into **InRoad Score** (0-100)                                                             |
| `agent_3/way_in.py`           | Generates **one specific, actionable sentence** for entry strategy                                             |

#### 1. Shared Context Detector

**Detects:** Hackathons, communities, open-source projects, conferences shared between candidate and target team.

```python
class SharedContext:
    context_type: str  # 'hackathon', 'community', 'opensource', 'conference'
    name: str          # E.g., "PyCon 2025", "Python Discord"
    relevance_score: float  # 0.0-1.0
```

**Output:**

```python
class ContextDetectorResponse:
    shared_contexts: List[SharedContext]
    total_overlap_score: float  # Average relevance
    summary: str  # E.g., "3 shared contexts detected"
```

---

#### 2. Connector Person Finder

**Finds:** 2nd-degree connections (your network → their network).

```python
class ConnectorPerson:
    person_name: str
    relationship_to_candidate: str  # "Former MIT classmate"
    relationship_strength_to_candidate: float  # 0.0-1.0
    relationship_to_company: str  # "Senior Engineer at target company"
    relationship_strength_to_company: float  # 0.0-1.0
    introduction_likelihood: float  # Probability they'd introduce you
```

**Output:**

```python
class ConnectorResponse:
    connectors: List[ConnectorPerson]
    best_connector: ConnectorPerson  # Highest value bridge
    entry_probability: float  # Overall intro likelihood (0.0-1.0)
    summary: str
```

---

#### 3. Engagement Signal Checker

**Detects:** Company employees who have interacted with candidate's work.

```python
class EmployeeInteraction:
    employee_name: str
    employee_role: str  # "Backend Lead", "CTO", etc.
    interaction_type: str  # "starred_repo", "commented_on_PR", "attended_talk"
    strength: float  # 0.0-1.0
```

**Output:**

```
engagement_strength: float  # 0.0-1.0
employee_interactions: List[EmployeeInteraction]
```

---

#### 4. Team Composition Analyzer

**Analyzes:** How candidate skills complement/overlap with team.

**Categories:**

- `complements` — Your skills fill team gaps (best fit)
- `neutral` — Mixed overlap
- `overlaps` — Heavy skill duplication (lower priority)

**Output:**

```
team_fit_category: str  # 'complements', 'neutral', or 'overlaps'
team_chemistry_score: float  # 0.0-1.0
```

---

#### 5. InRoad Score Calculator

**Combines all signals** into final opportunity quality score.

**Formula:**

```
inroad_score = (
    role_fit_pct × 0.40 +           # How well skills match (from Member A)
    team_overlap_pct × 0.20 +       # Shared contexts (from Context Detector)
    entry_probability_pct × 0.30 +  # Can you get introduced? (from Connectors + Engagement)
    competition_index × 100 × 0.10  # Hidden opportunity bonus (from Member B)
)

Range: 0-100 (higher = better)
```

**Breakdown:**

- `role_fit_percentage` — 0-100 (from Member A fit_score)
- `team_overlap_percentage` — 0-100 (from shared contexts)
- `entry_probability_percentage` — 0-100 (from connectors + engagement)
- `competition_index` — 0.0-1.0 (from Member B)
- `inroad_score` — 0-100 (final combined)
- `structural_explanation` — One-line plain English summary

---

#### 6. Way In Strategy Generator

**Generates:** Single most actionable entry strategy sentence.

```python
class WayInStrategy:
    actionable_sentence: str
    # Example: "David Lee, your MIT classmate, is their backend lead —
    #           he attended HackTheAI 2025 with you. That's your way in."

    primary_signal: str  # Which signal is strongest
    confidence: float  # 0.0-1.0
```

**Selection Logic:**

1. Check all 4 signals (shared_context, engagement, connector, team_fit)
2. Find the **highest-value human bridge**
3. Generate one specific, actionable sentence
4. Include confidence score

---

## 🔌 API Endpoints & Frontend Integration

### FastAPI Server

**Location:** `main.py`  
**Port:** `8000`  
**Host:** `0.0.0.0` (all network interfaces)

#### Configuration:

- **CORS:** All origins (`*`), all methods, all headers
- **Logging:** INFO level with structured output
- **Validation:** Pydantic request/response models
- **Error Handling:** Comprehensive try-catch with meaningful HTTP status codes

---

### Endpoint 1: Health Check

**Request:**

```bash
GET /
```

**Response (200 OK):**

```json
{
  "status": "healthy",
  "engine": "Opportunity Engine Running",
  "timestamp": "2026-05-23T14:30:00.123456"
}
```

---

### Endpoint 2: Full Analysis Pipeline

**Request:**

```bash
POST /analyze
Content-Type: application/json
```

**Request Body:**

```json
{
  "resume_text": "string (min 10 chars)",
  "project_descriptions": "string (min 10 chars)"
}
```

**Example Request:**

```json
{
  "resume_text": "Senior Backend Engineer with 5 years experience in Python and FastAPI. Built distributed systems and ML pipelines. Led teams of 3-5 engineers.",
  "project_descriptions": "- Built ML inference API using FastAPI and TensorFlow serving 10K+ daily requests\n- Developed data pipeline for 1M+ records using Apache Spark\n- Led backend team for real-time analytics platform processing 50M events/day"
}
```

**Response (200 OK):**

```json
{
  "status": "success",
  "timestamp": "2026-05-23T14:30:00.123456",
  "candidate_profile": {
    "core_skills": ["Python", "FastAPI", "ML", "TensorFlow", "Spark"],
    "ownership_signals": [
      "Built end-to-end ML systems",
      "Led engineering teams",
      "Architected data pipelines"
    ],
    "measurable_outcomes": [
      "Serving 10K+ daily requests",
      "Processing 1M+ records",
      "Handling 50M events/day"
    ],
    "problem_solving_patterns": [
      "Worked on real-time distributed systems",
      "Optimized high-throughput data processing",
      "Led technical decision-making"
    ],
    "domain_expertise": ["Backend", "Data Engineering", "ML Ops"],
    "seniority_level": "Senior Engineer",
    "semantic_summary": "Experienced backend engineer specializing in scalable ML systems and data infrastructure..."
  },
  "matched_opportunities": [
    {
      "opportunity_id": 1,
      "title": "AI/ML Engineer - Early Stage",
      "company": "NeuralFlow Startup",
      "source_type": "founder_post",
      "fit_score": 87.45,
      "match_reasoning": "Strong experience with ML infrastructure, FastAPI, and Python. Your experience with high-throughput systems aligns perfectly with their backend needs.",
      "scores": {
        "competition_index": 0.85,
        "response_probability": 0.78,
        "growth_potential": 0.9,
        "referral_likelihood": 0.7,
        "opportunity_score": 0.805,
        "score_reasoning": "Highly hidden opportunity with strong growth potential in early-stage AI startup"
      },
      "chemistry": {
        "inroad_score": 82.5,
        "structural_explanation": "Strong role fit + existing network bridge = high priority opportunity",
        "shared_contexts_count": 3,
        "shared_contexts_summary": "Both active in Python community, attended HackTheAI 2025, contributed to PyTorch",
        "employee_interactions": [
          {
            "employee_name": "Sarah Chen",
            "employee_role": "VP Engineering",
            "interaction_type": "starred_repo",
            "strength": 0.75
          }
        ],
        "engagement_strength": 0.72,
        "best_connector_name": "David Lee",
        "best_connector_intro": "Your MIT classmate, now Senior Engineer at NeuralFlow",
        "entry_probability": 0.85,
        "team_fit_category": "complements",
        "team_chemistry_score": 0.88,
        "way_in_strategy": "David Lee, your MIT classmate, is their backend lead and attended HackTheAI 2025 with you — that's your way in.",
        "way_in_confidence": 0.9
      }
    },
    {
      "opportunity_id": 4,
      "title": "ML Platform Engineer",
      "company": "DataVault AI",
      "source_type": "employee_post",
      "fit_score": 85.2,
      "match_reasoning": "Your experience with Spark and data pipelines directly matches their platform needs...",
      "scores": {
        "competition_index": 0.8,
        "response_probability": 0.82,
        "growth_potential": 0.85,
        "referral_likelihood": 0.75,
        "opportunity_score": 0.805,
        "score_reasoning": "Employee referral path + strong technical fit"
      },
      "chemistry": {
        "inroad_score": 79.3,
        "structural_explanation": "Good role fit with warm referral path available",
        "shared_contexts_count": 2,
        "shared_contexts_summary": "Both active in data engineering communities",
        "employee_interactions": [],
        "engagement_strength": 0.55,
        "best_connector_name": "Maria Garcia",
        "best_connector_intro": "Your former colleague, now Engineering Manager at DataVault",
        "entry_probability": 0.8,
        "team_fit_category": "complements",
        "team_chemistry_score": 0.82,
        "way_in_strategy": "Maria Garcia, your former colleague, is an Engineering Manager at DataVault and could fast-track your application.",
        "way_in_confidence": 0.85
      }
    },
    {
      "opportunity_id": 7,
      "title": "Backend Engineer - Series A",
      "company": "TechFlow Innovations",
      "source_type": "newsletter",
      "fit_score": 82.15,
      "match_reasoning": "Solid experience with backend systems and Python...",
      "scores": {
        "competition_index": 0.7,
        "response_probability": 0.68,
        "growth_potential": 0.8,
        "referral_likelihood": 0.65,
        "opportunity_score": 0.71,
        "score_reasoning": "Quality startup with reasonable visibility"
      },
      "chemistry": {
        "inroad_score": 75.8,
        "structural_explanation": "Moderate fit with some network overlap",
        "shared_contexts_count": 1,
        "shared_contexts_summary": "Both active in startup community",
        "employee_interactions": [],
        "engagement_strength": 0.4,
        "best_connector_name": "James Wilson",
        "best_connector_intro": "Attended same hackathon series",
        "entry_probability": 0.6,
        "team_fit_category": "neutral",
        "team_chemistry_score": 0.7,
        "way_in_strategy": "You both have connections to the startup accelerator community — leverage that shared circle.",
        "way_in_confidence": 0.68
      }
    }
  ],
  "summary": {
    "total_opportunities_evaluated": 10,
    "top_opportunities_matched": 3,
    "average_fit_score": 84.93,
    "highest_fit_score": 87.45,
    "seniority_level": "Senior Engineer",
    "primary_domain": "Backend + ML Infrastructure"
  }
}
```

---

### Error Handling

| Scenario                          | HTTP Status | Response                                                                                          |
| --------------------------------- | ----------- | ------------------------------------------------------------------------------------------------- |
| Invalid input (resume < 10 chars) | 400         | `{"status": "error", "detail": "Resume text must be at least 10 characters", "status_code": 400}` |
| Profile extraction fails          | 400         | `{"status": "error", "detail": "Failed to extract candidate profile: ...", "status_code": 400}`   |
| Opportunity matching fails        | 500         | `{"status": "error", "detail": "Failed to match opportunities: ...", "status_code": 500}`         |
| Unexpected error                  | 500         | `{"status": "error", "detail": "An unexpected error occurred", "status_code": 500}`               |

---

## 🧪 Testing Strategy

### Test Files

Located in `tests/` directory:

| File                | Purpose                                     | Owner    |
| ------------------- | ------------------------------------------- | -------- |
| `test_api.py`       | Full `/analyze` endpoint end-to-end testing | Member B |
| `test_profile.py`   | Member A profile extraction unit tests      | Member A |
| `test_discovery.py` | Member B opportunity scoring and ranking    | Member B |
| `test_matching.py`  | Member A relevance matching and embeddings  | Member A |

---

### Running Tests

#### All Tests:

```bash
pytest
```

#### Specific Test File:

```bash
pytest tests/test_api.py -v
```

#### With Coverage Report:

```bash
pytest --cov=. tests/
```

#### Single Test Function:

```bash
pytest tests/test_api.py::test_analyze_endpoint -v
```

#### Watch Mode (auto-run on changes):

```bash
pytest-watch
```

---

### Manual API Testing

#### Option 1: cURL

**Health Check:**

```bash
curl -X GET "http://localhost:8000/"
```

**Analyze Candidate:**

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python developer with 3 years building FastAPI applications",
    "project_descriptions": "- Built ML inference API using FastAPI and TensorFlow\n- Developed data pipeline for 100K+ records"
  }'
```

---

#### Option 2: Python Requests

```python
import requests
import json

# Health check
response = requests.get("http://localhost:8000/")
print(json.dumps(response.json(), indent=2))

# Analyze candidate
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "resume_text": "Your resume text here...",
        "project_descriptions": "Your projects here..."
    }
)
print(json.dumps(response.json(), indent=2))
```

---

#### Option 3: Interactive API Documentation

Once server is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc (Alternative UI):** http://localhost:8000/redoc

Both provide:

- Live request builder
- Schema visualization
- Response examples
- Try-it-out functionality

---

### Starting the Server

#### Option 1: Direct Python Execution

```bash
python main.py
```

#### Option 2: Uvicorn with Auto-Reload

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Option 3: Uvicorn with Custom Workers

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server will be available at: **http://localhost:8000**

---

## 📦 Dependencies

### Core Packages (requirements.txt)

| Package                   | Version | Purpose                           |
| ------------------------- | ------- | --------------------------------- |
| **fastapi**               | Latest  | Web framework for APIs            |
| **uvicorn**               | Latest  | ASGI server                       |
| **pydantic**              | Latest  | Request/response validation       |
| **sentence-transformers** | Latest  | Generate embeddings locally       |
| **transformers**          | Latest  | Hugging Face transformer models   |
| **torch**                 | Latest  | PyTorch for ML inference          |
| **tf-keras**              | Latest  | Keras for deep learning           |
| **numpy**                 | Latest  | Numerical computing               |
| **openai**                | Latest  | OpenAI API integration (optional) |
| **google-generativeai**   | Latest  | Google AI integration (optional)  |
| **python-dotenv**         | Latest  | Environment variable management   |
| **pytest**                | Latest  | Testing framework                 |
| **cors**                  | Latest  | CORS middleware support           |

---

## 📊 Data Flow Detailed

### Complete Pipeline Execution

```
1. CLIENT SENDS REQUEST
   POST /analyze
   {
     "resume_text": "...",
     "project_descriptions": "..."
   }

2. FASTAPI RECEIVES & VALIDATES
   - Check resume_text min length: 10 chars ✓
   - Check project_descriptions min length: 10 chars ✓
   - Parse JSON schema ✓

3. MEMBER A: PROFILE EXTRACTION
   Input: resume_text + project_descriptions
   Process:
     a. Tokenize and analyze text
     b. Extract 7 signals using NLP/ML
     c. Generate embedding for candidate profile
   Output:
     {
       "core_skills": [...],
       "ownership_signals": [...],
       "measurable_outcomes": [...],
       "problem_solving_patterns": [...],
       "domain_expertise": [...],
       "seniority_level": "...",
       "semantic_summary": "..."
     }

4. MEMBER B: OPPORTUNITY DISCOVERY & SCORING
   Input: None (internal dataset)
   Process:
     a. Load 10 mock opportunities from dataset.py
     b. For each opportunity:
        - Calculate competition_index (0.0-1.0)
        - Calculate response_probability (0.0-1.0)
        - Calculate growth_potential (0.0-1.0)
        - Calculate referral_likelihood (0.0-1.0)
        - Combine: opportunity_score = avg of 4 signals
     c. Sort by opportunity_score (descending)
     d. Select top 3
   Output:
     [
       {
         "id": 1,
         "title": "...",
         "company": "...",
         "scores": {...},
         "opportunity_score": 0.805
       },
       ...
     ]

5. MEMBER A: RELEVANCE MATCHING
   Input: candidate_profile + top_3_opportunities
   Process:
     a. Generate embedding for each opportunity
     b. Calculate cosine_similarity(candidate_embedding, opportunity_embedding)
     c. Convert to fit_score (0-100)
     d. Generate match_reasoning using candidate signals
   Output:
     [
       {
         "opportunity_id": 1,
         "fit_score": 87.45,
         "match_reasoning": "..."
       },
       ...
     ]

6. AGENT 3: INROAD CHEMISTRY ANALYSIS
   For each top 3 opportunity:

   a. CONTEXT DETECTOR
      Input: candidate_profile + opportunity metadata
      Process: Compare candidate communities/hackathons/etc vs target team
      Output: shared_contexts[], total_overlap_score, summary

   b. CONNECTOR FINDER
      Input: candidate_profile + opportunity metadata
      Process: Identify 2nd-degree bridges in networks
      Output: connectors[], best_connector, entry_probability

   c. ENGAGEMENT CHECKER
      Input: candidate_profile + opportunity metadata
      Process: Check if company employees interacted with candidate's work
      Output: employee_interactions[], engagement_strength

   d. TEAM ANALYZER
      Input: candidate_profile + opportunity team metadata
      Process: Analyze team composition fit
      Output: team_fit_category, team_chemistry_score

   e. INROAD CALCULATOR
      Input: All above signals + role_fit_score + competition_index
      Process: Combine using weighted formula:
        inroad_score = (
          role_fit × 0.40 +
          team_overlap × 0.20 +
          entry_probability × 0.30 +
          competition × 0.10
        )
      Output: inroad_score, structural_explanation

   f. WAY IN GENERATOR
      Input: All signals from a-e
      Process: Find highest-value signal, generate actionable sentence
      Output: actionable_sentence, primary_signal, confidence

7. AGGREGATION & FORMATTING
   Combine all data:
     - candidate_profile (Member A output)
     - matched_opportunities (Member B + A + Agent 3 outputs)
     - summary statistics

   Create response object: AnalyzeResponse

8. RESPONSE SENT TO CLIENT
   HTTP 200 OK
   {
     "status": "success",
     "timestamp": "...",
     "candidate_profile": {...},
     "matched_opportunities": [...],
     "summary": {...}
   }
```

---

## 🎓 Key Features

### 1. **AI-Powered Profile Extraction**

- Member A automatically extracts 7 key signals from resume + projects
- No manual tagging required
- Uses Hugging Face transformers (local, no external API calls)

### 2. **Hidden Opportunity Discovery**

- Member B surfaces opportunities from non-traditional sources
- Founder posts, GitHub repositories, employee referrals, newsletters, hackathons
- Algorithmic ranking prevents job board bias

### 3. **Human Network Analysis** ⭐

- Agent 3 detects real paths to introductions
- Identifies shared communities, connector persons, engagement signals
- Generates specific, actionable entry strategies
- Moves beyond skill matching to actual hiring mechanics

### 4. **Semantic Matching with Embeddings**

- Vector similarity instead of keyword matching
- Understands contextual relevance
- More accurate than TF-IDF or regex patterns

### 5. **Production-Ready API**

- Full error handling and validation
- CORS enabled for frontend development
- Pydantic models for type safety
- Comprehensive logging for debugging

---

## 🚀 Frontend Integration

### Quick Start for Frontend Developers

1. **Ensure server is running:**

   ```bash
   python main.py
   ```

2. **Make API call from frontend:**

   ```javascript
   const response = await fetch("http://localhost:8000/analyze", {
     method: "POST",
     headers: { "Content-Type": "application/json" },
     body: JSON.stringify({
       resume_text: candidateResume,
       project_descriptions: candidateProjects,
     }),
   });
   const data = await response.json();
   ```

3. **Render the response:**
   - Display `candidate_profile` in profile section
   - Render `matched_opportunities` as cards
   - Show `chemistry.way_in_strategy` as key insight
   - Display `chemistry.inroad_score` as opportunity score

### CORS Configuration

Already enabled for all origins in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### Example Frontend Flow

```
1. User enters resume + projects
   ↓
2. Frontend validates input (min 10 chars each)
   ↓
3. POST /analyze call
   ↓
4. Display loading indicator (typical response: 2-5 seconds)
   ↓
5. Parse response:
   - Show candidate profile summary
   - Render 3 opportunities as ranked cards
   - For each opportunity:
     * Display title, company, source type
     * Show fit_score as percentage bar
     * Display match_reasoning in tooltip
     * Highlight way_in_strategy in bold
     * Show inroad_score as "Opportunity Quality"
   ↓
6. Click opportunity → show full scoring breakdown
   - competition_index, response_probability, growth_potential, referral_likelihood
   - shared_contexts with names
   - connector_person with relationship details
   - team_chemistry_score reasoning
```

---

## 🔧 Debugging & Development

### Enable Verbose Logging

Edit `main.py`:

```python
import logging

# Change from INFO to DEBUG
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### View Detailed Error Messages

Check terminal output when running `python main.py`:

```
INFO:     Application startup complete
INFO:     Step 1: Extracting candidate profile...
INFO:     Profile extracted successfully: Senior Engineer
INFO:     Step 2: Ranking opportunities...
INFO:     Ranked top 3 opportunities by score
DEBUG:    Opportunity 1 scores: {...}
...
```

### Test Individual Components

```python
# Test Member A profile extraction
from member_a.profile_extractor import extract_candidate_profile

profile = extract_candidate_profile(
    "Your resume text...",
    "Your project descriptions..."
)
print(profile)

# Test Member B opportunity scoring
from member_b.scorer import rank_opportunities
from member_b.dataset import get_mock_opportunities

opps = get_mock_opportunities()
ranked = rank_opportunities(opps, top_k=3)
print(ranked)

# Test Agent 3 chemistry
from agent_3.context_detector import detect_shared_contexts

contexts = detect_shared_contexts(profile, opps[0])
print(contexts)
```

---

## 📈 Performance Metrics

| Operation            | Typical Duration | Notes                             |
| -------------------- | ---------------- | --------------------------------- |
| Profile extraction   | 500ms - 1s       | NLP processing                    |
| Opportunity ranking  | 50ms             | Simple scoring                    |
| Relevance matching   | 1-2s             | Embedding generation + similarity |
| Chemistry analysis   | 1-2s             | 6 sub-analyses                    |
| **Total end-to-end** | **2-5s**         | Depends on model size             |

---

## 🎯 Next Steps & Enhancements

### MVP Features (Complete ✓)

- ✓ Profile extraction
- ✓ Opportunity discovery
- ✓ Semantic matching
- ✓ Chemistry analysis
- ✓ API endpoints
- ✓ Error handling

### Potential Enhancements

1. **Batch Processing**
   - Add `/analyze-batch` endpoint for multiple candidates

2. **Persistent Storage**
   - Cache opportunities in database
   - Store user profiles and matches

3. **Dynamic Opportunities**
   - Connect real job boards (LinkedIn, AngelList, etc.)
   - Real-time scraping of GitHub/newsletters

4. **Custom Weights**
   - Allow users to adjust scoring weights
   - Personalized ranking by seniority/domain

5. **Extended Feedback**
   - User feedback on matches
   - ML model retraining loop

6. **Advanced UI**
   - Match timeline visualization
   - Network graph of connectors
   - Opportunity comparison charts

---

## 📝 File Structure

```
Let-s-hack-in/
├── main.py                          # FastAPI application
├── config.py                        # Configuration (minimal)
├── requirements.txt                 # Dependencies
│
├── member_a/                        # Profile Extraction & Matching
│   ├── __init__.py
│   ├── profile_extractor.py        # Extract candidate signals
│   ├── relevance_matching.py       # Semantic matching
│   └── embeddings.py               # Embedding generation
│
├── member_b/                        # Opportunity Engine
│   ├── __init__.py
│   ├── dataset.py                  # 10 mock opportunities
│   └── scorer.py                   # Opportunity scoring
│
├── agent_3/                         # Chemistry Analysis
│   ├── __init__.py
│   ├── context_detector.py         # Shared contexts
│   ├── connector.py                # Connector finding
│   ├── engagement.py               # Engagement signals
│   ├── team_analyzer.py            # Team fit analysis
│   ├── calculator.py               # InRoad score
│   └── way_in.py                   # Entry strategy
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_api.py                 # End-to-end API tests
│   ├── test_profile.py             # Member A tests
│   ├── test_discovery.py           # Member B tests
│   └── test_matching.py            # Matching tests
│
├── data/                            # Data storage
│   └── mock_opportunities.json     # Mock data
│
└── MEMBER_B_DOCUMENTATION.md        # Original Member B docs
└── SYSTEM_OVERVIEW.md               # This file
```

---

## 🚀 Quick Start Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start server: `python main.py`
- [ ] Check health: `curl http://localhost:8000/`
- [ ] Test API: Visit `http://localhost:8000/docs`
- [ ] Run tests: `pytest`
- [ ] Integrate frontend: Call `POST /analyze` from frontend
- [ ] Monitor logs: Check terminal output for debugging
- [ ] Deploy: Configure CORS + security for production

---

## 📞 Support & Debugging

### Common Issues

**Issue: "Module not found" errors**

- Solution: Ensure virtual environment is activated and `pip install -r requirements.txt` is run

**Issue: Port 8000 already in use**

- Solution: `uvicorn main:app --port 8001` or kill existing process

**Issue: Slow embedding generation**

- Solution: This is normal for first run (models download). Subsequent runs are faster due to caching.

**Issue: Low inroad scores**

- Solution: This is realistic! Most opportunities won't have perfect chemistry. Focus on high-score matches.

---

## Summary

✅ **Complete 4-member intelligent opportunity-matching system**

**Members:**

- **Member A:** Profile extraction + semantic matching
- **Member B:** Hidden opportunity discovery + scoring
- **Agent 3:** InRoad chemistry analysis + entry strategies
- **FastAPI:** REST API + frontend integration

**Features:**

- AI-powered profile extraction (7 signals)
- Hidden opportunity discovery (5 source types)
- Semantic matching with embeddings
- Human network analysis (4 chemistry signals)
- InRoad scoring (combined 0-100)
- Actionable entry strategies
- Production-ready API
- Comprehensive testing

**Ready to use!** 🎯
