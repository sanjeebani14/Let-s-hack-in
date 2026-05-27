"""
Skill Confidence Score Generator

Aggregates metrics from ownership depth, outcome clarity, and problem complexity.
Computes a mathematical Skill Confidence Score normalized from 0 to 100 per identified technical skill.
"""

import re
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from .ownership import OwnershipAnalysis
from .outcome_scorer import OutcomeClarityScore
from .complexity import ComplexityRating


class SkillConfidenceComponent(BaseModel):
    """Single component contributing to skill confidence score."""
    component_name: str = Field(
        ...,
        description="Name of the scoring component",
        examples=["ownership", "outcome_clarity", "complexity", "frequency"]
    )
    score: float = Field(
        ...,
        description="Score for this component (0-1)",
        ge=0.0,
        le=1.0
    )
    weight: float = Field(
        ...,
        description="Weight applied to this component (0-1)",
        ge=0.0,
        le=1.0
    )
    weighted_contribution: float = Field(
        ...,
        description="Score × Weight contribution"
    )


class SkillConfidenceScore(BaseModel):
    """Comprehensive skill confidence score."""
    skill_name: str = Field(
        ...,
        description="Name of the technical skill being scored",
        examples=["Python", "Kubernetes", "System Design", "React"]
    )
    confidence_score: float = Field(
        ...,
        description="Overall confidence score (0-100)",
        ge=0.0,
        le=100.0
    )
    evidence_projects: int = Field(
        ...,
        description="Number of projects providing evidence for this skill"
    )
    components: List[SkillConfidenceComponent] = Field(
        default_factory=list,
        description="Breakdown of scoring components"
    )
    proficiency_level: str = Field(
        ...,
        description="Categorization of proficiency",
        examples=["novice", "intermediate", "advanced", "expert"]
    )
    summary: str = Field(
        ...,
        description="One-line summary of skill confidence"
    )


# Technical skill detection patterns
SKILL_PATTERNS = {
    "Python": r"\bpython\b|\bpy\b",
    "JavaScript": r"\bjavascript\b|\bjs\b|\bnode\.?js\b",
    "TypeScript": r"\btypescript\b|\bts\b",
    "React": r"\breact\b|\breactjs\b",
    "Vue": r"\bvue\b|\.vue",
    "Angular": r"\bangular\b",
    "FastAPI": r"\bfastapi\b",
    "Django": r"\bdjango\b",
    "Flask": r"\bflask\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "Docker": r"\bdocker\b",
    "PostgreSQL": r"\bpostgresql\b|\bpostgres\b",
    "MongoDB": r"\bmongodb\b",
    "Redis": r"\bredis\b",
    "AWS": r"\baws\b|amazon\s+web\s+services",
    "GCP": r"\bgcp\b|google\s+cloud",
    "Azure": r"\bazure\b|microsoft\s+azure",
    "System Design": r"\bsystem\s+design\b|\barchitecture\b|\bscalability\b",
    "Machine Learning": r"\bmachine\s+learning\b|\bml\b|\bai\b",
    "Data Science": r"\bdata\s+science\b|\bdata\s+analysis\b",
    "SQL": r"\bsql\b|sqlalchemy",
    "REST API": r"\brest\b|\bapi\b",
    "GraphQL": r"\bgraphql\b",
    "WebSocket": r"\bwebsocket\b",
    "Testing": r"\bunittest\b|\bpytest\b|\bjest\b|\bmocha\b|testing",
    "CI/CD": r"\bci/cd\b|\bcontinuous\s+(?:integration|deployment)\b",
}


def extract_skills_from_text(text: str, num_to_extract: int = 5) -> List[str]:
    """
    Extract technical skills mentioned in text.
    
    Args:
        text: Project narrative text
        num_to_extract: Maximum number of skills to extract
        
    Returns:
        List of identified skill names
    """
    identified_skills = []
    
    for skill_name, pattern in SKILL_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            identified_skills.append(skill_name)
            if len(identified_skills) >= num_to_extract:
                break
    
    return identified_skills[:num_to_extract]


def calculate_confidence_score(
    skill_name: str,
    ownership_analysis: OwnershipAnalysis,
    outcome_clarity: OutcomeClarityScore,
    complexity_rating: ComplexityRating,
    project_count: int = 1,
    skill_frequency: float = 1.0
) -> SkillConfidenceScore:
    """
    Calculate comprehensive skill confidence score.
    
    Aggregates ownership depth, outcome clarity, and problem complexity
    into a single 0-100 confidence metric.
    
    Formula:
        confidence = (
            ownership_score × 0.35 +
            outcome_clarity × 0.30 +
            complexity_score × 0.20 +
            frequency_bonus × 0.15
        ) × 100
    
    Args:
        skill_name: Name of the skill being scored
        ownership_analysis: Ownership depth assessment
        outcome_clarity: Outcome clarity metrics
        complexity_rating: Complexity assessment
        project_count: Number of projects providing evidence
        skill_frequency: How often skill appears in portfolio (0-1)
        
    Returns:
        SkillConfidenceScore: Comprehensive confidence score (0-100)
    """
    
    # Convert component scores to 0-1 range
    
    # Ownership component: higher confidence if "led" vs "assisted"
    ownership_base_score = ownership_analysis.action_verb_score
    ownership_multiplier = 1.0
    if ownership_analysis.ownership_level == "led":
        ownership_multiplier = 1.15
    elif ownership_analysis.ownership_level == "assisted":
        ownership_multiplier = 0.75
    
    ownership_score = min(1.0, ownership_base_score * ownership_multiplier)
    
    # Outcome clarity component
    outcome_score = outcome_clarity.clarity_score
    
    # Complexity component: higher score for novel problems
    complexity_score = complexity_rating.complexity_score
    
    # Frequency bonus: penalize if skill appears infrequently
    frequency_score = min(1.0, skill_frequency * 1.2)
    
    # Project count bonus: more projects = higher confidence
    project_bonus = min(0.15, (project_count - 1) * 0.08)
    
    # Calculate weighted score
    raw_score = (
        (ownership_score * 0.35) +
        (outcome_score * 0.30) +
        (complexity_score * 0.20) +
        (frequency_score * 0.15)
    ) + project_bonus
    
    confidence_score = min(100.0, raw_score * 100)
    
    # Determine proficiency level
    if confidence_score >= 85:
        proficiency_level = "expert"
    elif confidence_score >= 70:
        proficiency_level = "advanced"
    elif confidence_score >= 55:
        proficiency_level = "intermediate"
    else:
        proficiency_level = "novice"
    
    # Build components breakdown
    components = [
        SkillConfidenceComponent(
            component_name="ownership",
            score=ownership_score,
            weight=0.35,
            weighted_contribution=ownership_score * 0.35
        ),
        SkillConfidenceComponent(
            component_name="outcome_clarity",
            score=outcome_score,
            weight=0.30,
            weighted_contribution=outcome_score * 0.30
        ),
        SkillConfidenceComponent(
            component_name="complexity",
            score=complexity_score,
            weight=0.20,
            weighted_contribution=complexity_score * 0.20
        ),
        SkillConfidenceComponent(
            component_name="frequency",
            score=frequency_score,
            weight=0.15,
            weighted_contribution=frequency_score * 0.15
        ),
    ]
    
    # Generate summary
    summary = f"{proficiency_level.capitalize()}: {confidence_score:.0f}/100 - {ownership_analysis.ownership_level} with {'measurable' if outcome_clarity.is_specific else 'moderate'} outcomes"
    
    return SkillConfidenceScore(
        skill_name=skill_name,
        confidence_score=confidence_score,
        evidence_projects=project_count,
        components=components,
        proficiency_level=proficiency_level,
        summary=summary
    )
