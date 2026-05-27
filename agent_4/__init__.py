"""
Agent 4 — Skill Proof Agent

Parses portfolio descriptions, calculates algorithmic trust scores for claimed
technical competencies, and builds data maps for frontend visualization.

Components:
  - parser: Breaks project narratives into structured components
  - ownership: Detects ownership depth and role classification
  - outcome_scorer: Evaluates outcome clarity and metrics
  - complexity: Assesses problem complexity
  - confidence: Generates comprehensive skill confidence scores
  - graph_builder: Constructs skill graph for visualization
  - proof_card: Generates targeted proof cards for opportunities
"""

# Parser exports
from .parser import (
    ProjectNarrative,
    parse_project_narrative,
)

# Ownership exports
from .ownership import (
    OwnershipAnalysis,
    detect_ownership_level,
)

# Outcome scorer exports
from .outcome_scorer import (
    OutcomeMeasure,
    OutcomeClarityScore,
    score_outcome_clarity,
)

# Complexity exports
from .complexity import (
    ComplexityIndicator,
    ComplexityRating,
    evaluate_complexity,
)

# Confidence exports
from .confidence import (
    SkillConfidenceComponent,
    SkillConfidenceScore,
    extract_skills_from_text,
    calculate_confidence_score,
)

# Graph builder exports
from .graph_builder import (
    SkillNode,
    SkillEdge,
    SkillGraph,
    build_skill_graph,
    graph_to_dict,
    normalize_skill_id,
)

# Proof card exports
from .proof_card import (
    ProofCardSkill,
    ProofCard,
    generate_proof_card,
    proof_card_to_dict,
)

__all__ = [
    # Parser
    "ProjectNarrative",
    "parse_project_narrative",
    # Ownership
    "OwnershipAnalysis",
    "detect_ownership_level",
    # Outcome Scorer
    "OutcomeMeasure",
    "OutcomeClarityScore",
    "score_outcome_clarity",
    # Complexity
    "ComplexityIndicator",
    "ComplexityRating",
    "evaluate_complexity",
    # Confidence
    "SkillConfidenceComponent",
    "SkillConfidenceScore",
    "extract_skills_from_text",
    "calculate_confidence_score",
    # Graph Builder
    "SkillNode",
    "SkillEdge",
    "SkillGraph",
    "build_skill_graph",
    "graph_to_dict",
    "normalize_skill_id",
    # Proof Card
    "ProofCardSkill",
    "ProofCard",
    "generate_proof_card",
    "proof_card_to_dict",
]
