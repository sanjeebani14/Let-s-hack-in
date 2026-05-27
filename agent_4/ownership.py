"""
Ownership Depth Detector

Analyzes narrative text patterns for strong action verbs vs. passive language.
Classifies the candidate's role into categorical values: "led", "contributed", or "assisted".
Flags an is_vague boolean if ownership indicators are low.
"""

import re
from pydantic import BaseModel, Field
from typing import Literal, Dict, List


class OwnershipAnalysis(BaseModel):
    """Analysis of candidate ownership depth in a project."""
    ownership_level: Literal["led", "contributed", "assisted"] = Field(
        ...,
        description="Categorical ownership classification"
    )
    is_vague: bool = Field(
        ...,
        description="True if ownership indicators are weak or unclear"
    )
    action_verb_score: float = Field(
        ...,
        description="Strength of action verbs in narrative (0-1)",
        ge=0.0,
        le=1.0
    )
    evidence: str = Field(
        ...,
        description="Key phrase supporting the ownership classification"
    )
    confidence: float = Field(
        ...,
        description="Confidence in this classification (0-1)",
        ge=0.0,
        le=1.0
    )


# Strong action verbs indicating high ownership
STRONG_ACTION_VERBS = {
    "led": 0.95, "spearheaded": 0.95, "founded": 0.95, "architect": 0.90,
    "engineered": 0.90, "directed": 0.90, "owned": 0.90, "owned": 0.90,
    "designed": 0.85, "built": 0.85, "created": 0.85, "developed": 0.85,
    "implemented": 0.80, "drove": 0.80, "executed": 0.80, "launched": 0.80,
    "shipped": 0.80, "managed": 0.80, "oversaw": 0.85, "orchestrated": 0.85
}

# Medium action verbs indicating contribution
MEDIUM_ACTION_VERBS = {
    "contributed": 0.70, "helped": 0.65, "assisted": 0.60, "supported": 0.65,
    "worked on": 0.70, "collaborated": 0.70, "partnered": 0.70, "participated": 0.65,
    "involved in": 0.60, "part of": 0.55, "responsible for": 0.75,
    "took on": 0.70, "handled": 0.70, "tackled": 0.75
}

# Weak verbs or passive language indicating low ownership
WEAK_ACTION_VERBS = {
    "used": 0.40, "reviewed": 0.40, "observed": 0.30, "witnessed": 0.25,
    "followed": 0.35, "assigned to": 0.35, "given": 0.30, "told to": 0.25,
    "was": 0.20, "involved": 0.45, "attended": 0.25, "trained": 0.35,
    "learned": 0.40, "was asked": 0.25, "was told": 0.20, "fixed": 0.55
}

# Vague language patterns
VAGUE_PATTERNS = [
    r"somewhat|kind of|sort of|like|maybe|might",
    r"helped with|was part of|was involved",
    r"the team (did|built|created|solved)",
    r"(we|our team) (did|built|created)",
    r"among other things|as well as|also did"
]


def extract_key_phrase(text: str, candidate_role_text: str = "") -> str:
    """Extract the most relevant action phrase from text."""
    # Combine texts for better extraction
    full_text = candidate_role_text + " " + text
    
    # Look for verb phrases
    verb_patterns = [
        r"(led|spearheaded|architected|engineered|designed|built|created|developed|implemented|drove|managed|owned|directed|oversaw)\s+(?:the\s+)?([\w\s]+?)(?:\s+(?:by|to|with|for|in|at)|\s*\.|\s*,|$)",
        r"(responsible\s+for|owner\s+of|drove|took\s+on)\s+([\w\s]+?)(?:\s+(?:by|to|with|for|in|at)|\s*\.|\s*,|$)"
    ]
    
    for pattern in verb_patterns:
        matches = re.finditer(pattern, full_text, re.IGNORECASE)
        for match in matches:
            return match.group(0).strip()
    
    # Return first sentence as fallback
    sentences = full_text.split('.')
    return sentences[0].strip() if sentences else "Unspecified role"


def detect_ownership_level(
    project_narrative_text: str,
    candidate_role_text: str = ""
) -> OwnershipAnalysis:
    """
    Analyze ownership depth from narrative patterns.
    
    Detects strong vs. passive language, counts action verbs, and classifies
    into one of three levels: "led", "contributed", "assisted".
    
    Args:
        project_narrative_text: Full project description
        candidate_role_text: Specific mention of candidate's role
        
    Returns:
        OwnershipAnalysis: Ownership classification with evidence
    """
    
    combined_text = project_narrative_text + " " + candidate_role_text
    lower_text = combined_text.lower()
    
    # Score based on action verb presence
    strong_verb_count = sum(
        lower_text.count(verb) for verb in STRONG_ACTION_VERBS
    )
    medium_verb_count = sum(
        lower_text.count(verb) for verb in MEDIUM_ACTION_VERBS
    )
    weak_verb_count = sum(
        lower_text.count(verb) for verb in WEAK_ACTION_VERBS
    )
    
    # Calculate weighted action verb score
    total_verbs = strong_verb_count + medium_verb_count + weak_verb_count
    
    if total_verbs == 0:
        action_verb_score = 0.3
        verb_weight = 0.0
    else:
        verb_weight = (
            (strong_verb_count * 0.95) +
            (medium_verb_count * 0.65) +
            (weak_verb_count * 0.30)
        ) / total_verbs
    
    # Check for vague patterns
    vague_count = sum(
        len(re.findall(pattern, lower_text, re.IGNORECASE))
        for pattern in VAGUE_PATTERNS
    )
    is_vague = vague_count > 2 or verb_weight < 0.45
    
    # Determine ownership level
    if verb_weight >= 0.75 and strong_verb_count > 0 and not is_vague:
        ownership_level = "led"
        confidence = min(0.95, 0.6 + (verb_weight * 0.4))
    elif verb_weight >= 0.50 and medium_verb_count > 0:
        ownership_level = "contributed"
        confidence = min(0.90, 0.5 + (verb_weight * 0.35))
    else:
        ownership_level = "assisted"
        confidence = min(0.85, 0.4 + (verb_weight * 0.3))
    
    # Extract evidence phrase
    evidence = extract_key_phrase(project_narrative_text, candidate_role_text)
    
    return OwnershipAnalysis(
        ownership_level=ownership_level,
        is_vague=is_vague,
        action_verb_score=min(1.0, verb_weight),
        evidence=evidence,
        confidence=confidence
    )
