import json
from member_a.embeddings import generate_embedding, cosine_similarity


def calculate_fit_score(candidate_profile: dict, opportunity: dict) -> float:

    candidate_text = json.dumps(candidate_profile)
    opportunity_text = json.dumps(opportunity)

    candidate_vector = generate_embedding(candidate_text)
    opportunity_vector = generate_embedding(opportunity_text)

    return cosine_similarity(candidate_vector, opportunity_vector)

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