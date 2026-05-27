"""
LinkedIn DM Generator

Inputs the connection bridge vector discovered by Agent 3 and outputs
a highly targeted, hyper-personalized, short messaging template.

Ensures professional, organic tone — entirely devoid of typical cold sales language.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from enum import Enum


class LinkedInMessageType(str, Enum):
    """Types of LinkedIn messages based on entry vector."""
    WARM_CONNECTOR = "warm_connector"          # Via established connection
    SHARED_CONTEXT = "shared_context"          # Via shared community/event
    ENGAGEMENT_FOLLOW_UP = "engagement_follow_up"  # Reply to their engagement
    COLLEAGUE_INQUIRY = "colleague_inquiry"    # Peer-level inquiry
    OPEN_INQUIRY = "open_inquiry"              # General inquiry (fallback)


class LinkedInDMTemplate(BaseModel):
    """Customized LinkedIn DM template."""
    message_type: LinkedInMessageType = Field(
        ...,
        description="Type of message based on entry vector"
    )
    subject_line: str = Field(
        ...,
        description="Subject (only included if sender chooses to send as a connection request note)",
        examples=["PyCon 2025 + Python optimization interests"]
    )
    message_body: str = Field(
        ...,
        description="Main message body (max 1,500 characters, ~250 words)",
        examples=[
            "Hey Sarah, I noticed you starred our PyTorch optimization repo..."
        ]
    )
    tone_notes: str = Field(
        ...,
        description="Guidance on delivery tone and pacing",
        examples=["Peer-to-peer, curious and humble. Send immediately."]
    )
    character_count: int = Field(
        ...,
        description="Character count of message_body"
    )


def _sanitize_template_value(value: Any, fallback: str = "") -> str:
    """
    Safely extract string values from any input type.
    Prevents null injection and handles edge cases.
    """
    if value is None:
        return fallback
    if isinstance(value, dict):
        # Try common key patterns
        for key in ["value", "name", "text", "description"]:
            if key in value:
                return str(value[key]).strip()
        return fallback
    if isinstance(value, (list, tuple)):
        return str(value[0]) if value else fallback
    return str(value).strip() if value else fallback


def generate_linkedin_dm(
    opportunity_title: str,
    candidate_name: str,
    way_in_strategy: Optional[Dict[str, Any]] = None,
    shared_contexts: Optional[list] = None,
    engagement_signals: Optional[list] = None,
    connector_data: Optional[Dict[str, Any]] = None,
    inroad_score: float = 0.0,
    opportunity_data: Optional[Dict[str, Any]] = None,
) -> LinkedInDMTemplate:
    """
    Generate highly customized LinkedIn DM based on entry vector.

    Args:
        opportunity_title: Target opportunity/company
        candidate_name: Name of candidate
        way_in_strategy: Entry strategy from Agent 3 (WayInStrategy)
        shared_contexts: List of shared touchpoints
        engagement_signals: Employee interactions
        connector_data: Connector person details
        inroad_score: InRoad Chemistry score
        opportunity_data: Full opportunity metadata

    Returns:
        LinkedInDMTemplate: Customized message ready to send
    """

    # Safe defaults
    way_in_strategy = way_in_strategy or {}
    shared_contexts = shared_contexts or []
    engagement_signals = engagement_signals or []
    connector_data = connector_data or {}
    opportunity_data = opportunity_data or {}

    message_type = LinkedInMessageType.OPEN_INQUIRY
    subject_line = "Quick note on mutual interests"
    message_body = ""
    tone_notes = "Professional, concise, genuine interest."

    # Determine message type and build custom template
    primary_signal = _sanitize_template_value(
        way_in_strategy.get("primary_signal"),
        fallback="no_signal"
    )

    # CASE 1: Connector pathway
    if primary_signal == "connector" and connector_data:
        best_connector = connector_data.get("best_connector", {})
        connector_name = _sanitize_template_value(
            best_connector.get("person_name"),
            fallback="your colleague"
        )
        target_person = opportunity_data.get("hiring_contact", {})
        target_name = _sanitize_template_value(target_person.get("name"), fallback="there")
        relationship = _sanitize_template_value(
            best_connector.get("relationship_to_candidate", "connection")
        )
        core_focus = _sanitize_template_value(
            opportunity_data.get("core_focus", "your focus")
        )
        
        # Build warm intro template
        message_type = LinkedInMessageType.WARM_CONNECTOR
        subject_line = f"Introduction from {connector_name}"
        
        message_body = f"""Hi {target_name},

{connector_name} suggested I reach out — {relationship} and they know your work.

I'm genuinely interested in what you're building at {opportunity_title}. My background aligns particularly with {core_focus}.

Would you have 15 minutes to chat?

{candidate_name}"""
        
        tone_notes = "Warm, brief, credible. They already have a reason to trust you."

    # CASE 2: Engagement follow-up
    elif primary_signal == "engagement" and engagement_signals:
        engagement = engagement_signals[0]
        person_name = _sanitize_template_value(
            engagement.get("person_name"),
            fallback="there"
        )
        interaction_detail = _sanitize_template_value(
            engagement.get("interaction_detail"),
            fallback="your recent work"
        )
        
        message_type = LinkedInMessageType.ENGAGEMENT_FOLLOW_UP
        subject_line = f"Continuing the {opportunity_title} conversation"
        
        core_focus = _sanitize_template_value(
            opportunity_data.get("core_focus", "this domain")
        )
        message_body = f"""Hi {person_name},

Saw that you {interaction_detail} — that resonated with me.

I've been working on similar challenges in {core_focus} and noticed some parallels with your approach.

Would love to hear your perspective on [specific technical detail]. Are you open to a quick chat?

{candidate_name}"""
        
        tone_notes = "Peer-to-peer, technical, curious. They already know you exist."

    # CASE 3: Shared context
    elif primary_signal == "shared_context" and shared_contexts:
        context = shared_contexts[0] if isinstance(shared_contexts, list) else {}
        context_name = _sanitize_template_value(context.get("name"), fallback="our community")
        context_type = _sanitize_template_value(context.get("context_type"), fallback="event")
        
        message_type = LinkedInMessageType.SHARED_CONTEXT
        subject_line = f"{context_name} + {opportunity_title} intersection"
        
        if context_type == "hackathon":
            core_focus = _sanitize_template_value(
                opportunity_data.get("core_focus", "related technologies")
            )
            message_body = f"""Hi there,

We both participated in {context_name} — I was really impressed with {opportunity_title}'s approach to [domain].

Since then, I've been diving deeper into {core_focus}. I'd love to learn more about your perspective on this.

Open to a quick conversation?

{candidate_name}"""
        else:
            message_body = f"""Hi there,

We're both part of {context_name}, and I've been following {opportunity_title}'s work with interest.

My recent projects align closely with what you're building. Would you be open to a brief chat?

{candidate_name}"""
        
        tone_notes = "Community-first, authentic. Shared spaces reduce cold-contact friction."

    # CASE 4: Fallback - Open inquiry
    else:
        message_type = LinkedInMessageType.OPEN_INQUIRY
        subject_line = f"{opportunity_title} + your engineering approach"
        
        target_person = opportunity_data.get("hiring_contact", {})
        target_name = _sanitize_template_value(target_person.get("name"), fallback="there")
        core_focus = _sanitize_template_value(
            opportunity_data.get("core_focus", "your technical approach")
        )
        relevant_domain = _sanitize_template_value(
            opportunity_data.get("relevant_domain", "related domains")
        )
        
        message_body = f"""Hi {target_name},

I've been following {opportunity_title}'s engineering blog and {core_focus}.

My background in {relevant_domain} gives me a strong perspective on this.

Curious if there's a fit to chat?

{candidate_name}"""
        
        tone_notes = "Respectful, research-backed. Keep it brief and authentic."

    # Clean up message body (remove extra whitespace, ensure safety)
    message_body = " ".join(message_body.split()).strip()

    # Ensure message_body never exceeds practical LinkedIn limits
    max_chars = 1500
    if len(message_body) > max_chars:
        message_body = message_body[:max_chars].rsplit(" ", 1)[0] + "..."

    return LinkedInDMTemplate(
        message_type=message_type,
        subject_line=subject_line,
        message_body=message_body,
        tone_notes=tone_notes,
        character_count=len(message_body)
    )
