"""
Cold Email Generator

Formulates complete email packages with impactful subject lines,
customized body text using shared community context, and explicit low-friction CTAs.

Optimized for high open rates and response engagement.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum


class EmailCTAType(str, Enum):
    """Types of call-to-action structures."""
    MEETING_REQUEST = "meeting_request"          # "Would you have 15 minutes?"
    RESPONSE_REQUEST = "response_request"        # "Thoughts on this approach?"
    INFORMATION_REQUEST = "information_request"  # "Love to learn more"
    COLLABORATION_INQUIRY = "collaboration_inquiry"  # "Potential collaboration angle?"


class EmailVariant(BaseModel):
    """Single email variant (A/B test option)."""
    variant_name: str = Field(
        ...,
        description="Variant identifier: 'A', 'B', etc.",
        examples=["A", "B"]
    )
    subject_line: str = Field(
        ...,
        description="Email subject line (40-60 characters optimal)",
        examples=["Re: Your PyTorch optimization approach"]
    )
    body: str = Field(
        ...,
        description="Email body (150-250 words, conversational tone)"
    )
    cta_type: EmailCTAType = Field(
        ...,
        description="Type of call-to-action"
    )
    estimated_read_time_seconds: int = Field(
        ...,
        description="Estimated time to read full email",
        examples=[30, 45, 60]
    )


class ColdEmailPackage(BaseModel):
    """Complete cold email package with variants."""
    opportunity_title: str = Field(
        ...,
        description="Target opportunity/company"
    )
    recipient_name: str = Field(
        ...,
        description="Recipient's name (or 'there' if unknown)"
    )
    primary_email: EmailVariant = Field(
        ...,
        description="Primary email variant (most personalized)"
    )
    variant_b: Optional[EmailVariant] = Field(
        default=None,
        description="Alternative email variant for A/B testing"
    )
    sending_notes: str = Field(
        ...,
        description="Notes on sending: best time, frequency, follow-up strategy",
        examples=["Send Tuesday-Thursday, 9am-11am PT. Follow up after 5 days if no response."]
    )
    context_bridges_included: List[str] = Field(
        ...,
        description="List of context bridges used in the email",
        examples=["shared hackathon", "open-source repo", "engineering blog"]
    )


def _sanitize_email_value(value: Any, fallback: str = "") -> str:
    """
    Safely extract string values for email templates.
    Prevents null injection and HTML/script issues.
    """
    if value is None:
        return fallback
    if isinstance(value, dict):
        for key in ["value", "name", "text", "title"]:
            if key in value:
                return str(value[key]).strip()
        return fallback
    if isinstance(value, (list, tuple)):
        return str(value[0]).strip() if value else fallback
    
    text = str(value).strip()
    # Remove any HTML/script tags
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text if text else fallback


def _build_context_opener(
    shared_contexts: List[Dict[str, Any]],
    engagement_signals: List[Dict[str, Any]],
    opportunity_data: Dict[str, Any]
) -> tuple[str, List[str]]:
    """
    Build opening paragraph using context bridges.

    Returns:
        (opener_paragraph, list_of_bridges_used)
    """
    bridges_used = []
    opener = ""

    # Priority 1: Shared context (hackathon, community, conference)
    if shared_contexts:
        context = shared_contexts[0] if isinstance(shared_contexts, list) else {}
        context_name = _sanitize_email_value(context.get("name"), "our community")
        context_type = _sanitize_email_value(context.get("context_type"), "event")
        
        if context_type == "hackathon":
            opener = f"I was impressed by {_sanitize_email_value(opportunity_data.get('opportunity_title'), opportunity_data.get('company_name', 'your team'))}'s work when we both participated in {context_name}."
            bridges_used.append("shared hackathon")
        elif context_type == "opensource":
            opener = f"I've been following your contributions to the {context_name} project. Your recent commits on {_sanitize_email_value(opportunity_data.get('core_focus', 'this area'))} caught my attention."
            bridges_used.append("open-source repo")
        elif context_type == "community":
            opener = f"We're both part of {context_name}, and I've been impressed with {_sanitize_email_value(opportunity_data.get('opportunity_title'), 'your')} recent technical depth."
            bridges_used.append("community connection")
        else:  # conference
            opener = f"I attended your talk at {context_name} on {_sanitize_email_value(opportunity_data.get('talk_topic'), 'engineering challenges')}, and I've been thinking about the insights ever since."
            bridges_used.append("conference talk")

    # Priority 2: Engagement signal (they interacted with your work)
    elif engagement_signals:
        engagement = engagement_signals[0]
        person_name = _sanitize_email_value(engagement.get("person_name"), "the team")
        interaction = _sanitize_email_value(engagement.get("interaction_detail"), "your work")
        
        opener = f"Saw that {person_name} {interaction} — that was great to see. It confirmed what I've been thinking about our approach to {_sanitize_email_value(opportunity_data.get('core_focus', 'these challenges'))}."
        bridges_used.append("mutual interest")

    # Priority 3: Company/domain expertise (fallback)
    else:
        company_name = _sanitize_email_value(opportunity_data.get("company_name"), "your company")
        opener = f"I've been following {company_name}'s engineering blog, especially the recent post on {_sanitize_email_value(opportunity_data.get('featured_blog_topic'), 'architecture challenges')}."
        bridges_used.append("engineering blog")

    return opener, bridges_used


def _build_cta_close(
    cta_type: EmailCTAType,
    candidate_name: str,
    opportunity_title: str
) -> str:
    """Build call-to-action closing based on CTA type."""
    
    base_close_template = "\n\nBest,\n{name}"

    if cta_type == EmailCTAType.MEETING_REQUEST:
        cta = f"Would you have 15 minutes for a quick call next week? I'd love to discuss your approach to {opportunity_title}."
    elif cta_type == EmailCTAType.RESPONSE_REQUEST:
        cta = f"Curious about your thoughts on this angle. Do you have a few minutes to chat?"
    elif cta_type == EmailCTAType.INFORMATION_REQUEST:
        cta = f"I'd love to learn more about how you're tackling this at {opportunity_title}."
    elif cta_type == EmailCTAType.COLLABORATION_INQUIRY:
        cta = f"I see a potential collaboration angle here — would you be open to exploring it?"
    else:
        cta = f"Would appreciate your insights on this. Open to a quick chat?"

    return cta + base_close_template.format(name=candidate_name)


def generate_cold_email(
    opportunity_title: str,
    recipient_name: str,
    candidate_name: str,
    shared_contexts: Optional[List[Dict[str, Any]]] = None,
    engagement_signals: Optional[List[Dict[str, Any]]] = None,
    proof_card: Optional[Dict[str, Any]] = None,
    opportunity_data: Optional[Dict[str, Any]] = None,
    inroad_score: float = 0.0,
    include_variant_b: bool = True,
) -> ColdEmailPackage:
    """
    Generate complete cold email package with primary and variant.

    Args:
        opportunity_title: Target opportunity/company
        recipient_name: Name of recipient (e.g., "Sarah Chen" or "there")
        candidate_name: Full name of candidate
        shared_contexts: List of shared touchpoints
        engagement_signals: Employee engagement with candidate's work
        proof_card: Proof Card from Agent 4
        opportunity_data: Full opportunity metadata
        inroad_score: InRoad Chemistry score
        include_variant_b: Whether to generate A/B test variant

    Returns:
        ColdEmailPackage: Complete email with variants
    """

    # Safe defaults
    shared_contexts = shared_contexts or []
    engagement_signals = engagement_signals or []
    proof_card = proof_card or {}
    opportunity_data = opportunity_data or {}

    # Build opening using context bridges
    opener, bridges_used = _build_context_opener(
        shared_contexts,
        engagement_signals,
        opportunity_data
    )

    # Determine primary CTA type based on inroad score
    if inroad_score >= 75:
        primary_cta = EmailCTAType.MEETING_REQUEST
    elif inroad_score >= 60:
        primary_cta = EmailCTAType.RESPONSE_REQUEST
    elif inroad_score >= 45:
        primary_cta = EmailCTAType.INFORMATION_REQUEST
    else:
        primary_cta = EmailCTAType.COLLABORATION_INQUIRY

    # Extract core focus for body context
    core_focus = _sanitize_email_value(
        opportunity_data.get("core_focus", "engineering challenges"),
        "engineering challenges"
    )

    # Get top proof-backed skill for credibility
    proof_claim = ""
    matched_skills = proof_card.get("matched_skills", [])
    if matched_skills:
        top_skill = matched_skills[0]
        skill_name = _sanitize_email_value(top_skill.get("skill_name"), "my expertise")
        evidence = _sanitize_email_value(
            top_skill.get("best_project_evidence", "relevant experience"),
            "relevant experience"
        )
        proof_claim = f" My background in {skill_name} ({evidence}) gives me solid perspective here."

    # Build primary email body
    primary_body = f"""{opener}

What stood out was the technical depth around {core_focus}.{proof_claim}

I think there's real alignment between how I approach these problems and what you're building.

{_build_cta_close(primary_cta, candidate_name, opportunity_title)}"""

    # Clean and validate body
    primary_body = " ".join(primary_body.split()).strip()
    if len(primary_body) > 2000:
        primary_body = primary_body[:2000].rsplit(" ", 1)[0] + "…"

    # Primary subject line
    primary_subject = _build_primary_subject(
        opportunity_title,
        core_focus,
        bridges_used,
        inroad_score
    )

    primary_email = EmailVariant(
        variant_name="A",
        subject_line=primary_subject,
        body=primary_body,
        cta_type=primary_cta,
        estimated_read_time_seconds=45 if len(primary_body) > 300 else 30
    )

    # Build variant B (alternative angle)
    variant_b = None
    if include_variant_b:
        variant_b_cta = (
            EmailCTAType.COLLABORATION_INQUIRY
            if primary_cta == EmailCTAType.MEETING_REQUEST
            else EmailCTAType.MEETING_REQUEST
        )
        
        variant_b_subject = _build_variant_subject(
            opportunity_title,
            core_focus,
            bridges_used
        )
        
        variant_b_body = f"""Hi {recipient_name},

I've been diving into {core_focus} lately, and your team's approach resonates with me.{proof_claim}

Quick thought: [specific insight about their work]. Happy to elaborate if interesting.

{_build_cta_close(variant_b_cta, candidate_name, opportunity_title)}"""

        variant_b_body = " ".join(variant_b_body.split()).strip()
        if len(variant_b_body) > 2000:
            variant_b_body = variant_b_body[:2000].rsplit(" ", 1)[0] + "…"

        variant_b = EmailVariant(
            variant_name="B",
            subject_line=variant_b_subject,
            body=variant_b_body,
            cta_type=variant_b_cta,
            estimated_read_time_seconds=35
        )

    sending_notes = _get_sending_strategy(inroad_score)

    return ColdEmailPackage(
        opportunity_title=opportunity_title,
        recipient_name=recipient_name,
        primary_email=primary_email,
        variant_b=variant_b,
        sending_notes=sending_notes,
        context_bridges_included=bridges_used
    )


def _build_primary_subject(
    opportunity_title: str,
    core_focus: str,
    bridges_used: List[str],
    inroad_score: float
) -> str:
    """Build strong primary subject line."""
    
    # Use highest-value bridge in subject
    bridge_ref = ""
    if bridges_used:
        if "hackathon" in bridges_used[0]:
            bridge_ref = "From [hackathon] — "
        elif "open-source" in bridges_used[0]:
            bridge_ref = "PyTorch contributor here — "
        elif "community" in bridges_used[0]:
            bridge_ref = "[Community member] — "
        elif "engineering blog" in bridges_used[0]:
            bridge_ref = "Re: Your recent post — "

    core_ref = core_focus[:30] if len(core_focus) > 30 else core_focus

    # Optimal length: 40-60 characters
    subject = f"{bridge_ref}Your {opportunity_title} approach"
    if len(subject) > 60:
        subject = subject[:57] + "…"

    return subject


def _build_variant_subject(
    opportunity_title: str,
    core_focus: str,
    bridges_used: List[str]
) -> str:
    """Build alternative subject line for variant B."""
    
    subjects = [
        f"Quick thought on {core_focus}",
        f"Thinking about your {opportunity_title} work",
        f"Alignment on {core_focus}?",
        f"Re: {core_focus} challenges",
    ]

    return subjects[len(bridges_used) % len(subjects)]


def _get_sending_strategy(inroad_score: float) -> str:
    """Get sending recommendations based on score."""
    
    if inroad_score >= 80:
        return "High confidence match. Send immediately. Follow up after 5 days if no response. Try variant B after 1 week."
    elif inroad_score >= 60:
        return "Good fit. Send Tuesday-Thursday 9-11am PT. Follow up after 1 week. A/B test both variants before next cycle."
    elif inroad_score >= 40:
        return "Moderate fit. Send once, but prioritize higher-scoring opportunities first. One follow-up after 1 week."
    else:
        return "Lower priority. Send alongside higher-confidence prospects. Expect lower response rate."
