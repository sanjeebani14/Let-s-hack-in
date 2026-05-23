"""
Engagement Signal Checker

Scans a mock database/log of interactions to see if target company employees
have interacted with the candidate's public work (e.g., starring GitHub repo, liking article).
Returns an array of objects containing person's name, role, and interaction.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any


class EmployeeInteraction(BaseModel):
    """A single interaction from a target company employee with candidate's work."""
    person_name: str = Field(
        ...,
        description="Name of the employee who interacted",
        examples=["Sarah Chen", "Marcus Johnson"]
    )
    person_role: str = Field(
        ...,
        description="Job title/role of the employee",
        examples=["Senior ML Engineer", "VP Engineering", "Tech Lead"]
    )
    company: str = Field(
        ...,
        description="Name of the company they work for"
    )
    interaction_type: str = Field(
        ...,
        description="Type of interaction: 'github_star', 'article_like', 'repo_fork', 'comment', 'mention'",
        examples=["github_star", "article_like", "repo_fork"]
    )
    interaction_detail: str = Field(
        ...,
        description="Specific interaction string describing what they did",
        examples=["Starred your PyTorch Utils repo", "Liked your Medium article on ML optimization"]
    )
    interaction_date: str = Field(
        ...,
        description="When the interaction occurred",
        examples=["2026-05-20", "2026-04-15"]
    )


class EngagementResponse(BaseModel):
    """Response from engagement signal check."""
    interactions: List[EmployeeInteraction] = Field(
        ...,
        description="List of detected employee interactions"
    )
    engagement_strength: float = Field(
        ...,
        description="Overall engagement score 0.0-1.0 (higher = more employees engaged)",
        ge=0.0,
        le=1.0
    )
    summary: str = Field(
        ...,
        description="One-line summary of engagement signals"
    )


def check_engagement_signals(
    candidate_profile: Dict[str, Any],
    opportunity_data: Dict[str, Any]
) -> EngagementResponse:
    """
    Check if target company employees have interacted with candidate's work.
    
    Args:
        candidate_profile: Extracted candidate profile (from Member A)
        opportunity_data: Full opportunity data including target company
        
    Returns:
        EngagementResponse: List of employee interactions and engagement strength
    """
    
    # Mock interaction database
    # In real scenario, this would query actual GitHub API, Twitter, LinkedIn, etc.
    mock_interactions_db = {
        "NeuralFlow Startup": [
            {
                "person_name": "Alex Kumar",
                "person_role": "CTO & Co-Founder",
                "company": "NeuralFlow Startup",
                "interaction_type": "github_star",
                "interaction_detail": "Starred your TensorFlow optimization repo",
                "interaction_date": "2026-05-18"
            },
            {
                "person_name": "Emma Wright",
                "person_role": "Senior ML Engineer",
                "company": "NeuralFlow Startup",
                "interaction_type": "repo_fork",
                "interaction_detail": "Forked your inference pipeline project",
                "interaction_date": "2026-05-10"
            }
        ],
        "DataFlow Collective": [
            {
                "person_name": "James Park",
                "person_role": "VP Engineering",
                "company": "DataFlow Collective",
                "interaction_type": "article_like",
                "interaction_detail": "Liked your blog post on async FastAPI patterns",
                "interaction_date": "2026-05-19"
            }
        ],
        "QuantumAI Labs": [
            {
                "person_name": "Dr. Lisa Chen",
                "person_role": "Head of ML Infrastructure",
                "company": "QuantumAI Labs",
                "interaction_type": "comment",
                "interaction_detail": "Commented on your PyTorch distributed training discussion",
                "interaction_date": "2026-05-16"
            },
            {
                "person_name": "Robert Singh",
                "person_role": "Senior Backend Engineer",
                "company": "QuantumAI Labs",
                "interaction_type": "github_star",
                "interaction_detail": "Starred your Kubernetes deployment templates",
                "interaction_date": "2026-05-12"
            }
        ],
        "VisionTech Inc": [
            {
                "person_name": "Sofia Rossi",
                "person_role": "Tech Lead, Backend",
                "company": "VisionTech Inc",
                "interaction_type": "mention",
                "interaction_detail": "Mentioned your FastAPI best practices in team meeting notes",
                "interaction_date": "2026-05-17"
            }
        ],
        "default": []
    }
    
    company_name = opportunity_data.get("company", "")
    interactions = mock_interactions_db.get(company_name, mock_interactions_db["default"])
    
    # Convert to EmployeeInteraction objects
    employee_interactions = [
        EmployeeInteraction(**interaction)
        for interaction in interactions
    ]
    
    # Calculate engagement strength
    # Base calculation: 0.2 points per interaction (capped at 1.0)
    engagement_strength = min(len(employee_interactions) * 0.2, 1.0)
    
    # Weight by interaction type (stars and forks are stronger signals)
    for interaction in employee_interactions:
        if interaction.interaction_type in ["github_star", "repo_fork"]:
            engagement_strength = min(engagement_strength + 0.15, 1.0)
    
    # Generate summary
    if employee_interactions:
        role_count = len(set(i.person_role for i in employee_interactions))
        summary = f"{len(employee_interactions)} employees interacted, including {role_count} different roles"
    else:
        summary = "No detected employee interactions yet, but opportunity to build visibility"
    
    return EngagementResponse(
        interactions=employee_interactions,
        engagement_strength=engagement_strength,
        summary=summary
    )
