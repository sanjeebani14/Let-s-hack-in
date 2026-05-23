"""
Member B - Opportunity Scorer & Ranker
Evaluates opportunities on 4 signals and ranks them for candidate matching.
"""

from typing import List, Dict, Any
from datetime import datetime


def score_opportunity(opportunity: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scores a single opportunity on 4 algorithmic signals.
    
    Signals (each 0.0 to 1.0):
    - competition_index: How hidden is it? GitHub repos/founder posts = higher (less competition)
    - response_probability: Likelihood of reply based on source and stage
    - growth_potential: Career acceleration value
    - referral_likelihood: Probability of securing warm intro
    
    Args:
        opportunity: Dictionary containing opportunity details
        
    Returns:
        Dictionary with opportunity enriched with scoring metrics
    """
    
    # Extract features for scoring
    source_type = opportunity.get("source_type", "").lower()
    stage = opportunity.get("stage", "").lower()
    team_size = opportunity.get("team_size", 5)
    
    # ============================================
    # Signal 1: Competition Index (Hidden-ness)
    # Higher = more hidden/less competitive
    # ============================================
    competition_scores = {
        "founder_post": 0.85,        # Directly from founder - very hidden
        "github_repo": 0.80,         # Niche discovery - hidden
        "employee_post": 0.70,       # Internal referral channel - moderately hidden
        "newsletter": 0.65,          # Newsletter subscribers only - semi-hidden
        "hackathon": 0.75,           # Event-based - fairly hidden
        "job_board": 0.30,           # Public boards - highly competitive
        "linkedin": 0.40             # LinkedIn - very visible
    }
    competition_index = competition_scores.get(source_type, 0.50)
    
    # ============================================
    # Signal 2: Response Probability
    # Likelihood of getting a reply based on source + stage
    # ============================================
    stage_response_boost = {
        "seed": 0.80,           # Founders are hungry, responsive
        "series_a": 0.70,       # Growing, still personal
        "series_b": 0.60,       # Larger hiring process, less personal
        "series_c": 0.50,       # Very formal hiring
        "public": 0.45,         # Large company, formal HR
        "bootstrapped": 0.75,   # Founder-led, responsive
        "non_profit": 0.65      # Mission-driven, responsive
    }
    base_response = stage_response_boost.get(stage, 0.55)
    
    # Source type modifier for response
    source_response_modifier = {
        "founder_post": 0.95,      # Direct, personal channel
        "employee_post": 0.85,     # Referral = warm
        "newsletter": 0.75,        # Curated audience
        "github_repo": 0.70,       # Shows genuine interest
        "hackathon": 0.80,         # Event context builds rapport
        "job_board": 0.50,
        "linkedin": 0.60
    }
    modifier = source_response_modifier.get(source_type, 0.60)
    response_probability = min(base_response * (modifier / 0.70), 1.0)  # Cap at 1.0
    
    # ============================================
    # Signal 3: Growth Potential
    # Career acceleration based on stage and team size
    # ============================================
    stage_growth = {
        "seed": 0.90,           # Highest growth, high responsibility
        "series_a": 0.80,       # Strong growth trajectory
        "series_b": 0.70,       # Established, but good learning
        "series_c": 0.60,       # Stable, slower growth
        "public": 0.50,         # Mature company
        "bootstrapped": 0.85,   # Founder-level responsibility
        "non_profit": 0.65      # Meaningful work, variable growth
    }
    base_growth = stage_growth.get(stage, 0.60)
    
    # Small teams = more responsibility = higher growth
    team_growth_boost = max(1.0 - (team_size / 50), 0.1)  # Smaller teams boost growth
    growth_potential = min(base_growth * 1.1 * team_growth_boost, 1.0)
    
    # ============================================
    # Signal 4: Referral Likelihood
    # Probability of securing a warm intro
    # ============================================
    referral_sources = {
        "employee_post": 0.85,     # Someone already inside = easy intro
        "founder_post": 0.70,      # Can ask mutual connections
        "newsletter": 0.50,        # Possible through newsletter community
        "hackathon": 0.80,         # Event connections
        "github_repo": 0.60,       # Can reference contributions
        "job_board": 0.25,         # No warm context
        "linkedin": 0.40
    }
    referral_likelihood = referral_sources.get(source_type, 0.35)
    
    # ============================================
    # Calculate Final Opportunity Score
    # ============================================
    # Weighted average (all signals equally important for now)
    opportunity_score = (
        competition_index * 0.25 +
        response_probability * 0.25 +
        growth_potential * 0.25 +
        referral_likelihood * 0.25
    )
    opportunity_score = round(opportunity_score, 3)
    
    # ============================================
    # Generate One-Line Reasoning
    # ============================================
    reasoning_components = []
    
    if competition_index > 0.75:
        reasoning_components.append("highly hidden opportunity")
    elif competition_index > 0.60:
        reasoning_components.append("semi-hidden channel")
    else:
        reasoning_components.append("competitive posting")
    
    if stage == "seed":
        reasoning_components.append("strong growth potential")
    elif stage in ["series_a", "bootstrapped"]:
        reasoning_components.append("solid growth trajectory")
    
    if response_probability > 0.75:
        reasoning_components.append("high response likelihood")
    
    score_reasoning = f"This is a {', '.join(reasoning_components)} with a strong fit profile for ambitious engineers."
    
    # Return enriched opportunity
    return {
        **opportunity,
        "competition_index": round(competition_index, 3),
        "response_probability": round(response_probability, 3),
        "growth_potential": round(growth_potential, 3),
        "referral_likelihood": round(referral_likelihood, 3),
        "opportunity_score": opportunity_score,
        "score_reasoning": score_reasoning
    }


def rank_opportunities(opportunities: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Scores all opportunities and returns only the top K ranked by opportunity_score.
    
    Args:
        opportunities: List of opportunity dictionaries
        top_k: Number of top opportunities to return (default: 3)
        
    Returns:
        List of top K opportunities sorted by opportunity_score (descending)
    """
    
    # Score all opportunities
    scored_opportunities = [score_opportunity(opp) for opp in opportunities]
    
    # Sort by opportunity_score descending
    ranked = sorted(
        scored_opportunities,
        key=lambda x: x["opportunity_score"],
        reverse=True
    )
    
    # Return only top K
    return ranked[:top_k]
