"""
Action Instruction Generator

Evaluates InRoad score findings and outputs exactly 2-3 immediate, concrete,
time-sensitive tactical instructions. Avoids generic advice.

Examples:
  - "Contribute a patch fixing open issue #12 on their public repository"
  - "Reference your shared experience at the PyCon 2025 hackathon"
  - "Star their recent AWS Lambda optimization repo and leave a comment with insights"
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum


class InstructionCategory(str, Enum):
    """Categories of tactical instructions."""
    TECHNICAL_CONTRIBUTION = "technical_contribution"
    SHARED_CONTEXT_REFERENCE = "shared_context_reference"
    ENGAGEMENT_FOLLOW_UP = "engagement_follow_up"
    CONNECTOR_REQUEST = "connector_request"
    PUBLIC_VISIBILITY = "public_visibility"


class TacticalInstruction(BaseModel):
    """Single concrete tactical instruction."""
    instruction: str = Field(
        ...,
        description="Exact, actionable instruction with specifics (not generic advice)",
        examples=[
            "Contribute a patch fixing open issue #12 on their public repository",
            "Reference your shared experience at the PyCon 2025 hackathon in your outreach",
            "Star their recent AWS Lambda optimization repo and leave a technical comment"
        ]
    )
    category: InstructionCategory = Field(
        ...,
        description="Category of instruction"
    )
    reasoning: str = Field(
        ...,
        description="Why this action strengthens your position",
        examples=[
            "They actively maintain this repo and value community contributions",
            "Shared community signals increase warm introduction likelihood"
        ]
    )
    time_frame: str = Field(
        ...,
        description="When to execute: 'immediate' (today), 'this_week', 'before_outreach'",
        examples=["immediate", "this_week", "before_outreach"]
    )


class ActionInstructions(BaseModel):
    """Container for 2-3 tactical instructions."""
    opportunity_title: str = Field(
        ...,
        description="Target opportunity title"
    )
    instructions: List[TacticalInstruction] = Field(
        ...,
        description="Array of 2-3 concrete tactical instructions",
        min_items=2,
        max_items=3
    )
    priority_sequence: List[int] = Field(
        ...,
        description="Order to execute instructions (1-indexed)",
        examples=[[1, 2, 3]]
    )
    estimated_prep_time_minutes: int = Field(
        ...,
        description="Total estimated time to complete all instructions",
        examples=[15, 30, 45]
    )


def generate_action_instructions(
    opportunity_title: str,
    inroad_score: float,
    way_in_strategy: Optional[Dict[str, Any]] = None,
    shared_contexts: Optional[List[Dict[str, Any]]] = None,
    engagement_signals: Optional[List[Dict[str, Any]]] = None,
    connector_data: Optional[Dict[str, Any]] = None,
    proof_card: Optional[Dict[str, Any]] = None,
    opportunity_data: Optional[Dict[str, Any]] = None,
) -> ActionInstructions:
    """
    Generate 2-3 concrete tactical instructions based on InRoad findings.

    Args:
        opportunity_title: Name of target opportunity
        inroad_score: Combined InRoad Chemistry score (0-100)
        way_in_strategy: Entry strategy from Agent 3
        shared_contexts: List of shared touchpoints
        engagement_signals: Employee interactions
        connector_data: Connector person data
        proof_card: Proof card from Agent 4
        opportunity_data: Full opportunity details

    Returns:
        ActionInstructions: 2-3 tactical instructions with reasoning
    """

    # Sanitize inputs with safe defaults
    way_in_strategy = way_in_strategy or {}
    shared_contexts = shared_contexts or []
    engagement_signals = engagement_signals or []
    connector_data = connector_data or {}
    proof_card = proof_card or {}
    opportunity_data = opportunity_data or {}

    instructions_list: List[TacticalInstruction] = []

    # INSTRUCTION 1: High-priority based on strongest signal
    # Determine signal hierarchy
    has_connector = connector_data.get("best_connector") is not None
    has_engagement = len(engagement_signals) > 0
    has_shared_context = len(shared_contexts) > 0
    has_proven_skills = len(proof_card.get("matched_skills", [])) > 0

    # Build instruction 1: Connector-first if available (highest warmth)
    if has_connector and inroad_score >= 60:
        connector_name = connector_data.get("best_connector", {}).get("person_name", "your shared contact")
        connector_rel = connector_data.get("best_connector", {}).get("relationship_to_candidate", "connection")
        
        instruction_1 = TacticalInstruction(
            instruction=f"Request an introduction from {connector_name} ({connector_rel}) to the hiring team. Prepare a 1-line context: 'Interested in their {opportunity_title} work.'",
            category=InstructionCategory.CONNECTOR_REQUEST,
            reasoning="Warm introductions have 5-10x higher response rate than cold outreach. Your connection already knows their value.",
            time_frame="this_week"
        )
        instructions_list.append(instruction_1)

    # Build instruction 2: Engagement follow-up if signals exist
    elif has_engagement and inroad_score >= 50:
        person_name = engagement_signals[0].get("person_name", "the team")
        interaction = engagement_signals[0].get("interaction_detail", "your work")
        
        instruction_2 = TacticalInstruction(
            instruction=f"Reply to {person_name}'s interaction ({interaction}) with a thoughtful comment about the related technology. Show familiarity, not flattery.",
            category=InstructionCategory.ENGAGEMENT_FOLLOW_UP,
            reasoning="They've already demonstrated interest in your work. Direct engagement resets the relationship from cold to warm.",
            time_frame="immediate"
        )
        instructions_list.append(instruction_2)

    # Build instruction 3: Shared context reference
    if has_shared_context:
        best_context = shared_contexts[0] if isinstance(shared_contexts, list) else {}
        context_name = best_context.get("name", "shared community")
        context_type = best_context.get("context_type", "community")
        
        if context_type == "hackathon":
            instruction = TacticalInstruction(
                instruction=f"Prepare a 2-line anecdote about {context_name}: What problem did you tackle? What did you learn about their tech stack there?",
                category=InstructionCategory.SHARED_CONTEXT_REFERENCE,
                reasoning="Shared experience creates instant credibility and gives them a reason to engage (not just another resume).",
                time_frame="before_outreach"
            )
        elif context_type == "opensource":
            instruction = TacticalInstruction(
                instruction=f"Star their repository and post a specific, technical comment on an open issue. Reference a similar challenge you solved.",
                category=InstructionCategory.PUBLIC_VISIBILITY,
                reasoning="Public contributions signal expertise and show up in their notifications — organic visibility without cold outreach.",
                time_frame="this_week"
            )
        else:
            instruction = TacticalInstruction(
                instruction=f"Reference {context_name} ({context_type}) in your first message. Mention a specific insight or person you both know.",
                category=InstructionCategory.SHARED_CONTEXT_REFERENCE,
                reasoning="Shared touchpoints reduce perceived distance and increase response likelihood.",
                time_frame="before_outreach"
            )
        
        instructions_list.append(instruction)

    # If we haven't built 2 instructions yet, add a skill-based action
    if len(instructions_list) < 2 and has_proven_skills:
        skills = proof_card.get("matched_skills", [])
        if skills:
            top_skill = skills[0]
            skill_name = top_skill.get("skill_name", "your expertise")
            
            instruction = TacticalInstruction(
                instruction=f"Identify one blog post or technical deep-dive you wrote on {skill_name}. Prepare to share it as evidence of expertise.",
                category=InstructionCategory.PUBLIC_VISIBILITY,
                reasoning="Concrete proof points turn claims into verifiable facts. Opportunities value substance over assertions.",
                time_frame="before_outreach"
            )
            instructions_list.append(instruction)

    # Ensure we have at least 2, at most 3 instructions
    if len(instructions_list) < 2:
        # Fallback 1: Generic but still specific technical prep
        instruction = TacticalInstruction(
            instruction="Document your top 2 technical achievements matching this opportunity's core domain. Be specific on metrics and architecture.",
            category=InstructionCategory.PUBLIC_VISIBILITY,
            reasoning="Clear, evidence-backed positioning distinguishes you from generic applicants.",
            time_frame="before_outreach"
        )
        instructions_list.append(instruction)
    
    # Ensure we have at least 2 total
    if len(instructions_list) < 2:
        # Final fallback: Add a second generic instruction
        instruction = TacticalInstruction(
            instruction="Review their company blog/recent tech posts. Prepare a 1-2 sentence insight about what they're building.",
            category=InstructionCategory.SHARED_CONTEXT_REFERENCE,
            reasoning="Demonstrates genuine research and gives you authentic talking points for conversations.",
            time_frame="before_outreach"
        )
        instructions_list.append(instruction)

    instructions_list = instructions_list[:3]  # Max 3

    # Determine priority sequence
    priority_sequence = list(range(1, len(instructions_list) + 1))

    # Estimate time
    estimated_time = 15 if len(instructions_list) == 2 else 30

    return ActionInstructions(
        opportunity_title=opportunity_title,
        instructions=instructions_list,
        priority_sequence=priority_sequence,
        estimated_prep_time_minutes=estimated_time
    )
