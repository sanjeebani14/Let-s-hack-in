"""
Proof Card Generator

Accepts a target opportunity as context, filters the skill graph
to top 3-5 most relevant skills, and outputs clean snapshot containing:
skill_name, confidence_score, and best_project_evidence.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from .graph_builder import SkillGraph, normalize_skill_id


class ProofCardSkill(BaseModel):
    """Single skill card in proof snapshot."""
    skill_name: str = Field(
        ...,
        description="Name of the technical skill"
    )
    confidence_score: float = Field(
        ...,
        description="Confidence score for this skill (0-100)"
    )
    proficiency_level: str = Field(
        ...,
        description="Proficiency level"
    )
    best_project_evidence: str = Field(
        ...,
        description="One-line evidence from best project demonstrating skill"
    )
    project_count: int = Field(
        ...,
        description="Number of projects providing evidence"
    )


class ProofCard(BaseModel):
    """Clean snapshot of top relevant skills for target opportunity."""
    opportunity_title: str = Field(
        ...,
        description="Title/name of target opportunity"
    )
    required_skills: List[str] = Field(
        ...,
        description="Skills listed as required in opportunity description"
    )
    matched_skills: List[ProofCardSkill] = Field(
        ...,
        description="Top 3-5 candidate skills matched to opportunity"
    )
    total_relevance_score: float = Field(
        ...,
        description="Average relevance of matched skills (0-100)"
    )
    summary: str = Field(
        ...,
        description="One-line summary of skill match"
    )


def extract_skills_from_opportunity(opportunity_description: str) -> List[str]:
    """
    Extract required skills from opportunity description.
    
    Args:
        opportunity_description: Full opportunity text
        
    Returns:
        List of extracted skill names
    """
    # Keywords that often precede skill mentions
    skill_markers = [
        r"required:\s*(.+?)(?:\n|$)",
        r"skills:\s*(.+?)(?:\n|$)",
        r"experience with\s+(.+?)(?:\n|,|$)",
        r"expertise in\s+(.+?)(?:\n|,|$)",
        r"(?:strong|solid|excellent)\s+(?:knowledge|experience)\s+(?:in|with)\s+(.+?)(?:\n|,|$)",
    ]
    
    import re
    found_skills = []
    
    for pattern in skill_markers:
        matches = re.findall(pattern, opportunity_description, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            # Split by common delimiters
            skills = re.split(r'[,;/]', match)
            for skill in skills:
                skill_cleaned = skill.strip()
                if skill_cleaned and len(skill_cleaned) < 50:
                    found_skills.append(skill_cleaned)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in found_skills:
        skill_normalized = skill.lower()
        if skill_normalized not in seen:
            seen.add(skill_normalized)
            unique_skills.append(skill)
    
    return unique_skills[:10]  # Top 10 required skills


def calculate_skill_relevance(
    skill_name: str,
    required_skills: List[str],
    confidence_score: float
) -> float:
    """
    Calculate relevance of candidate skill to opportunity requirements.
    
    Args:
        skill_name: Candidate's skill
        required_skills: Skills required by opportunity
        confidence_score: Candidate's confidence in this skill
        
    Returns:
        Relevance score (0-1)
    """
    # Direct match
    skill_lower = skill_name.lower()
    for req_skill in required_skills:
        req_lower = req_skill.lower()
        if skill_lower == req_lower:
            return min(1.0, confidence_score / 100.0)
        # Partial match (e.g., "Node.js" matches "Node")
        if skill_lower in req_lower or req_lower in skill_lower:
            return min(0.9, (confidence_score / 100.0) * 0.9)
    
    # No direct match, but high confidence might still be valuable
    if confidence_score >= 75:
        return 0.5  # Transferable skills
    
    return 0.3  # Related but not primary requirement


def generate_proof_card(
    skill_graph: SkillGraph,
    opportunity_description: str,
    opportunity_title: str = "Target Opportunity",
    max_skills: int = 5,
    min_confidence: float = 50.0
) -> ProofCard:
    """
    Generate proof card from skill graph filtered to opportunity requirements.
    
    Extracts required skills from opportunity, filters candidate skills
    by relevance, and returns top 3-5 most relevant skills with evidence.
    
    Args:
        skill_graph: Complete SkillGraph from graph_builder
        opportunity_description: Full opportunity job description
        opportunity_title: Title of the opportunity
        max_skills: Maximum skills to include (typically 3-5)
        min_confidence: Minimum confidence threshold
        
    Returns:
        ProofCard: Filtered skill snapshot for opportunity
    """
    
    # Extract required skills from opportunity
    required_skills = extract_skills_from_opportunity(opportunity_description)
    
    # Calculate relevance for each candidate skill
    skill_relevances = []
    
    for node in skill_graph.nodes:
        if node.overall_confidence < min_confidence:
            continue
        
        relevance = calculate_skill_relevance(
            node.name,
            required_skills,
            node.overall_confidence
        )
        
        # Combined score: relevance × confidence
        combined_score = relevance * (node.overall_confidence / 100.0)
        
        skill_relevances.append({
            "node": node,
            "relevance": relevance,
            "combined_score": combined_score
        })
    
    # Sort by combined score descending
    skill_relevances.sort(key=lambda x: x["combined_score"], reverse=True)
    
    # Select top skills
    top_skills = skill_relevances[:max_skills]
    
    # Build proof card entries
    matched_skills: List[ProofCardSkill] = []
    
    for skill_info in top_skills:
        node = skill_info["node"]
        
        # Find best project evidence (highest confidence edge)
        best_edge = None
        best_confidence = 0.0
        
        for edge in skill_graph.edges:
            if (edge.source_skill_id == node.id and 
                edge.confidence_score > best_confidence):
                best_edge = edge
                best_confidence = edge.confidence_score
        
        # Create proof evidence string
        if best_edge:
            evidence = best_edge.evidence_summary
        else:
            evidence = f"{node.proficiency_level.capitalize()} proficiency across {node.project_count} projects"
        
        proof_card_skill = ProofCardSkill(
            skill_name=node.name,
            confidence_score=node.overall_confidence,
            proficiency_level=node.proficiency_level,
            best_project_evidence=evidence,
            project_count=node.project_count
        )
        matched_skills.append(proof_card_skill)
    
    # Calculate average relevance
    if matched_skills:
        total_relevance_score = sum(
            s.confidence_score for s in matched_skills
        ) / len(matched_skills)
    else:
        total_relevance_score = 0.0
    
    # Generate summary
    if matched_skills:
        top_3_skills = ", ".join([s.skill_name for s in matched_skills[:3]])
        summary = f"Strong match: {top_3_skills} ({total_relevance_score:.0f}/100 avg confidence)"
    else:
        summary = "Insufficient skill match for this opportunity"
    
    return ProofCard(
        opportunity_title=opportunity_title,
        required_skills=required_skills,
        matched_skills=matched_skills,
        total_relevance_score=total_relevance_score,
        summary=summary
    )


def proof_card_to_dict(proof_card: ProofCard) -> Dict:
    """
    Convert ProofCard to dictionary for frontend consumption.
    
    Args:
        proof_card: ProofCard object
        
    Returns:
        Dictionary suitable for JSON serialization
    """
    return {
        "opportunity": {
            "title": proof_card.opportunity_title,
            "requiredSkills": proof_card.required_skills
        },
        "matched_skills": [
            {
                "name": skill.skill_name,
                "confidence": skill.confidence_score,
                "proficiency": skill.proficiency_level,
                "evidence": skill.best_project_evidence,
                "projectCount": skill.project_count
            }
            for skill in proof_card.matched_skills
        ],
        "match": {
            "relevanceScore": proof_card.total_relevance_score,
            "summary": proof_card.summary
        }
    }
