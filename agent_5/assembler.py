"""
Outreach Package Assembler

Master module that combines:
  - Action instructions (Agent 5)
  - LinkedIn DM templates
  - Cold email package
  - Proof card attachments

Into a unified OutreachPackage payload per opportunity.
Ensures robust null-safety and template validation before delivery.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

def _get_iso_timestamp():
    """Generate ISO8601 timestamp."""
    return datetime.utcnow().isoformat() + "Z"

from .instructions import ActionInstructions, generate_action_instructions
from .linkedin_templates import LinkedInDMTemplate, generate_linkedin_dm
from .email_templates import ColdEmailPackage, generate_cold_email
from .attachment import AttachedProofCard, attach_proof_to_proof_card
from .attachment import integrate_proof_into_linkedin_dm, integrate_proof_into_email


class OutreachPackage(BaseModel):
    """Complete outreach payload for a single opportunity."""
    
    # Metadata
    opportunity_title: str = Field(
        ...,
        description="Target opportunity/company name"
    )
    candidate_name: str = Field(
        ...,
        description="Name of candidate"
    )
    generated_timestamp: str = Field(
        default_factory=_get_iso_timestamp,
        description="ISO8601 timestamp when package was generated"
    )
    inroad_score: float = Field(
        ...,
        description="InRoad Chemistry score from Agent 3 (0-100)",
        ge=0.0,
        le=100.0
    )
    
    # Components
    action_instructions: ActionInstructions = Field(
        ...,
        description="2-3 tactical instructions for prep"
    )
    linkedin_outreach: LinkedInDMTemplate = Field(
        ...,
        description="Customized LinkedIn DM message"
    )
    email_outreach: ColdEmailPackage = Field(
        ...,
        description="Cold email package with variants"
    )
    proof_attachment: AttachedProofCard = Field(
        ...,
        description="Evidence-backed skill proof"
    )
    
    # Integration
    enriched_linkedin_message: str = Field(
        ...,
        description="LinkedIn message with proof integrated"
    )
    enriched_email_primary: str = Field(
        ...,
        description="Primary email with proof integrated"
    )
    
    # Validation
    safety_checks_passed: bool = Field(
        ...,
        description="All null-safety and template validation checks passed"
    )
    validation_notes: List[str] = Field(
        default=[],
        description="Notes from validation process"
    )
    
    # Recommended execution
    recommended_order: List[str] = Field(
        ...,
        description="Recommended sequence: action_instructions, linkedin, email",
        examples=[["action_instructions", "linkedin", "email_followup"]]
    )
    estimated_total_time_minutes: int = Field(
        ...,
        description="Total time to execute full package"
    )
    
    
    @validator("inroad_score")
    def validate_score(cls, v):
        """Ensure score is in valid range."""
        if not (0.0 <= v <= 100.0):
            raise ValueError("InRoad score must be between 0-100")
        return round(v, 1)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export as JSON-safe dictionary."""
        return json.loads(self.model_dump_json())
    
    def to_json(self) -> str:
        """Export as formatted JSON."""
        return self.model_dump_json(indent=2)


class AssemblyValidationResult(BaseModel):
    """Result of assembly validation."""
    is_valid: bool = Field(
        ...,
        description="Whether assembly passed all checks"
    )
    errors: List[str] = Field(
        default=[],
        description="List of validation errors"
    )
    warnings: List[str] = Field(
        default=[],
        description="Non-fatal warnings"
    )
    checks_performed: Dict[str, bool] = Field(
        ...,
        description="Individual check results"
    )


def _safe_get_nested(obj: Any, *keys: str, default: Any = None) -> Any:
    """Safely navigate nested dict/object structures."""
    for key in keys:
        if isinstance(obj, dict):
            obj = obj.get(key)
        elif hasattr(obj, key):
            obj = getattr(obj, key, None)
        else:
            return default
        if obj is None:
            return default
    return obj


def _validate_outreach_components(
    action_instructions: ActionInstructions,
    linkedin_dm: LinkedInDMTemplate,
    email_pkg: ColdEmailPackage,
    proof_attachment: AttachedProofCard
) -> AssemblyValidationResult:
    """
    Validate all components for safety and integrity.

    Returns:
        AssemblyValidationResult with detailed validation info
    """
    errors = []
    warnings = []
    checks = {
        "action_instructions_valid": False,
        "linkedin_dm_valid": False,
        "email_package_valid": False,
        "proof_attachment_valid": False,
        "all_null_safe": False,
        "message_text_length_ok": False,
        "cta_present": False,
    }

    # Check 1: Action instructions
    try:
        if (
            hasattr(action_instructions, "instructions")
            and len(action_instructions.instructions) >= 2
            and len(action_instructions.instructions) <= 3
        ):
            checks["action_instructions_valid"] = True
        else:
            errors.append("Action instructions invalid: must have 2-3 items")
    except Exception as e:
        errors.append(f"Action instructions validation failed: {str(e)}")

    # Check 2: LinkedIn DM
    try:
        if (
            hasattr(linkedin_dm, "message_body")
            and len(_safe_get_nested(linkedin_dm, "message_body", default="")) > 20
            and hasattr(linkedin_dm, "subject_line")
        ):
            checks["linkedin_dm_valid"] = True
        else:
            errors.append("LinkedIn DM invalid: missing required fields or content too short")
    except Exception as e:
        errors.append(f"LinkedIn DM validation failed: {str(e)}")

    # Check 3: Email package
    try:
        primary_email = _safe_get_nested(email_pkg, "primary_email")
        if (
            primary_email
            and hasattr(primary_email, "body")
            and len(primary_email.body) > 50
            and hasattr(primary_email, "subject_line")
            and len(primary_email.subject_line) > 10
        ):
            checks["email_package_valid"] = True
        else:
            errors.append("Email package invalid: primary email incomplete")
    except Exception as e:
        errors.append(f"Email package validation failed: {str(e)}")

    # Check 4: Proof attachment
    try:
        if (
            hasattr(proof_attachment, "primary_proof_attachment")
            and hasattr(proof_attachment, "email_body_attachment_snippet")
            and len(proof_attachment.email_body_attachment_snippet) > 10
        ):
            checks["proof_attachment_valid"] = True
        else:
            errors.append("Proof attachment invalid: missing content")
    except Exception as e:
        errors.append(f"Proof attachment validation failed: {str(e)}")

    # Check 5: Null safety
    try:
        null_unsafe = False
        
        for component in [action_instructions, linkedin_dm, email_pkg, proof_attachment]:
            if component is None:
                null_unsafe = True
                break
        
        if not null_unsafe:
            checks["all_null_safe"] = True
    except Exception as e:
        errors.append(f"Null safety check failed: {str(e)}")

    # Check 6: Message length
    try:
        linkedin_len = len(_safe_get_nested(linkedin_dm, "message_body", default=""))
        email_len = len(_safe_get_nested(email_pkg, "primary_email", "body", default=""))
        
        if 20 < linkedin_len < 2000 and 50 < email_len < 3000:
            checks["message_text_length_ok"] = True
        else:
            warnings.append(f"Message lengths unusual: LinkedIn {linkedin_len}, Email {email_len}")
    except Exception as e:
        errors.append(f"Message length check failed: {str(e)}")

    # Check 7: CTA present
    try:
        email_body = _safe_get_nested(email_pkg, "primary_email", "body", default="")
        cta_phrases = ["would", "should", "can", "happy", "open", "interested", "chat", "call", "meet"]
        
        if any(phrase in email_body.lower() for phrase in cta_phrases):
            checks["cta_present"] = True
        else:
            warnings.append("Email may lack clear call-to-action")
    except Exception as e:
        errors.append(f"CTA check failed: {str(e)}")

    is_valid = len(errors) == 0 and all(checks.values())

    return AssemblyValidationResult(
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        checks_performed=checks
    )


def assemble_outreach_package(
    opportunity_title: str,
    candidate_name: str,
    inroad_score: float,
    way_in_strategy: Optional[Dict[str, Any]] = None,
    shared_contexts: Optional[List[Dict[str, Any]]] = None,
    engagement_signals: Optional[List[Dict[str, Any]]] = None,
    connector_data: Optional[Dict[str, Any]] = None,
    proof_card: Optional[Dict[str, Any]] = None,
    opportunity_data: Optional[Dict[str, Any]] = None,
) -> OutreachPackage:
    """
    Master assembly function combining all Agent 5 components.

    Args:
        opportunity_title: Target opportunity/company
        candidate_name: Candidate full name
        inroad_score: InRoad Chemistry score (0-100) from Agent 3
        way_in_strategy: Entry strategy from Agent 3
        shared_contexts: Shared contexts from Agent 3
        engagement_signals: Engagement signals from Agent 3
        connector_data: Connector person data from Agent 3
        proof_card: Proof Card from Agent 4
        opportunity_data: Full opportunity metadata

    Returns:
        OutreachPackage: Complete outreach payload, validated and safe
    """

    # Safe defaults
    way_in_strategy = way_in_strategy or {}
    shared_contexts = shared_contexts or []
    engagement_signals = engagement_signals or []
    connector_data = connector_data or {}
    proof_card = proof_card or {}
    opportunity_data = opportunity_data or {}

    validation_notes = []

    # STEP 1: Generate action instructions
    try:
        action_instructions = generate_action_instructions(
            opportunity_title=opportunity_title,
            inroad_score=inroad_score,
            way_in_strategy=way_in_strategy,
            shared_contexts=shared_contexts,
            engagement_signals=engagement_signals,
            connector_data=connector_data,
            proof_card=proof_card,
            opportunity_data=opportunity_data,
        )
        validation_notes.append("✓ Action instructions generated")
    except Exception as e:
        validation_notes.append(f"⚠ Action instructions generation failed: {str(e)}")
        action_instructions = ActionInstructions(
            opportunity_title=opportunity_title,
            instructions=[],
            priority_sequence=[],
            estimated_prep_time_minutes=15
        )

    # STEP 2: Generate LinkedIn DM
    try:
        linkedin_dm = generate_linkedin_dm(
            opportunity_title=opportunity_title,
            candidate_name=candidate_name,
            way_in_strategy=way_in_strategy,
            shared_contexts=shared_contexts,
            engagement_signals=engagement_signals,
            connector_data=connector_data,
            inroad_score=inroad_score,
            opportunity_data=opportunity_data,
        )
        validation_notes.append("✓ LinkedIn DM generated")
    except Exception as e:
        validation_notes.append(f"⚠ LinkedIn DM generation failed: {str(e)}")
        linkedin_dm = LinkedInDMTemplate(
            message_type="open_inquiry",
            subject_line="Quick note",
            message_body=f"Hi there, interested in discussing opportunities at {opportunity_title}.",
            tone_notes="Professional",
            character_count=0
        )

    # STEP 3: Generate cold email package
    try:
        email_pkg = generate_cold_email(
            opportunity_title=opportunity_title,
            recipient_name=_safe_get_nested(
                opportunity_data,
                "hiring_contact",
                "name",
                default="there"
            ),
            candidate_name=candidate_name,
            shared_contexts=shared_contexts,
            engagement_signals=engagement_signals,
            proof_card=proof_card,
            opportunity_data=opportunity_data,
            inroad_score=inroad_score,
            include_variant_b=True,
        )
        validation_notes.append("✓ Cold email package generated")
    except Exception as e:
        validation_notes.append(f"⚠ Cold email generation failed: {str(e)}")
        email_pkg = ColdEmailPackage(
            opportunity_title=opportunity_title,
            recipient_name="there",
            primary_email=None,
            variant_b=None,
            sending_notes="Manual creation recommended",
            context_bridges_included=[]
        )

    # STEP 4: Create proof attachment
    try:
        proof_attachment = attach_proof_to_proof_card(
            opportunity_title=opportunity_title,
            proof_card=proof_card,
            matched_skills=_safe_get_nested(proof_card, "matched_skills"),
        )
        validation_notes.append("✓ Proof attachment created")
    except Exception as e:
        validation_notes.append(f"⚠ Proof attachment creation failed: {str(e)}")
        proof_attachment = AttachedProofCard(
            opportunity_title=opportunity_title,
            primary_proof_attachment=None,
            secondary_proof_attachments=[],
            linkedin_dm_attachment_snippet="Relevant experience",
            email_body_attachment_snippet="Relevant experience",
            signature_proof_line=None,
            attachment_integrity_check=False
        )

    # STEP 5: Validate all components
    try:
        validation = _validate_outreach_components(
            action_instructions,
            linkedin_dm,
            email_pkg,
            proof_attachment
        )
        validation_notes.extend([f"[{k}]: {v}" for k, v in validation.checks_performed.items()])
        validation_notes.extend(validation.errors)
        validation_notes.extend(validation.warnings)
        safety_checks_passed = validation.is_valid
    except Exception as e:
        validation_notes.append(f"⚠ Validation failed: {str(e)}")
        safety_checks_passed = False

    # STEP 6: Integrate proof into messages
    try:
        enriched_linkedin = integrate_proof_into_linkedin_dm(
            _safe_get_nested(linkedin_dm, "message_body", default="Hi there, interested in discussing."),
            proof_attachment
        )
    except Exception as e:
        enriched_linkedin = _safe_get_nested(linkedin_dm, "message_body", default="")
        validation_notes.append(f"⚠ LinkedIn proof integration failed: {str(e)}")

    try:
        enriched_email = integrate_proof_into_email(
            _safe_get_nested(email_pkg, "primary_email", "body", default="Hi there,"),
            proof_attachment
        )
    except Exception as e:
        enriched_email = _safe_get_nested(email_pkg, "primary_email", "body", default="")
        validation_notes.append(f"⚠ Email proof integration failed: {str(e)}")

    # STEP 7: Calculate recommended order and timing
    recommended_order = []
    total_time = 0

    if action_instructions and hasattr(action_instructions, "instructions"):
        recommended_order.append("action_instructions")
        total_time += _safe_get_nested(action_instructions, "estimated_prep_time_minutes", default=15)

    if linkedin_dm:
        recommended_order.append("linkedin")
        total_time += 5  # Time to send LinkedIn message

    if email_pkg:
        recommended_order.append("email_followup")
        total_time += 10  # Time to send email

    # Create final OutreachPackage
    package = OutreachPackage(
        opportunity_title=opportunity_title,
        candidate_name=candidate_name,
        inroad_score=inroad_score,
        action_instructions=action_instructions,
        linkedin_outreach=linkedin_dm,
        email_outreach=email_pkg,
        proof_attachment=proof_attachment,
        enriched_linkedin_message=enriched_linkedin,
        enriched_email_primary=enriched_email,
        safety_checks_passed=safety_checks_passed,
        validation_notes=validation_notes,
        recommended_order=recommended_order,
        estimated_total_time_minutes=max(15, total_time),
    )

    return package
