"""
Project Narrative Parser

Breaks down project text into structured components:
  - what_was_built: Core product/feature description
  - candidate_role: Specific role(s) the candidate took
  - outcome: Results and impact statements
  - decisions_made: Technical and strategic decisions
  - challenges_faced: Problems encountered and resolved
"""

import re
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class ProjectNarrative(BaseModel):
    """Structured breakdown of a project narrative."""
    raw_text: str = Field(
        ...,
        description="Original project description text"
    )
    what_was_built: str = Field(
        ...,
        description="Core product/feature that was constructed",
        examples=["Real-time data pipeline for ML training", "REST API for event streaming"]
    )
    candidate_role: str = Field(
        ...,
        description="Specific role(s) the candidate took in the project",
        examples=["Lead backend engineer", "Full-stack contributor", "Architecture designer"]
    )
    outcome: str = Field(
        ...,
        description="Results and impact statements",
        examples=["Reduced query latency by 40%", "Shipped to 50k users"]
    )
    decisions_made: List[str] = Field(
        default_factory=list,
        description="Technical and strategic decisions documented"
    )
    challenges_faced: List[str] = Field(
        default_factory=list,
        description="Problems encountered and how they were resolved"
    )


def extract_sentences_by_keyword(
    text: str,
    keywords: List[str],
    context_sentences: int = 2
) -> List[str]:
    """
    Extract sentences containing specific keywords with surrounding context.
    
    Args:
        text: Full project narrative
        keywords: List of keywords to search for
        context_sentences: Number of surrounding sentences to include
        
    Returns:
        List of extracted text passages
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    relevant_sentences = []
    for i, sentence in enumerate(sentences):
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            # Gather context
            start_idx = max(0, i - context_sentences)
            end_idx = min(len(sentences), i + context_sentences + 1)
            context = ' '.join(sentences[start_idx:end_idx])
            relevant_sentences.append(context)
    
    return relevant_sentences


def parse_project_narrative(text: str) -> ProjectNarrative:
    """
    Parse unstructured project narrative into components.
    
    Uses heuristic keyword matching and sentence extraction to identify
    project components from natural language descriptions.
    
    Args:
        text: Raw project description/narrative
        
    Returns:
        ProjectNarrative: Structured project data
    """
    
    # Extract "what was built"
    build_keywords = [
        "built", "created", "developed", "implemented", "designed",
        "architected", "engineered", "constructed", "framework",
        "system", "platform", "service", "application", "tool",
        "library", "database", "API"
    ]
    build_passages = extract_sentences_by_keyword(text, build_keywords, context_sentences=1)
    what_was_built = build_passages[0] if build_passages else "Project details not clearly specified"
    # Clean up to single sentence if too long
    what_was_built = what_was_built.split('.')[0] if len(what_was_built) > 150 else what_was_built
    
    # Extract candidate role
    role_keywords = [
        "led", "managed", "owner", "architect", "engineer", "developer",
        "contributor", "team", "lead", "senior", "junior", "responsible",
        "drove", "spearheaded", "directed", "oversaw"
    ]
    role_passages = extract_sentences_by_keyword(text, role_keywords, context_sentences=1)
    candidate_role = role_passages[0] if role_passages else "Contributor"
    candidate_role = candidate_role.split('.')[0] if len(candidate_role) > 120 else candidate_role
    
    # Extract outcome/impact
    outcome_keywords = [
        "reduced", "improved", "increased", "decreased", "achieved",
        "delivered", "launched", "shipped", "impact", "result",
        "outcome", "metrics", "performance", "growth", "%", "users",
        "customers", "success", "won", "gained"
    ]
    outcome_passages = extract_sentences_by_keyword(text, outcome_keywords, context_sentences=1)
    outcome = outcome_passages[0] if outcome_passages else "Outcome not specified"
    outcome = outcome.split('.')[0] if len(outcome) > 150 else outcome
    
    # Extract decisions made
    decision_keywords = [
        "decided", "chose", "selected", "opted", "picked", "used",
        "implemented", "adopted", "migrated", "switched", "refactored",
        "engineered", "trade-off", "tradeoff", "approach", "strategy",
        "design", "architecture", "stack", "technology"
    ]
    decisions_passages = extract_sentences_by_keyword(text, decision_keywords, context_sentences=0)
    decisions_made = [p.split('.')[0] for p in decisions_passages[:3]]
    
    # Extract challenges faced
    challenge_keywords = [
        "challenge", "problem", "issue", "bug", "difficult", "hard",
        "struggled", "overcame", "solved", "fixed", "resolved",
        "error", "failure", "bottleneck", "limitation", "constraint",
        "failed", "unexpected", "debug", "broke", "crashed", "slow"
    ]
    challenge_passages = extract_sentences_by_keyword(text, challenge_keywords, context_sentences=1)
    challenges_faced = [p.split('.')[0] for p in challenge_passages[:3]]
    
    return ProjectNarrative(
        raw_text=text,
        what_was_built=what_was_built,
        candidate_role=candidate_role,
        outcome=outcome,
        decisions_made=decisions_made,
        challenges_faced=challenges_faced
    )
