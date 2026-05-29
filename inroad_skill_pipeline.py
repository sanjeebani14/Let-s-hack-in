"""
Build Agent 4 skill graph + proof card from portfolio text.
"""

from __future__ import annotations

import re
from typing import Dict, List

from agent_4 import (
    build_skill_graph,
    calculate_confidence_score,
    detect_ownership_level,
    evaluate_complexity,
    generate_proof_card,
    graph_to_dict,
    parse_project_narrative,
    proof_card_to_dict,
    score_outcome_clarity,
    extract_skills_from_text,
)
from agent_4.confidence import SkillConfidenceScore


def _split_projects(project_descriptions: str) -> List[Dict[str, str]]:
    chunks = re.split(r"\n\s*[-•*]\s+|\n\n+", project_descriptions.strip())
    projects = []
    for i, chunk in enumerate(chunks):
        text = chunk.strip()
        if len(text) < 20:
            continue
        projects.append({"id": f"project_{i + 1}", "description": text})
    if not projects and len(project_descriptions.strip()) >= 20:
        projects.append({"id": "project_1", "description": project_descriptions.strip()})
    return projects


def build_skill_graph_from_portfolio(project_descriptions: str):
    projects = _split_projects(project_descriptions)
    confidence_by_skill: Dict[str, List[SkillConfidenceScore]] = {}

    for project in projects:
        text = project["description"]
        narrative = parse_project_narrative(text)
        ownership = detect_ownership_level(text, narrative.candidate_role)
        outcome = score_outcome_clarity(narrative.outcome or text)
        complexity = evaluate_complexity(text)

        skills = extract_skills_from_text(text, num_to_extract=6)
        if not skills:
            continue

        for skill in skills:
            freq = 1.0 / max(len(skills), 1)
            score = calculate_confidence_score(
                skill,
                ownership,
                outcome,
                complexity,
                project_count=1,
                skill_frequency=freq,
            )
            confidence_by_skill.setdefault(skill, []).append(score)

    if not confidence_by_skill:
        fallback = extract_skills_from_text(project_descriptions, num_to_extract=3)
        for skill in fallback:
            narrative = parse_project_narrative(project_descriptions[:500])
            ownership = detect_ownership_level(project_descriptions, narrative.candidate_role)
            outcome = score_outcome_clarity(project_descriptions)
            complexity = evaluate_complexity(project_descriptions)
            confidence_by_skill[skill] = [
                calculate_confidence_score(
                    skill, ownership, outcome, complexity, project_count=1, skill_frequency=1.0
                )
            ]

    return build_skill_graph(confidence_by_skill)


def build_proof_for_opportunity(skill_graph, opportunity: Dict) -> Dict:
    card = generate_proof_card(
        skill_graph,
        opportunity.get("description", ""),
        opportunity_title=opportunity.get("title", "Opportunity"),
    )
    return proof_card_to_dict(card)
