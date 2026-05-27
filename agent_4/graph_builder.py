"""
Skill Graph Builder

Constructs a structured graph where nodes represent distinct skills,
and edges represent projects proving them.
Each edge encapsulates confidence score and evidence summary for frontend visualization.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Set, Any
from .confidence import SkillConfidenceScore


class SkillNode(BaseModel):
    """Node in skill graph representing a technical skill."""
    id: str = Field(
        ...,
        description="Unique identifier for the skill (normalized)",
        examples=["python", "system-design", "react"]
    )
    name: str = Field(
        ...,
        description="Display name of the skill"
    )
    proficiency_level: str = Field(
        ...,
        description="Current proficiency level"
    )
    overall_confidence: float = Field(
        ...,
        description="Average confidence score across all projects (0-100)"
    )
    project_count: int = Field(
        ...,
        description="Number of projects demonstrating this skill"
    )


class SkillEdge(BaseModel):
    """Edge in skill graph linking skill to project evidence."""
    source_skill_id: str = Field(
        ...,
        description="Source skill node ID"
    )
    target_project_id: str = Field(
        ...,
        description="Target project identifier"
    )
    confidence_score: float = Field(
        ...,
        description="Skill confidence score for this project (0-100)"
    )
    evidence_summary: str = Field(
        ...,
        description="One-line evidence summary for UI display"
    )
    ownership_level: str = Field(
        ...,
        description="Ownership classification for this project"
    )
    outcome_metrics_count: int = Field(
        ...,
        description="Number of quantified outcomes in project"
    )


class SkillGraph(BaseModel):
    """Complete skill graph structure for frontend consumption."""
    nodes: List[SkillNode] = Field(
        ...,
        description="Skill nodes in the graph"
    )
    edges: List[SkillEdge] = Field(
        ...,
        description="Edges connecting skills to project evidence"
    )
    stats: Dict[str, Any] = Field(
        default_factory=dict,
        description="Graph statistics and metadata"
    )


def normalize_skill_id(skill_name: str) -> str:
    """
    Convert skill name to normalized ID for graph use.
    
    Args:
        skill_name: Display name of skill
        
    Returns:
        Normalized ID (lowercase, hyphenated)
    """
    return skill_name.lower().replace(" ", "-").replace("/", "-")


def build_skill_graph(
    confidence_scores_by_skill: Dict[str, List[SkillConfidenceScore]],
    projects_data: Dict[str, Dict] = None
) -> SkillGraph:
    """
    Build complete skill graph from confidence scores.
    
    Constructs nodes for each unique skill and edges linking to
    projects providing evidence. Each edge includes confidence score
    and evidence summary suitable for frontend rendering.
    
    Args:
        confidence_scores_by_skill: Dictionary mapping skill names to
                                   lists of SkillConfidenceScore objects
        projects_data: Optional mapping of project IDs to project metadata
        
    Returns:
        SkillGraph: Complete graph structure with nodes and edges
    """
    
    nodes: List[SkillNode] = []
    edges: List[SkillEdge] = []
    
    if projects_data is None:
        projects_data = {}
    
    # Build nodes and edges for each skill
    for skill_name, score_list in confidence_scores_by_skill.items():
        skill_id = normalize_skill_id(skill_name)
        
        # Calculate aggregate metrics for skill node
        avg_confidence = sum(s.confidence_score for s in score_list) / len(score_list)
        project_count = sum(s.evidence_projects for s in score_list)
        
        # Use proficiency from highest confidence score
        proficiency_level = score_list[0].proficiency_level
        if any(s.proficiency_level == "expert" for s in score_list):
            proficiency_level = "expert"
        elif any(s.proficiency_level == "advanced" for s in score_list):
            proficiency_level = "advanced"
        
        # Create skill node
        node = SkillNode(
            id=skill_id,
            name=skill_name,
            proficiency_level=proficiency_level,
            overall_confidence=avg_confidence,
            project_count=project_count
        )
        nodes.append(node)
        
        # Create edges from this skill to projects
        for i, score in enumerate(score_list):
            project_id = projects_data.get(
                f"project_{i}",
                {}
            ).get("id", f"project_{i}")
            
            # Extract outcome metrics count from components
            outcome_component = next(
                (c for c in score.components if c.component_name == "outcome_clarity"),
                None
            )
            outcome_metrics_count = 0
            if outcome_component:
                # Estimate from component score
                outcome_metrics_count = max(1, int(outcome_component.score * 3))
            
            # Extract ownership level from summary or components
            ownership_level = "contributed"  # default
            if "led" in score.summary.lower():
                ownership_level = "led"
            elif "assisted" in score.summary.lower():
                ownership_level = "assisted"
            
            # Build evidence summary
            evidence_summary = f"{ownership_level.capitalize()} {skill_name} work: {score.proficiency_level} proficiency"
            
            # Create edge
            edge = SkillEdge(
                source_skill_id=skill_id,
                target_project_id=project_id,
                confidence_score=score.confidence_score,
                evidence_summary=evidence_summary,
                ownership_level=ownership_level,
                outcome_metrics_count=outcome_metrics_count
            )
            edges.append(edge)
    
    # Calculate graph statistics
    stats = {
        "total_skills": len(nodes),
        "total_edges": len(edges),
        "average_skill_confidence": (
            sum(n.overall_confidence for n in nodes) / len(nodes)
            if nodes else 0
        ),
        "total_projects_linked": len(set(e.target_project_id for e in edges)),
        "top_skills": sorted(nodes, key=lambda n: n.overall_confidence, reverse=True)[:3]
    }
    
    return SkillGraph(
        nodes=nodes,
        edges=edges,
        stats=stats
    )


def graph_to_dict(graph: SkillGraph) -> Dict:
    """
    Convert SkillGraph to standard dictionary format for JSON serialization.
    
    Args:
        graph: SkillGraph object
        
    Returns:
        Dictionary representation suitable for frontend consumption
    """
    return {
        "nodes": [
            {
                "id": node.id,
                "label": node.name,
                "proficiency": node.proficiency_level,
                "confidence": node.overall_confidence,
                "projectCount": node.project_count
            }
            for node in graph.nodes
        ],
        "edges": [
            {
                "source": edge.source_skill_id,
                "target": edge.target_project_id,
                "confidence": edge.confidence_score,
                "evidence": edge.evidence_summary,
                "ownership": edge.ownership_level,
                "metrics": edge.outcome_metrics_count
            }
            for edge in graph.edges
        ],
        "stats": {
            "totalSkills": graph.stats.get("total_skills", 0),
            "totalEdges": graph.stats.get("total_edges", 0),
            "averageConfidence": graph.stats.get("average_skill_confidence", 0),
            "topSkills": [
                {"name": s.name, "confidence": s.overall_confidence}
                for s in graph.stats.get("top_skills", [])
            ]
        }
    }
