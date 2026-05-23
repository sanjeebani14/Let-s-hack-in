"""
Shared Context Detector

Compares candidate metadata (communities, hackathons, open-source repositories)
against the target team's corporate or engineering social touchpoints.
Returns a list of specific shared touchpoints found.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any


class SharedContext(BaseModel):
    """A single shared touchpoint between candidate and target team."""
    context_type: str = Field(
        ...,
        description="Type of shared context: 'hackathon', 'community', 'opensource', 'conference'",
        examples=["hackathon", "community", "opensource"]
    )
    name: str = Field(
        ...,
        description="Name of the shared context/event/project",
        examples=["PyCon 2025", "Python Discord Server", "PyTorch Contrib"]
    )
    relevance_score: float = Field(
        ...,
        description="Relevance score 0.0-1.0",
        ge=0.0,
        le=1.0
    )


class ContextDetectorResponse(BaseModel):
    """Response from shared context detection."""
    shared_contexts: List[SharedContext] = Field(
        ...,
        description="List of detected shared touchpoints"
    )
    total_overlap_score: float = Field(
        ...,
        description="Average relevance score of all shared contexts (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    summary: str = Field(
        ...,
        description="One-line summary of shared contexts"
    )


def detect_shared_contexts(
    candidate_profile: Dict[str, Any],
    opportunity_data: Dict[str, Any]
) -> ContextDetectorResponse:
    """
    Compare candidate metadata against target team's touchpoints.
    
    Args:
        candidate_profile: Extracted candidate profile (from Member A)
        opportunity_data: Full opportunity data including team metadata
        
    Returns:
        ContextDetectorResponse: Detected shared contexts with scoring
    """
    
    # Mock candidate contexts
    candidate_contexts = {
        "communities": ["Python Discord", "ML Community", "Startup Circle"],
        "hackathons": ["HackTheAI 2025", "PyHack 2024", "Web3 Summit Hackathon"],
        "opensource": ["PyTorch Contributors", "TensorFlow Community", "FastAPI Sponsors"],
        "conferences": ["PyCon 2025", "NeurIPS 2024", "PyData Summit"]
    }
    
    # Mock target team contexts
    target_team_contexts = {
        "communities": ["Python Discord", "ML Community", "Backend Engineers Guild"],
        "hackathons": ["HackTheAI 2025", "AI Engineering Hackathon"],
        "opensource": ["PyTorch Contributors", "FastAPI Sponsors", "OpenAI Community"],
        "conferences": ["PyCon 2025", "AI Summit 2025"]
    }
    
    shared_contexts: List[SharedContext] = []
    relevance_scores = []
    
    # Check communities
    for context in candidate_contexts["communities"]:
        if context in target_team_contexts["communities"]:
            shared_contexts.append(SharedContext(
                context_type="community",
                name=context,
                relevance_score=0.85
            ))
            relevance_scores.append(0.85)
    
    # Check hackathons
    for context in candidate_contexts["hackathons"]:
        if context in target_team_contexts["hackathons"]:
            shared_contexts.append(SharedContext(
                context_type="hackathon",
                name=context,
                relevance_score=0.90
            ))
            relevance_scores.append(0.90)
    
    # Check open-source
    for context in candidate_contexts["opensource"]:
        if context in target_team_contexts["opensource"]:
            shared_contexts.append(SharedContext(
                context_type="opensource",
                name=context,
                relevance_score=0.80
            ))
            relevance_scores.append(0.80)
    
    # Check conferences
    for context in candidate_contexts["conferences"]:
        if context in target_team_contexts["conferences"]:
            shared_contexts.append(SharedContext(
                context_type="conference",
                name=context,
                relevance_score=0.75
            ))
            relevance_scores.append(0.75)
    
    # Calculate total overlap score
    total_overlap_score = (
        sum(relevance_scores) / len(relevance_scores)
        if relevance_scores
        else 0.0
    )
    
    # Generate summary
    if shared_contexts:
        summary = f"Found {len(shared_contexts)} shared touchpoints including {shared_contexts[0].name}"
    else:
        summary = "No direct shared contexts detected, but may have indirect connections"
    
    return ContextDetectorResponse(
        shared_contexts=shared_contexts,
        total_overlap_score=total_overlap_score,
        summary=summary
    )
