# Agent 4 — Skill Proof Agent

## Overview

Agent 4 is a comprehensive skill assessment system that parses portfolio descriptions, calculates algorithmic trust scores for claimed technical competencies, and builds data structures suitable for frontend visualization.

The agent analyzes project narratives through multiple lenses:

- **Ownership depth**: Distinguishes leadership vs. contribution vs. assistance
- **Outcome clarity**: Separates vague claims from measurable proofs
- **Problem complexity**: Identifies novel challenges vs. routine work
- **Skill confidence**: Aggregates multiple signals into 0-100 trust scores

## Architecture

### Core Modules

#### 1. **parser.py** — Project Narrative Parser

Breaks down unstructured project descriptions into structured components:

- `what_was_built`: Core product/feature description
- `candidate_role`: Specific role(s) the candidate took
- `outcome`: Results and impact statements
- `decisions_made`: Technical and strategic decisions (list)
- `challenges_faced`: Problems encountered and resolved (list)

**Key Functions:**

- `parse_project_narrative(text)` → `ProjectNarrative`

**Example:**

```python
from agent_4 import parse_project_narrative

description = "I led development of a real-time event streaming platform..."
narrative = parse_project_narrative(description)
print(narrative.what_was_built)  # Extracted product description
print(narrative.candidate_role)   # Extracted role information
```

---

#### 2. **ownership.py** — Ownership Depth Detector

Analyzes linguistic patterns to classify candidate's level of ownership/contribution.

**Classification Levels:**

- `"led"` (0.75-1.0 action verb score): Strong leadership indicators
- `"contributed"` (0.50-0.75): Active contribution indicators
- `"assisted"` (below 0.50): Supporting/learning roles

**Detection Method:**

- Scores action verbs: strong verbs (led, architected, designed) vs. weak (used, attended, learned)
- Flags `is_vague` if language is passive or lacks specific ownership indicators
- Returns `action_verb_score`, `confidence`, and key `evidence`

**Key Functions:**

- `detect_ownership_level(narrative_text, role_text)` → `OwnershipAnalysis`

**Example:**

```python
ownership = detect_ownership_level(project_description)
print(f"Level: {ownership.ownership_level}")           # "led"
print(f"Action Verb Score: {ownership.action_verb_score}")  # 0.85
print(f"Is Vague: {ownership.is_vague}")               # False
```

---

#### 3. **outcome_scorer.py** — Outcome Clarity Scorer

Evaluates outcome statements for concrete metrics vs. vague claims.

**Metrics Detected:**

- Percentages: "40%", "improved by 50%"
- Counts: "10k users", "500 downloads"
- Time: "reduced latency to 100ms"
- Ratios: "2x faster", "3-fold improvement"
- Financial: "$2M revenue"

**Clarity Score (0-1):**

- 0.95+: 3+ metrics identified
- 0.75-0.95: Specific outcomes with some metrics
- 0.55-0.75: Mix of vague and measurable
- Below 0.55: Mostly unquantified claims

**Key Functions:**

- `score_outcome_clarity(outcome_text)` → `OutcomeClarityScore`

**Example:**

```python
clarity = score_outcome_clarity("Reduced latency by 40%, improved throughput 3x")
print(f"Clarity Score: {clarity.clarity_score}")  # 0.95
print(f"Is Specific: {clarity.is_specific}")      # True
print(f"Measures: {len(clarity.measures_found)}")  # 2 metrics
```

---

#### 4. **complexity.py** — Problem Complexity Evaluator

Assesses whether the project involved routine work or novel challenges.

**Complexity Indicators:**

- Constraints (distributed systems, compliance, legacy code)
- Failures (debugging critical issues, handling edge cases)
- Trade-offs (architectural decisions, technology choices, refactoring)
- Scale (millions of users, billions of data points)
- Novel approaches (innovative algorithms, new patterns)

**Classification:**

- `"novel"` (score >= 0.65): Multiple complexity indicators
- `"routine"` (score < 0.65): Standard engineering practices

**Key Functions:**

- `evaluate_complexity(narrative_text, challenges_list, outcome_text)` → `ComplexityRating`

**Example:**

```python
complexity = evaluate_complexity(project_description)
print(f"Level: {complexity.complexity_level}")        # "novel"
print(f"Score: {complexity.complexity_score}")        # 0.79
print(f"Indicators: {complexity.indicators_found}")   # [constraint, failure, novel]
```

---

#### 5. **confidence.py** — Skill Confidence Score Generator

Aggregates ownership, outcome clarity, and complexity into skill confidence scores (0-100).

**Formula:**

```
confidence = (
    ownership_score × 0.35 +      # How much did candidate lead?
    outcome_clarity × 0.30 +       # How measurable were results?
    complexity_score × 0.20 +      # How novel/complex was the work?
    frequency_score × 0.15         # How often demonstrated?
) × 100
```

**Proficiency Levels:**

- 85-100: Expert
- 70-84: Advanced
- 55-69: Intermediate
- Below 55: Novice

**Key Functions:**

- `calculate_confidence_score(skill_name, ownership, clarity, complexity, ...)` → `SkillConfidenceScore`
- `extract_skills_from_text(narrative)` → `List[str]`

**Example:**

```python
confidence = calculate_confidence_score(
    "Python",
    ownership_analysis,
    outcome_clarity,
    complexity_rating,
    project_count=2
)
print(f"Skill: {confidence.skill_name}")           # "Python"
print(f"Score: {confidence.confidence_score}/100")  # 85.7
print(f"Level: {confidence.proficiency_level}")     # "expert"
```

---

#### 6. **graph_builder.py** — Skill Graph Builder

Constructs a graph structure where nodes are skills and edges are projects providing evidence.

**Data Structures:**

- `SkillNode`: Represents a technical skill with:
  - `id`: Normalized skill identifier
  - `name`: Display name
  - `proficiency_level`: Overall proficiency
  - `overall_confidence`: Average confidence across projects
  - `project_count`: Number of evidence projects

- `SkillEdge`: Links skill to project evidence with:
  - `source_skill_id`: Which skill
  - `target_project_id`: Which project
  - `confidence_score`: Skill confidence for this project
  - `evidence_summary`: One-line summary for UI
  - `ownership_level`: "led", "contributed", or "assisted"
  - `outcome_metrics_count`: Number of quantified outcomes

**Key Functions:**

- `build_skill_graph(confidence_scores_by_skill)` → `SkillGraph`
- `graph_to_dict(graph)` → `Dict` (JSON-ready format)

**Example:**

```python
# After calculating confidence scores for multiple skills/projects
graph = build_skill_graph({
    "Python": [confidence_score_1, confidence_score_2],
    "Kubernetes": [confidence_score_3],
    # ...
})

# Stats available
print(f"Skills: {graph.stats['total_skills']}")
print(f"Edges: {graph.stats['total_edges']}")
print(f"Avg Confidence: {graph.stats['average_skill_confidence']:.1f}/100")

# Export to JSON
graph_dict = graph_to_dict(graph)
```

---

#### 7. **proof_card.py** — Proof Card Generator

Filters the skill graph to generate targeted proof cards for specific job opportunities.

**Workflow:**

1. Extract required skills from opportunity description
2. Calculate relevance of candidate's skills to requirements
3. Select top 3-5 most relevant skills
4. Include best project evidence for each skill

**Output (ProofCard):**

- `opportunity_title`: Job title
- `required_skills`: Skills listed in posting
- `matched_skills`: Top matching skills with evidence
- `total_relevance_score`: Average match quality (0-100)
- `summary`: One-line summary

**Key Functions:**

- `generate_proof_card(skill_graph, opportunity_description, title, max_skills)` → `ProofCard`
- `proof_card_to_dict(proof_card)` → `Dict` (JSON-ready)

**Example:**

```python
opportunity = """
Senior Backend Engineer role:
Required: Python, Kubernetes, PostgreSQL, System Design
Preferred: Distributed systems, Kafka
"""

proof_card = generate_proof_card(graph, opportunity, "Senior Backend Engineer")
print(proof_card.summary)  # "Strong match: Python, Kubernetes, PostgreSQL (95/100)"
for skill in proof_card.matched_skills:
    print(f"- {skill.skill_name}: {skill.confidence_score:.1f}/100")
```

---

## Complete Workflow

```python
from agent_4 import (
    parse_project_narrative,
    detect_ownership_level,
    score_outcome_clarity,
    evaluate_complexity,
    calculate_confidence_score,
    build_skill_graph,
    generate_proof_card,
)

# 1. Parse portfolio project
narrative = parse_project_narrative(project_description)

# 2. Analyze ownership
ownership = detect_ownership_level(project_description)

# 3. Score outcome clarity
clarity = score_outcome_clarity(narrative.outcome)

# 4. Evaluate complexity
complexity = evaluate_complexity(project_description)

# 5. Calculate skill confidence (for each detected skill)
skills = extract_skills_from_text(project_description)
confidence_by_skill = {}
for skill in skills:
    confidence_by_skill[skill] = calculate_confidence_score(
        skill, ownership, clarity, complexity
    )

# 6. Build graph from multiple projects
full_graph = build_skill_graph(confidence_scores_by_all_skills)

# 7. Generate proof card for opportunity
proof_card = generate_proof_card(full_graph, opportunity_description)
```

---

## Output Formats

### Skill Graph (JSON)

```json
{
  "nodes": [
    {
      "id": "python",
      "label": "Python",
      "proficiency": "expert",
      "confidence": 94.5,
      "projectCount": 2
    }
  ],
  "edges": [
    {
      "source": "python",
      "target": "project_1",
      "confidence": 85.7,
      "evidence": "Led Python work: expert proficiency",
      "ownership": "led",
      "metrics": 3
    }
  ],
  "stats": {
    "totalSkills": 8,
    "totalEdges": 10,
    "averageConfidence": 92.3,
    "topSkills": [...]
  }
}
```

### Proof Card (JSON)

```json
{
  "opportunity": {
    "title": "Senior Backend Engineer",
    "requiredSkills": ["Python", "Kubernetes", "PostgreSQL", ...]
  },
  "matched_skills": [
    {
      "name": "Python",
      "confidence": 94.5,
      "proficiency": "expert",
      "evidence": "Led Python work in event streaming platform",
      "projectCount": 2
    }
  ],
  "match": {
    "relevanceScore": 94.5,
    "summary": "Strong match: Python, Kubernetes, PostgreSQL (95/100)"
  }
}
```

---

## Pydantic Schemas

All data structures use Pydantic v2 for:

- Type validation
- JSON serialization
- Documentation via field descriptions
- Field constraints (ge=0, le=100, etc.)

---

## Files

```
agent_4/
├── __init__.py              # Module exports
├── parser.py                # Project narrative parsing
├── ownership.py             # Ownership depth detection
├── outcome_scorer.py        # Outcome clarity evaluation
├── complexity.py            # Problem complexity assessment
├── confidence.py            # Skill confidence scoring
├── graph_builder.py         # Skill graph construction
└── proof_card.py            # Opportunity-targeted proof cards
```

---

## Testing

Run the comprehensive workflow:

```bash
python example_agent_4_complete_workflow.py
```

Quick test suite:

```bash
python test_agent_4.py
```

---

## Design Principles

1. **Modular**: Each component is independent and composable
2. **Production-ready**: Full type hints, Pydantic validation, error handling
3. **Heuristic-based**: Uses regex and keyword matching for local execution
4. **Frontend-friendly**: Output formats ready for visualization
5. **Deterministic**: No LLM calls, consistent results
6. **Transparent**: Evidence strings explain each score

---

## Scoring Philosophy

Agent 4 doesn't assume competency claims are fraudulent. Instead, it:

- Rewards **demonstrated leadership** over participation
- Requires **measurable outcomes** to confirm impact
- Recognizes **novel challenges** as indicators of depth
- Weights **frequency** of skill usage across projects

The confidence score represents "algorithmic trust" — how much evidence supports the claimed competency level.
