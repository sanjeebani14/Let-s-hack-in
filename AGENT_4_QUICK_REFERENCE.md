# Agent 4 Quick Reference Guide

## Module Imports

```python
# Import everything
from agent_4 import *

# Or specific components
from agent_4 import (
    parse_project_narrative,
    detect_ownership_level,
    score_outcome_clarity,
    evaluate_complexity,
    calculate_confidence_score,
    extract_skills_from_text,
    build_skill_graph,
    generate_proof_card,
    graph_to_dict,
    proof_card_to_dict,
)
```

---

## Module-by-Module Examples

### 1. Parser - Breaking Down Project Narratives

```python
from agent_4 import parse_project_narrative

project_description = """
I led the development of a real-time event streaming platform using Python
and Apache Kafka. Architected distributed system handling 2M events/second
with <100ms latency. Managed 4-person engineering team.

Overcame consensus challenges with custom Kafka offset management.
Reduced data loss incidents to zero and achieved 99.99% consistency.
Used Kubernetes for orchestration, migrated from RabbitMQ.
"""

narrative = parse_project_narrative(project_description)

# Extracted components:
print(narrative.what_was_built)      # "Real-time event streaming platform..."
print(narrative.candidate_role)      # "Led the development of a..."
print(narrative.outcome)             # "Reduced data loss incidents..."
print(narrative.decisions_made)      # ["Used Kubernetes...", "migrated from..."]
print(narrative.challenges_faced)    # ["Overcame consensus challenges..."]
```

---

### 2. Ownership - Detecting Leadership Depth

```python
from agent_4 import detect_ownership_level

# From the narrative above
ownership = detect_ownership_level(project_description)

print(f"Level: {ownership.ownership_level}")         # "led"
print(f"Action Verb Score: {ownership.action_verb_score}")  # 0.86
print(f"Is Vague: {ownership.is_vague}")             # False
print(f"Confidence: {ownership.confidence:.2f}")     # 0.94
print(f"Evidence: {ownership.evidence}")             # "Architected distributed system..."

# Possible levels: "led", "contributed", "assisted"
```

---

### 3. Outcome Scorer - Finding Concrete Metrics

```python
from agent_4 import score_outcome_clarity

outcome_text = "Reduced data loss incidents by 100%, improved consistency from 99.9% to 99.99%"

clarity = score_outcome_clarity(outcome_text)

print(f"Clarity Score: {clarity.clarity_score:.2f}")        # 0.95
print(f"Is Specific: {clarity.is_specific}")                # True
print(f"Is Vague: {clarity.is_vague}")                      # False
print(f"Metrics Found: {len(clarity.measures_found)}")      # 3

# Inspect individual metrics:
for measure in clarity.measures_found:
    print(f"  - {measure.metric_type}: {measure.value} {measure.unit}")
    # Outputs:
    # - percentage: 100 %
    # - percentage: 99.9 %
    # - percentage: 99.99 %

print(f"Summary: {clarity.summary}")                        # "Clear & measurable: 3 metrics identified"
```

---

### 4. Complexity - Assessing Challenge Level

```python
from agent_4 import evaluate_complexity

complexity = evaluate_complexity(project_description)

print(f"Complexity Level: {complexity.complexity_level}")    # "novel"
print(f"Complexity Score: {complexity.complexity_score:.2f}") # 0.79
print(f"Summary: {complexity.summary}")                      # "Novel complexity: constraint, failure, novel"

# View indicators:
for indicator in complexity.indicators_found:
    print(f"\n{indicator.indicator_type}:")
    print(f"  {indicator.description}")
    print(f"  Weight: {indicator.weight:.2f}")

# Possible levels: "routine", "novel"
```

---

### 5. Confidence - Aggregating All Signals

```python
from agent_4 import calculate_confidence_score, extract_skills_from_text

# Extract skills mentioned in project
skills = extract_skills_from_text(project_description)
print(f"Detected skills: {skills}")  # ["Python", "Apache Kafka", "Kubernetes", ...]

# Calculate confidence for one skill
confidence = calculate_confidence_score(
    skill_name="Python",
    ownership_analysis=ownership,
    outcome_clarity=clarity,
    complexity_rating=complexity,
    project_count=1,
    skill_frequency=1.0
)

print(f"Skill: {confidence.skill_name}")                           # "Python"
print(f"Confidence Score: {confidence.confidence_score:.1f}/100")   # 85.7
print(f"Proficiency: {confidence.proficiency_level}")              # "expert"
print(f"Evidence Projects: {confidence.evidence_projects}")        # 1
print(f"Summary: {confidence.summary}")                            # "Expert: 85.7/100 - led with measurable outcomes"

# Possible proficiency levels: "novice", "intermediate", "advanced", "expert"

# View component breakdown:
for component in confidence.components:
    print(f"\n{component.component_name}:")
    print(f"  Score: {component.score:.2f}")
    print(f"  Weight: {component.weight:.0%}")
    print(f"  Contribution: {component.weighted_contribution:.2f}")
```

---

### 6. Graph Builder - Creating Skill Visualization Structure

```python
from agent_4 import build_skill_graph, graph_to_dict

# Assume we have confidence scores for multiple skills and projects
confidence_scores_by_skill = {
    "Python": [confidence_score_1, confidence_score_2],
    "Kubernetes": [confidence_score_3],
    "PostgreSQL": [confidence_score_4],
    # ... more skills
}

# Build the graph
graph = build_skill_graph(confidence_scores_by_skill)

# Access graph structure
print(f"Total Skills: {len(graph.nodes)}")                    # 8
print(f"Total Skill-Project Links: {len(graph.edges)}")      # 12
print(f"Average Confidence: {graph.stats['average_skill_confidence']:.1f}/100")  # 92.3

# Get top skills
top_3 = graph.stats['top_skills'][:3]
for skill in top_3:
    print(f"- {skill.name}: {skill.overall_confidence:.1f}/100 ({skill.proficiency_level})")

# Export to JSON for frontend
graph_dict = graph_to_dict(graph)
print(f"Frontend Format Nodes: {len(graph_dict['nodes'])}")
print(f"Frontend Format Edges: {len(graph_dict['edges'])}")

# Save to JSON file
import json
with open("skill_graph.json", "w") as f:
    json.dump(graph_dict, f, indent=2)
```

---

### 7. Proof Card - Filtering for Specific Opportunities

```python
from agent_4 import generate_proof_card, proof_card_to_dict

opportunity_description = """
We're hiring a Senior Backend Engineer.

Required Skills:
- Python (5+ years)
- Kubernetes
- PostgreSQL
- System Design & Distributed Systems

Preferred:
- Apache Kafka or similar streaming platforms
- High-performance/low-latency systems
- TensorFlow or ML infrastructure
"""

# Generate proof card filtered to this opportunity
proof_card = generate_proof_card(
    skill_graph=graph,
    opportunity_description=opportunity_description,
    opportunity_title="Senior Backend Engineer",
    max_skills=5,
    min_confidence=50.0
)

print(f"Opportunity: {proof_card.opportunity_title}")
print(f"Required Skills: {proof_card.required_skills}")
print(f"Match Relevance: {proof_card.total_relevance_score:.1f}/100")
print(f"Summary: {proof_card.summary}")

# View matched skills
print(f"\nMatched Skills ({len(proof_card.matched_skills)}):")
for skill in proof_card.matched_skills:
    print(f"\n  {skill.skill_name}")
    print(f"    Confidence: {skill.confidence_score:.1f}/100 ({skill.proficiency_level})")
    print(f"    Evidence: {skill.best_project_evidence}")
    print(f"    Project Count: {skill.project_count}")

# Export to JSON for frontend
card_dict = proof_card_to_dict(proof_card)
with open("proof_card.json", "w") as f:
    json.dump(card_dict, f, indent=2)
```

---

## Complete End-to-End Workflow

```python
from agent_4 import *
import json

# Sample projects
projects = [
    {
        "id": "project_1",
        "text": "I led development of a real-time event platform using Python..."
    },
    {
        "id": "project_2",
        "text": "Built a React dashboard for monitoring distributed systems..."
    }
]

# 1. Parse all projects
parsed = []
for project in projects:
    narrative = parse_project_narrative(project["text"])
    parsed.append((project["id"], narrative, project["text"]))

# 2. Analyze each project
confidence_by_skill = {}

for project_id, narrative, full_text in parsed:
    # Get all components
    ownership = detect_ownership_level(full_text)
    clarity = score_outcome_clarity(narrative.outcome)
    complexity = evaluate_complexity(full_text)

    # Calculate confidence for each skill
    skills = extract_skills_from_text(full_text)
    for skill in skills:
        if skill not in confidence_by_skill:
            confidence_by_skill[skill] = []

        conf = calculate_confidence_score(
            skill, ownership, clarity, complexity, project_count=1
        )
        confidence_by_skill[skill].append(conf)

# 3. Build graph
graph = build_skill_graph(confidence_by_skill)

# 4. Generate proof cards for opportunities
opportunities = [
    {
        "title": "Senior Backend Engineer",
        "description": "Required: Python, Kubernetes, PostgreSQL..."
    },
    {
        "title": "Full Stack Engineer",
        "description": "Required: React, Python, REST APIs..."
    }
]

results = {
    "graph": graph_to_dict(graph),
    "proofCards": []
}

for opp in opportunities:
    card = generate_proof_card(
        graph,
        opp["description"],
        opp["title"],
        max_skills=5
    )
    results["proofCards"].append(proof_card_to_dict(card))

# 5. Export results
with open("agent4_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("✓ Analysis complete!")
print(f"  - Skills identified: {len(graph.nodes)}")
print(f"  - Average confidence: {graph.stats['average_skill_confidence']:.1f}/100")
print(f"  - Opportunities analyzed: {len(results['proofCards'])}")
```

---

## Common Patterns

### Pattern 1: Single Project Analysis

```python
# Quick analysis of one project
project_text = "I built a Python microservice that..."

narrative = parse_project_narrative(project_text)
ownership = detect_ownership_level(project_text)
clarity = score_outcome_clarity(narrative.outcome)
complexity = evaluate_complexity(project_text)

print(f"{ownership.ownership_level} - {clarity.clarity_score:.1f} clarity - {complexity.complexity_level}")
```

### Pattern 2: Multiple Skills from One Project

```python
# Get confidence scores for all skills in a project
skills = extract_skills_from_text(project_text)
scores = {}

for skill in skills:
    scores[skill] = calculate_confidence_score(
        skill, ownership, clarity, complexity
    )

# Show top 3 by confidence
top_3 = sorted(scores.items(), key=lambda x: x[1].confidence_score, reverse=True)[:3]
for skill_name, score in top_3:
    print(f"{skill_name}: {score.confidence_score:.1f}")
```

### Pattern 3: Batch Processing Portfolio

```python
# Process entire portfolio and generate comprehensive profile
portfolio = {
    "project_1": "description...",
    "project_2": "description...",
    "project_3": "description...",
}

all_scores = {}

for project_id, description in portfolio.items():
    narrative = parse_project_narrative(description)
    ownership = detect_ownership_level(description)
    clarity = score_outcome_clarity(narrative.outcome)
    complexity = evaluate_complexity(description)

    for skill in extract_skills_from_text(description):
        if skill not in all_scores:
            all_scores[skill] = []
        all_scores[skill].append(
            calculate_confidence_score(skill, ownership, clarity, complexity)
        )

# Build complete skill profile
graph = build_skill_graph(all_scores)
```

---

## Scoring Reference

### Ownership Levels

- **"led"**: Strong leadership verbs (architect, design, lead, etc.)
- **"contributed"**: Active participation (implement, develop, handle)
- **"assisted"**: Supporting roles (helped, learned, attended)

### Outcome Clarity Scale

- **0.95-1.0**: 3+ concrete metrics identified
- **0.75-0.94**: Specific outcomes with metrics
- **0.55-0.74**: Mix of vague and measurable
- **Below 0.55**: Mostly unquantified claims

### Complexity Levels

- **"novel"**: Multiple complexity indicators (score ≥ 0.65)
- **"routine"**: Standard practices (score < 0.65)

### Proficiency Levels

- **"expert"**: 85-100 confidence
- **"advanced"**: 70-84 confidence
- **"intermediate"**: 55-69 confidence
- **"novice"**: Below 55 confidence

---

## Output Field Reference

### SkillConfidenceScore Fields

- `skill_name`: Name of the skill
- `confidence_score`: 0-100 trust metric
- `proficiency_level`: "novice"|"intermediate"|"advanced"|"expert"
- `evidence_projects`: Number of projects demonstrating skill
- `components`: Breakdown of how score was calculated
- `summary`: Human-readable summary

### ProofCard Fields

- `opportunity_title`: Job title
- `required_skills`: Skills from opportunity posting
- `matched_skills`: Top 3-5 most relevant candidate skills
- `total_relevance_score`: Average match quality (0-100)
- `summary`: "Strong match: [skills] ([score]/100 avg)"

### SkillGraph Fields

- `nodes`: List of SkillNode objects (skill metadata)
- `edges`: List of SkillEdge objects (skill-project links)
- `stats`: Graph statistics (total skills, average confidence, top skills)

---

For more details, see AGENT_4_DOCUMENTATION.md
