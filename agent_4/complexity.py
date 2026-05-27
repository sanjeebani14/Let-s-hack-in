"""
Problem Complexity Evaluator

Scans narratives for engineering constraints, mentions of systemic failures,
architectural trade-offs, or design pivots.
Assigns categorical complexity rating: "routine" or "novel".
"""

import re
from pydantic import BaseModel, Field
from typing import Literal, List


class ComplexityIndicator(BaseModel):
    """A single indicator of problem complexity."""
    indicator_type: str = Field(
        ...,
        description="Type of complexity indicator",
        examples=["constraint", "failure", "tradeoff", "pivot", "scale", "integration"]
    )
    description: str = Field(
        ...,
        description="Description of the complexity aspect"
    )
    weight: float = Field(
        ...,
        description="Weight of this indicator (0-1)",
        ge=0.0,
        le=1.0
    )


class ComplexityRating(BaseModel):
    """Assessment of problem complexity."""
    complexity_level: Literal["routine", "novel"] = Field(
        ...,
        description="Whether the problem was routine or novel/challenging"
    )
    complexity_score: float = Field(
        ...,
        description="Numerical complexity score (0-1): 0=trivial, 1=highly complex",
        ge=0.0,
        le=1.0
    )
    indicators_found: List[ComplexityIndicator] = Field(
        default_factory=list,
        description="List of complexity indicators identified"
    )
    summary: str = Field(
        ...,
        description="One-line summary of complexity assessment"
    )


# Keywords indicating constraints/limitations
CONSTRAINT_KEYWORDS = [
    "constraint", "limitation", "bottleneck", "overhead", "latency",
    "throughput", "memory", "bandwidth", "cost", "concurrency",
    "distributed", "consensus", "synchronization", "deadlock",
    "race condition", "scaling", "partition", "timeout", "deadline",
    "compliance", "regulation", "legacy", "compatibility"
]

# Keywords indicating failures/problems
FAILURE_KEYWORDS = [
    "failed", "broke", "crashed", "error", "bug", "issue", "problem",
    "struggled", "difficulty", "unforeseen", "unexpected", "surprise",
    "incident", "outage", "regression", "critical", "severe",
    "catastrophic", "loss", "corruption", "breach", "security"
]

# Keywords indicating trade-offs/pivots
TRADEOFF_KEYWORDS = [
    "trade-off", "tradeoff", "compromise", "versus", "vs.",
    "choice between", "decided", "pivoted", "shifted", "redesigned",
    "refactored", "rewrite", "migration", "rewrote", "changed approach",
    "realized", "discovered", "learned that", "initially", "first tried",
    "turned out", "instead", "switched to", "abandoned"
]

# Keywords indicating scale/architectural challenges
SCALE_KEYWORDS = [
    "scale", "scalable", "millions", "billions", "petabyte", "terabyte",
    "1000s", "10000s", "concurrent users", "high availability",
    "fault tolerance", "redundancy", "replication", "sharding",
    "load balancing", "caching", "optimization", "performance"
]

# Keywords indicating novel/research-oriented work
NOVEL_KEYWORDS = [
    "novel", "innovative", "first", "pioneering", "research",
    "experimental", "cutting-edge", "new approach", "custom",
    "proprietary", "unique", "invented", "algorithm", "new pattern",
    "first time", "pioneered"
]


def find_indicators(text: str) -> List[ComplexityIndicator]:
    """
    Scan narrative for complexity indicators.
    
    Args:
        text: Project narrative text
        
    Returns:
        List of identified complexity indicators
    """
    indicators = []
    lower_text = text.lower()
    
    # Check constraints
    constraint_count = sum(
        lower_text.count(keyword) for keyword in CONSTRAINT_KEYWORDS
    )
    if constraint_count > 0:
        indicators.append(ComplexityIndicator(
            indicator_type="constraint",
            description=f"Found {constraint_count} mentions of system constraints/limitations",
            weight=min(0.9, 0.4 + (constraint_count * 0.15))
        ))
    
    # Check failures/problems
    failure_count = sum(
        lower_text.count(keyword) for keyword in FAILURE_KEYWORDS
    )
    if failure_count > 0:
        indicators.append(ComplexityIndicator(
            indicator_type="failure",
            description=f"Found {failure_count} references to problems/failures encountered",
            weight=min(0.95, 0.5 + (failure_count * 0.15))
        ))
    
    # Check trade-offs/pivots
    tradeoff_count = sum(
        lower_text.count(keyword) for keyword in TRADEOFF_KEYWORDS
    )
    if tradeoff_count > 0:
        indicators.append(ComplexityIndicator(
            indicator_type="tradeoff",
            description=f"Found {tradeoff_count} mentions of design trade-offs or pivots",
            weight=min(0.9, 0.45 + (tradeoff_count * 0.15))
        ))
    
    # Check scale/architectural challenges
    scale_count = sum(
        lower_text.count(keyword) for keyword in SCALE_KEYWORDS
    )
    if scale_count > 0:
        indicators.append(ComplexityIndicator(
            indicator_type="scale",
            description=f"Found {scale_count} references to scaling or architectural challenges",
            weight=min(0.85, 0.4 + (scale_count * 0.12))
        ))
    
    # Check novel/innovative work
    novel_count = sum(
        lower_text.count(keyword) for keyword in NOVEL_KEYWORDS
    )
    if novel_count > 0:
        indicators.append(ComplexityIndicator(
            indicator_type="novel",
            description=f"Found {novel_count} mentions of innovative or novel approaches",
            weight=min(0.85, 0.5 + (novel_count * 0.12))
        ))
    
    return indicators


def evaluate_complexity(
    project_narrative_text: str,
    challenges_faced_list: List[str] = None,
    outcome_text: str = ""
) -> ComplexityRating:
    """
    Evaluate problem complexity from narrative patterns.
    
    Scans for engineering constraints, systemic failures, architectural
    trade-offs, and design pivots. Assigns "routine" or "novel" classification.
    
    Args:
        project_narrative_text: Full project description
        challenges_faced_list: List of challenges previously extracted
        outcome_text: Outcome/results statement
        
    Returns:
        ComplexityRating: Complexity assessment with indicators
    """
    
    # Combine all available text
    combined_text = project_narrative_text
    if challenges_faced_list:
        combined_text += " " + " ".join(challenges_faced_list)
    if outcome_text:
        combined_text += " " + outcome_text
    
    # Find complexity indicators
    indicators = find_indicators(combined_text)
    
    # Calculate complexity score
    if not indicators:
        complexity_score = 0.25  # Assumed routine if no indicators
    else:
        # Average weights of indicators
        avg_weight = sum(ind.weight for ind in indicators) / len(indicators)
        
        # Bonus for multiple indicator types (suggests multifaceted complexity)
        type_diversity = len(set(ind.indicator_type for ind in indicators))
        if type_diversity >= 3:
            avg_weight = min(1.0, avg_weight + 0.15)
        elif type_diversity == 2:
            avg_weight = min(1.0, avg_weight + 0.08)
        
        complexity_score = avg_weight
    
    # Determine complexity level
    if complexity_score >= 0.65:
        complexity_level = "novel"
    else:
        complexity_level = "routine"
    
    # Generate summary
    indicator_summary = ", ".join([ind.indicator_type for ind in indicators])
    if not indicator_summary:
        summary = "Routine project with standard engineering practices"
    else:
        summary = f"Novel complexity: {indicator_summary}"
    
    return ComplexityRating(
        complexity_level=complexity_level,
        complexity_score=min(1.0, complexity_score),
        indicators_found=indicators,
        summary=summary
    )
