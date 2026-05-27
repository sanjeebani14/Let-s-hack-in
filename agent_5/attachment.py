"""
Proof Card Attachment Logic

Ingests the Proof Card from Agent 4 and stitches evidence context directly
into LinkedIn DM and email templates. Ensures at least one core engineering
skill is supported by explicit numerical or narrative proof.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum


class ProofAttachmentType(str, Enum):
    """How proof is attached to communication."""
    INLINE_NARRATIVE = "inline_narrative"    # Woven into message body
    SIGNATURE_LINK = "signature_link"        # Attached as link in signature
    SUPPORTING_DOCUMENT = "supporting_document"  # Separate attachment reference
    REFERENCED_CLAIM = "referenced_claim"   # Specific claim with evidence


class ProofAttachment(BaseModel):
    """Container for proof-backed claim."""
    skill_name: str = Field(
        ...,
        description="Technical skill being proven"
    )
    confidence_score: float = Field(
        ...,
        description="Agent 4 confidence score (0-100)"
    )
    evidence_snippet: str = Field(
        ...,
        description="Specific project evidence (150 chars max)",
        examples=[
            "Led Python microservice handling 50k req/s with 99.9% uptime",
            "Optimized React component rendering, reducing load time 65%"
        ]
    )
    evidence_source: str = Field(
        ...,
        description="Where evidence comes from: 'portfolio', 'github', 'blog', 'open_source'",
        examples=["portfolio", "github", "blog"]
    )
    attachment_type: ProofAttachmentType = Field(
        ...,
        description="How this proof is incorporated"
    )
    attachment_text: str = Field(
        ...,
        description="Actual text/link to incorporate into message"
    )


class AttachedProofCard(BaseModel):
    """Proof card enriched with attachment metadata."""
    opportunity_title: str = Field(
        ...,
        description="Target opportunity"
    )
    primary_proof_attachment: ProofAttachment = Field(
        ...,
        description="Main skill being proven (strongest evidence)"
    )
    secondary_proof_attachments: List[ProofAttachment] = Field(
        default=[],
        description="Optional supporting proofs"
    )
    linkedin_dm_attachment_snippet: str = Field(
        ...,
        description="Text snippet to weave into LinkedIn DM (1-2 sentences max)"
    )
    email_body_attachment_snippet: str = Field(
        ...,
        description="Text snippet to incorporate into email body (1-3 sentences)"
    )
    signature_proof_line: Optional[str] = Field(
        default=None,
        description="Optional line for email signature/footer"
    )
    attachment_integrity_check: bool = Field(
        ...,
        description="Verification that proof is specific and measurable (not vague)"
    )


def _extract_quantitative_proof(evidence_text: str) -> bool:
    """
    Check if evidence contains specific metrics (%, number, time, money).
    Returns True if quantitative signals found.
    """
    quantitative_patterns = [
        r'\d+%',      # Percentages (50%)
        r'\d+[kmgt]\+',  # Scale (10k, 1M)
        r'\d+\s*(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?)',  # Time
        r'\$\d+',     # Money
        r'\d+x',      # Multipliers
    ]
    
    import re
    for pattern in quantitative_patterns:
        if re.search(pattern, evidence_text, re.IGNORECASE):
            return True
    return False


def _sanitize_proof_value(value: Any, fallback: str = "") -> str:
    """Safely extract string from proof data."""
    if value is None:
        return fallback
    if isinstance(value, dict):
        for key in ["evidence", "text", "value", "snippet"]:
            if key in value:
                return str(value[key]).strip()
        return fallback
    return str(value).strip() if value else fallback


def attach_proof_to_proof_card(
    opportunity_title: str,
    proof_card: Optional[Dict[str, Any]] = None,
    matched_skills: Optional[List[Dict[str, Any]]] = None,
) -> AttachedProofCard:
    """
    Transform Proof Card into attachment-ready format with message integration.

    Args:
        opportunity_title: Target opportunity
        proof_card: Full Proof Card from Agent 4
        matched_skills: Top matched skills (can be extracted from proof_card if not provided)

    Returns:
        AttachedProofCard: Proof card with attachment metadata and message snippets
    """

    # Safe defaults
    proof_card = proof_card or {}
    
    if matched_skills is None:
        matched_skills = proof_card.get("matched_skills", [])
    
    if not matched_skills:
        # Fallback: Create minimal but valid proof
        primary_attachment = ProofAttachment(
            skill_name="Technical Expertise",
            confidence_score=50.0,
            evidence_snippet="Relevant project experience",
            evidence_source="portfolio",
            attachment_type=ProofAttachmentType.INLINE_NARRATIVE,
            attachment_text="I've worked on related challenges in this domain."
        )
        
        return AttachedProofCard(
            opportunity_title=opportunity_title,
            primary_proof_attachment=primary_attachment,
            secondary_proof_attachments=[],
            linkedin_dm_attachment_snippet="My background aligns with this work.",
            email_body_attachment_snippet="My experience in related projects gives me solid perspective.",
            signature_proof_line=None,
            attachment_integrity_check=False
        )

    # Extract primary proof (highest confidence)
    primary_skill = matched_skills[0]
    skill_name = _sanitize_proof_value(
        primary_skill.get("skill_name"),
        fallback="Technical Expertise"
    )
    confidence_score = float(primary_skill.get("confidence_score", 50.0))
    evidence_snippet = _sanitize_proof_value(
        primary_skill.get("best_project_evidence"),
        fallback="Relevant project experience"
    )

    # Determine evidence source heuristic
    evidence_source = "portfolio"
    if "github" in evidence_snippet.lower() or "repo" in evidence_snippet.lower():
        evidence_source = "github"
    elif "blog" in evidence_snippet.lower() or "article" in evidence_snippet.lower():
        evidence_source = "blog"
    elif "open" in evidence_snippet.lower():
        evidence_source = "open_source"

    # Determine attachment type based on confidence and evidence quality
    is_quantitative = _extract_quantitative_proof(evidence_snippet)
    
    if confidence_score >= 80 and is_quantitative:
        attachment_type = ProofAttachmentType.INLINE_NARRATIVE
    elif confidence_score >= 70:
        attachment_type = ProofAttachmentType.REFERENCED_CLAIM
    elif confidence_score >= 60:
        attachment_type = ProofAttachmentType.SIGNATURE_LINK
    else:
        attachment_type = ProofAttachmentType.SUPPORTING_DOCUMENT

    # Build attachment text
    if attachment_type == ProofAttachmentType.INLINE_NARRATIVE:
        attachment_text = f"My {skill_name} experience: {evidence_snippet}"
    elif attachment_type == ProofAttachmentType.REFERENCED_CLAIM:
        attachment_text = evidence_snippet
    elif attachment_type == ProofAttachmentType.SIGNATURE_LINK:
        attachment_text = f"See my {skill_name} work: [portfolio link]"
    else:
        attachment_text = evidence_snippet

    primary_attachment = ProofAttachment(
        skill_name=skill_name,
        confidence_score=confidence_score,
        evidence_snippet=evidence_snippet[:150],  # Enforce max length
        evidence_source=evidence_source,
        attachment_type=attachment_type,
        attachment_text=attachment_text
    )

    # Build secondary attachments (next best skills)
    secondary_attachments = []
    if len(matched_skills) > 1:
        for i, skill in enumerate(matched_skills[1:3]):  # Max 2 secondary
            sec_skill_name = _sanitize_proof_value(
                skill.get("skill_name"),
                fallback=f"Supporting Skill {i+1}"
            )
            sec_evidence = _sanitize_proof_value(
                skill.get("best_project_evidence"),
                fallback="Relevant experience"
            )
            sec_confidence = float(skill.get("confidence_score", 50.0))

            secondary_attachments.append(ProofAttachment(
                skill_name=sec_skill_name,
                confidence_score=sec_confidence,
                evidence_snippet=sec_evidence[:100],
                evidence_source="portfolio",
                attachment_type=ProofAttachmentType.SUPPORTING_DOCUMENT,
                attachment_text=sec_evidence
            ))

    # Build LinkedIn DM snippet (1-2 sentences, conversational)
    linkedin_snippet = f"I've been working on {skill_name} — specifically {evidence_snippet}"
    if len(linkedin_snippet) > 120:
        linkedin_snippet = linkedin_snippet[:117] + "…"

    # Build email body snippet (1-3 sentences, professional)
    if is_quantitative:
        email_snippet = f"My background in {skill_name} includes {evidence_snippet}. This aligns closely with your focus."
    else:
        email_snippet = f"I've built substantial experience in {skill_name}: {evidence_snippet}."

    if len(email_snippet) > 300:
        email_snippet = email_snippet[:297] + "…"

    # Build signature line (optional, for highly confident skills)
    signature_line = None
    if confidence_score >= 85:
        signature_line = f"{skill_name}: {evidence_snippet[:80]}"

    # Check integrity (is proof specific and measurable?)
    integrity_check = (
        len(evidence_snippet) > 20 and
        (is_quantitative or any(verb in evidence_snippet.lower() 
         for verb in ["led", "built", "architected", "designed", "implemented", "optimized"]))
    )

    return AttachedProofCard(
        opportunity_title=opportunity_title,
        primary_proof_attachment=primary_attachment,
        secondary_proof_attachments=secondary_attachments,
        linkedin_dm_attachment_snippet=linkedin_snippet,
        email_body_attachment_snippet=email_snippet,
        signature_proof_line=signature_line,
        attachment_integrity_check=integrity_check
    )


def integrate_proof_into_linkedin_dm(
    dm_message_body: str,
    attached_proof: AttachedProofCard
) -> str:
    """
    Weave proof card into LinkedIn DM message body.

    Args:
        dm_message_body: Original DM message
        attached_proof: AttachedProofCard with metadata

    Returns:
        Enriched DM message with proof integrated
    """
    
    if not attached_proof.attachment_integrity_check:
        # Proof not sufficiently specific, return original
        return dm_message_body

    # Insert proof snippet before CTA (usually before "Best," or "Thanks,")
    lines = dm_message_body.split("\n")
    
    # Find CTA line
    cta_index = len(lines)
    for i, line in enumerate(lines):
        if line.strip().startswith(("Best", "Thanks", "Cheers", "Regards")):
            cta_index = i
            break

    # Insert proof snippet 1-2 lines before CTA
    insertion_point = max(0, cta_index - 1)
    
    enriched_body = "\n".join(lines[:insertion_point])
    enriched_body += f"\n\n{attached_proof.linkedin_dm_attachment_snippet}"
    enriched_body += "\n\n" + "\n".join(lines[insertion_point:])

    return enriched_body.strip()


def integrate_proof_into_email(
    email_body: str,
    attached_proof: AttachedProofCard
) -> str:
    """
    Integrate proof evidence into email body.

    Args:
        email_body: Original email body
        attached_proof: AttachedProofCard with metadata

    Returns:
        Enriched email body with proof integrated
    """
    
    if not attached_proof.attachment_integrity_check:
        return email_body

    # Find position to insert (usually after second paragraph, before CTA)
    lines = email_body.split("\n\n")
    
    if len(lines) > 2:
        # Insert before signature section
        signature_start = len(lines)
        for i, line in enumerate(lines):
            if line.strip().startswith(("Best", "Thanks", "Cheers")):
                signature_start = i
                break

        # Insert evidence in new paragraph before signature
        lines.insert(signature_start, attached_proof.email_body_attachment_snippet)
        enriched = "\n\n".join(lines)
    else:
        # Short email, append before signature
        enriched = email_body.replace(
            "\n\nBest,",
            f"\n\n{attached_proof.email_body_attachment_snippet}\n\nBest,"
        )

    return enriched.strip()
