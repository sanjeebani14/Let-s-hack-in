"""
InRoad Score Calculator

Formulates a combined quantitative mathematical score combining:
  - Role Fit % (from Member A's matching)
  - Team Overlap % (from Shared Context Detector)
  - Entry Probability % (from Connector Finder + Engagement Signals)
  - Competition Index (from Member B's scoring)

Outputs final score + one-line structural explanation.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class InRoadScore(BaseModel):
    """Final InRoad Chemistry score and breakdown."""
    role_fit_percentage: float = Field(
        ...,
        description="Role fit score from Member A (0-100)",
        ge=0.0,
        le=100.0
    )
    team_overlap_percentage: float = Field(
        ...,
        description="Shared context overlap score (0-100)",
        ge=0.0,
        le=100.0
    )
    entry_probability_percentage: float = Field(
        ...,
        description="Probability of getting intro via connectors/engagement (0-100)",
        ge=0.0,
        le=100.0
    )
    competition_index: float = Field(
        ...,
        description="How hidden/uncompetitive the opportunity is (0-1)",
        ge=0.0,
        le=1.0
    )
    inroad_score: float = Field(
        ...,
        description="Final combined InRoad Chemistry score (0-100)",
        ge=0.0,
        le=100.0
    )
    structural_explanation: str = Field(
        ...,
        description="One-line plain English explanation of the score",
        examples=["Strong role fit + existing network bridge = highest priority opportunity"]
    )


def calculate_inroad_score(
    role_fit_score: float,
    context_detector_response: Any,
    connector_response: Any,
    engagement_response: Any,
    competition_index: float,
    opportunity_data: Dict[str, Any]
) -> InRoadScore:
    """
    Calculate combined InRoad Chemistry score.
    
    Formula:
        inroad_score = (
            role_fit_pct × 0.40 +           # How well skills match
            team_overlap_pct × 0.20 +       # Shared contexts/communities
            entry_probability_pct × 0.30 +  # Can you get introduced?
            (competition_index × 100) × 0.10 # Hidden opportunity bonus
        )
    
    Args:
        role_fit_score: Fit score from Member A matching (0-100)
        context_detector_response: SharedContext detection results
        connector_response: Connector finding results
        engagement_response: Engagement signal results
        competition_index: Hidden opportunity score from Member B (0-1)
        opportunity_data: Full opportunity data
        
    Returns:
        InRoadScore: Final score with breakdown and explanation
    """
    
    # Extract percentages
    role_fit_pct = role_fit_score  # Already 0-100
    
    # Convert team overlap score (0-1) to percentage
    team_overlap_pct = (
        context_detector_response.total_overlap_score * 100
        if hasattr(context_detector_response, 'total_overlap_score')
        else 40.0  # Default if structure differs
    )
    
    # Calculate entry probability from connectors + engagement
    connector_pct = (
        connector_response.entry_probability * 100
        if hasattr(connector_response, 'entry_probability')
        else 0.0
    )
    engagement_pct = (
        engagement_response.engagement_strength * 100
        if hasattr(engagement_response, 'engagement_strength')
        else 0.0
    )
    
    # Average connector and engagement for entry probability
    entry_probability_pct = (connector_pct + engagement_pct) / 2
    
    # Competition index bonus (0-100)
    competition_bonus_pct = competition_index * 100
    
    # Apply weighted formula
    inroad_score = (
        role_fit_pct * 0.40 +
        team_overlap_pct * 0.20 +
        entry_probability_pct * 0.30 +
        competition_bonus_pct * 0.10
    )
    
    # Ensure score is capped at 100 and minimum 0
    inroad_score = max(0.0, min(100.0, inroad_score))
    
    # Generate structural explanation
    best_connector = None
    try:
        best_connector = connector_response.best_connector
    except:
        best_connector = None
    
    # Build explanation based on which factors are strongest
    strongest_factors = []
    
    if role_fit_pct >= 75:
        strongest_factors.append("excellent role fit")
    elif role_fit_pct >= 50:
        strongest_factors.append("solid role alignment")
    
    if team_overlap_pct >= 60:
        strongest_factors.append("shared communities")
    
    if entry_probability_pct >= 65:
        if best_connector:
            strongest_factors.append(f"direct path via {best_connector.person_name}")
        else:
            strongest_factors.append("strong entry pathways")
    
    if competition_bonus_pct >= 70:
        strongest_factors.append("hidden opportunity")
    
    if strongest_factors:
        explanation = (
            f"{strongest_factors[0].capitalize()} + "
            f"{' + '.join(strongest_factors[1:])} = "
            f"{'top priority' if inroad_score >= 80 else 'promising'} opportunity"
        )
    else:
        explanation = "Weaker signals overall, but possible entry point exists"
    
    return InRoadScore(
        role_fit_percentage=role_fit_pct,
        team_overlap_percentage=team_overlap_pct,
        entry_probability_percentage=entry_probability_pct,
        competition_index=competition_index,
        inroad_score=inroad_score,
        structural_explanation=explanation
    )
