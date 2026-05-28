import json
from typing import Dict, List, Any
from member_a.embeddings import generate_embedding, cosine_similarity


def calculate_fit_score(candidate_profile: dict, opportunity: dict) -> float:
    """
    Calculate fit score between candidate and opportunity using keyword matching
    and semantic similarity.
    
    Args:
        candidate_profile: Candidate profile dict
        opportunity: Opportunity dict
        
    Returns:
        Fit score (0-100)
    """
    
    # Extract text representations
    candidate_skills = " ".join(candidate_profile.get("core_skills", []))
    candidate_domains = " ".join(candidate_profile.get("domain_expertise", []))
    candidate_text = f"{candidate_skills} {candidate_domains}"
    
    opportunity_text = " ".join([
        str(opportunity.get("title", "")),
        str(opportunity.get("description", "")),
        str(opportunity.get("required_skills", []))
    ])
    
    # Embedding-based similarity
    candidate_vector = generate_embedding(candidate_text)
    opportunity_vector = generate_embedding(opportunity_text)
    embedding_score = cosine_similarity(candidate_vector, opportunity_vector)
    
    # Keyword matching bonus
    keyword_matches = 0
    candidate_keywords = set(candidate_skills.lower().split() + candidate_domains.lower().split())
    opportunity_keywords = set(opportunity_text.lower().split())
    matches = candidate_keywords & opportunity_keywords
    keyword_score = min(100, len(matches) * 10)  # 10 points per match
    
    # Combine scores
    fit_score = (embedding_score * 0.6) + (keyword_score * 0.4)
    return min(100, max(0, fit_score))

def generate_match_reasoning(candidate_profile, opportunity, fit_score):

    skills = ", ".join(candidate_profile["core_skills"][:3])

    return (
        f"The candidate demonstrates strong experience in {skills}, "
        f"which aligns well with this opportunity. "
        f"Their background in AI-driven projects and backend systems "
        f"makes them a strong fit with a match score of {fit_score}%."
    )
def rank_opportunity_matches(candidate_profile: dict, opportunities: list) -> list:

    results = []

    for opportunity in opportunities:

        fit_score = calculate_fit_score(candidate_profile, opportunity)

        reasoning = generate_match_reasoning(
            candidate_profile,
            opportunity,
            fit_score
        )

        results.append({
            "opportunity": opportunity,
            "fit_score": fit_score,
            "match_reasoning": reasoning
        })

    results.sort(key=lambda x: x["fit_score"], reverse=True)

    return results