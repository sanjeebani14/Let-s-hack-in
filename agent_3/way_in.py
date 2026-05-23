"""
"Your Way In" Generator

Inspects all 4 signals from the chemistry checks, extracts the single highest-value
human bridge, and generates exactly one specific, highly actionable sentence.

Example: "Their backend lead attended the same hackathon you did last month — that's your way in."
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class WayInStrategy(BaseModel):
    """Highly actionable entry strategy based on chemistry signals."""
    actionable_sentence: str = Field(
        ...,
        description="Single specific, actionable sentence describing the best way in",
        examples=[
            "Their backend lead attended the same hackathon you did last month — that's your way in.",
            "You both contributed to the PyTorch optimization repo — use that as your conversation starter.",
            "Sarah Chen, their CTO, was your mentor at AI Bootcamp — ask her for an intro."
        ]
    )
    primary_signal: str = Field(
        ...,
        description="Which signal is strongest: 'shared_context', 'engagement', 'connector', 'team_fit'",
        examples=["connector", "shared_context", "engagement"]
    )
    confidence: float = Field(
        ...,
        description="How confident this strategy is (0.0-1.0)",
        ge=0.0,
        le=1.0
    )


def generate_way_in(
    candidate_profile: Dict[str, Any],
    opportunity_data: Dict[str, Any],
    context_detector_response: Any,
    connector_response: Any,
    engagement_response: Any,
    team_analysis_response: Any,
    inroad_score_response: Any
) -> WayInStrategy:
    """
    Generate the single most actionable entry strategy.
    
    Inspects all 4 signals and extracts the highest-value human bridge,
    then creates one specific, actionable sentence.
    
    Args:
        candidate_profile: Extracted candidate profile
        opportunity_data: Full opportunity data
        context_detector_response: Shared contexts
        connector_response: Connector findings
        engagement_response: Employee engagement signals
        team_analysis_response: Team composition fit
        inroad_score_response: Final InRoad score
        
    Returns:
        WayInStrategy: Actionable entry sentence + confidence
    """
    
    strategy_signals = []
    
    # Signal 1: Best Connector (highest confidence human bridge)
    best_connector = None
    connector_confidence = 0.0
    try:
        if hasattr(connector_response, 'best_connector'):
            best_connector = connector_response.best_connector
            connector_confidence = best_connector.introduction_likelihood
            if best_connector.person_name != "No direct connectors found":
                strategy_signals.append({
                    "type": "connector",
                    "confidence": connector_confidence,
                    "value": best_connector,
                    "sentence": (
                        f"Ask {best_connector.person_name} — {best_connector.relationship_to_candidate} — "
                        f"to introduce you. They're {best_connector.relationship_to_company.lower()}."
                    )
                })
    except:
        pass
    
    # Signal 2: Shared Context (hackathons, communities, open-source)
    shared_context_confidence = 0.0
    try:
        if hasattr(context_detector_response, 'shared_contexts') and context_detector_response.shared_contexts:
            best_context = max(
                context_detector_response.shared_contexts,
                key=lambda x: x.relevance_score
            )
            shared_context_confidence = best_context.relevance_score
            strategy_signals.append({
                "type": "shared_context",
                "confidence": shared_context_confidence,
                "value": best_context,
                "sentence": (
                    f"You both participated in {best_context.name} — "
                    f"bring that up as your conversation starter when you reach out."
                )
            })
    except:
        pass
    
    # Signal 3: Employee Engagement (GitHub stars, article likes, etc.)
    engagement_confidence = 0.0
    try:
        if hasattr(engagement_response, 'interactions') and engagement_response.interactions:
            best_interaction = engagement_response.interactions[0]
            engagement_confidence = min(0.9, len(engagement_response.interactions) * 0.3)
            strategy_signals.append({
                "type": "engagement",
                "confidence": engagement_confidence,
                "value": best_interaction,
                "sentence": (
                    f"{best_interaction.person_name}, their {best_interaction.person_role.lower()}, "
                    f"already {best_interaction.interaction_detail.lower()} — "
                    f"they know your work, so mention this in your outreach."
                )
            })
    except:
        pass
    
    # Signal 4: Team Fit (if very strong, can be a strategy)
    team_fit_confidence = 0.0
    try:
        if hasattr(team_analysis_response, 'fit_category') and hasattr(team_analysis_response, 'chemistry_score'):
            if team_analysis_response.chemistry_score >= 0.75:
                team_fit_confidence = team_analysis_response.chemistry_score
                strategy_signals.append({
                    "type": "team_fit",
                    "confidence": team_fit_confidence,
                    "value": team_analysis_response,
                    "sentence": (
                        f"You {team_analysis_response.fit_category.value} their team culture perfectly — "
                        f"emphasize how your working style aligns with theirs."
                    )
                })
    except:
        pass
    
    # Select the highest-confidence signal
    if strategy_signals:
        best_signal = max(strategy_signals, key=lambda x: x["confidence"])
        primary_signal = best_signal["type"]
        actionable_sentence = best_signal["sentence"]
        confidence = best_signal["confidence"]
    else:
        # Fallback strategy if no strong signals
        company_name = opportunity_data.get("company", "the company")
        primary_signal = "generic"
        actionable_sentence = (
            f"Research people at {company_name} on LinkedIn, find 2-3 people whose work aligns with yours, "
            f"and send personalized messages mentioning specific projects of theirs you admire."
        )
        confidence = 0.4
    
    # Ensure confidence is 0-1
    confidence = max(0.0, min(1.0, confidence))
    
    return WayInStrategy(
        actionable_sentence=actionable_sentence,
        primary_signal=primary_signal,
        confidence=confidence
    )
