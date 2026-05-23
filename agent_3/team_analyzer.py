"""
Team Composition Analyzer

Compares the candidate's seniority level and primary working style
against the existing target team's seniority distribution and culture.
Returns a categorical string: "complements", "neutral", or "overlaps".
"""

from pydantic import BaseModel, Field
from typing import Dict, Any
from enum import Enum


class TeamFitCategory(str, Enum):
    """Categorical assessment of how candidate fits with target team composition."""
    COMPLEMENTS = "complements"  # Different seniority/skills - fills gaps
    NEUTRAL = "neutral"           # Similar but not problematic
    OVERLAPS = "overlaps"         # Redundant seniority/role - potential conflict


class TeamCompositionAnalysis(BaseModel):
    """Analysis of team fit based on composition."""
    candidate_seniority: str = Field(
        ...,
        description="Extracted seniority level of candidate",
        examples=["Student Developer", "Junior Engineer", "Mid-Level", "Senior", "Lead"]
    )
    target_team_seniority_distribution: Dict[str, int] = Field(
        ...,
        description="Count of team members at each seniority level",
        examples=[{"senior": 2, "junior": 1, "mid_level": 1}]
    )
    candidate_working_style: str = Field(
        ...,
        description="Primary working style of candidate",
        examples=["Self-directed learner", "Team collaborator", "Mentor-focused"]
    )
    team_culture_style: str = Field(
        ...,
        description="Dominant working style in target team",
        examples=["Self-directed learner", "Team collaborator", "Mentor-focused"]
    )
    fit_category: TeamFitCategory = Field(
        ...,
        description="How candidate's seniority/style fits: complements, neutral, or overlaps"
    )
    reasoning: str = Field(
        ...,
        description="Explanation of the fit assessment"
    )
    chemistry_score: float = Field(
        ...,
        description="Cultural/working style compatibility (0.0-1.0)",
        ge=0.0,
        le=1.0
    )


def analyze_team_composition(
    candidate_profile: Dict[str, Any],
    opportunity_data: Dict[str, Any]
) -> TeamCompositionAnalysis:
    """
    Analyze team composition fit based on seniority and working style.
    
    Args:
        candidate_profile: Extracted candidate profile (from Member A)
        opportunity_data: Full opportunity data including team composition
        
    Returns:
        TeamCompositionAnalysis: Fit assessment and reasoning
    """
    
    # Extract candidate seniority
    candidate_seniority = candidate_profile.get("seniority_level", "Unknown")
    
    # Mock team compositions by company
    mock_team_compositions = {
        "NeuralFlow Startup": {
            "seniority_distribution": {"senior": 1, "mid_level": 1, "junior": 1},
            "team_culture": "Self-directed learner",
            "size": 3
        },
        "DataFlow Collective": {
            "seniority_distribution": {"senior": 2, "mid_level": 3, "junior": 3},
            "team_culture": "Team collaborator",
            "size": 8
        },
        "QuantumAI Labs": {
            "seniority_distribution": {"senior": 2, "mid_level": 2, "junior": 2},
            "team_culture": "Mentor-focused",
            "size": 6
        },
        "VisionTech Inc": {
            "seniority_distribution": {"senior": 3, "mid_level": 4, "junior": 5},
            "team_culture": "Team collaborator",
            "size": 12
        },
        "default": {
            "seniority_distribution": {"mid_level": 5},
            "team_culture": "Self-directed learner",
            "size": 5
        }
    }
    
    company_name = opportunity_data.get("company", "")
    team_info = mock_team_compositions.get(company_name, mock_team_compositions["default"])
    
    # Map candidate seniority to team context
    seniority_hierarchy = {
        "Student Developer": 1,
        "Junior Engineer": 2,
        "Mid-Level": 3,
        "Senior": 4,
        "Lead": 5,
        "CTO/VP": 6
    }
    
    candidate_level = seniority_hierarchy.get(candidate_seniority, 2)
    team_seniority_dist = team_info["seniority_distribution"]
    
    # Count seniors and juniors in target team
    senior_count = team_seniority_dist.get("senior", 0) + team_seniority_dist.get("lead", 0)
    junior_count = team_seniority_dist.get("junior", 0) + team_seniority_dist.get("student", 0)
    
    # Determine fit category
    if candidate_level <= 2:  # Student or Junior
        if junior_count >= 2:
            fit_category = TeamFitCategory.OVERLAPS
            reasoning = f"Team already has {junior_count} junior developers. Candidate would overlap in seniority level."
            chemistry_score = 0.45
        else:
            fit_category = TeamFitCategory.COMPLEMENTS
            reasoning = "Team lacks junior/growth talent. Candidate would bring fresh perspectives and growth potential."
            chemistry_score = 0.85
    elif candidate_level == 3:  # Mid-level
        fit_category = TeamFitCategory.NEUTRAL
        reasoning = "Candidate's mid-level seniority aligns well with typical team structure. Solid balance expected."
        chemistry_score = 0.70
    else:  # Senior or Lead
        if senior_count >= 2:
            fit_category = TeamFitCategory.OVERLAPS
            reasoning = f"Team already has {senior_count} senior/lead members. Potential hierarchy conflicts."
            chemistry_score = 0.55
        else:
            fit_category = TeamFitCategory.COMPLEMENTS
            reasoning = "Team would benefit from senior mentorship and architectural guidance."
            chemistry_score = 0.80
    
    # Adjust based on working style match
    candidate_style = candidate_profile.get("semantic_summary", "")
    team_culture = team_info["team_culture"]
    
    # Simple heuristic: boost score if candidate seems collaborative and team culture matches
    if "collaborative" in candidate_style.lower() and team_culture == "Team collaborator":
        chemistry_score = min(chemistry_score + 0.10, 1.0)
    elif "self-directed" in candidate_style.lower() and team_culture == "Self-directed learner":
        chemistry_score = min(chemistry_score + 0.10, 1.0)
    elif "mentor" in candidate_style.lower() and team_culture == "Mentor-focused":
        chemistry_score = min(chemistry_score + 0.10, 1.0)
    
    return TeamCompositionAnalysis(
        candidate_seniority=candidate_seniority,
        target_team_seniority_distribution=team_seniority_dist,
        candidate_working_style="Builds intelligent systems with focus on impact",
        team_culture_style=team_culture,
        fit_category=fit_category,
        reasoning=reasoning,
        chemistry_score=chemistry_score
    )
