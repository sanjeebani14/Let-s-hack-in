"""
Agent 5 — Action Generator + Outreach Agent

Converts raw technical alignment data and human pathways into concrete tactical
plans and highly customized communications outreach templates.

Components:
  - instructions: Generates 2-3 concrete tactical instructions
  - linkedin_templates: Creates hyper-personalized LinkedIn DMs
  - email_templates: Formulates complete email packages with strong CTAs
  - attachment: Integrates proof cards into outreach templates
  - assembler: Combines all components into unified OutreachPackage
"""

# Instructions exports
from .instructions import (
    TacticalInstruction,
    ActionInstructions,
    InstructionCategory,
    generate_action_instructions,
)

# LinkedIn templates exports
from .linkedin_templates import (
    LinkedInMessageType,
    LinkedInDMTemplate,
    generate_linkedin_dm,
)

# Email templates exports
from .email_templates import (
    EmailCTAType,
    EmailVariant,
    ColdEmailPackage,
    generate_cold_email,
)

# Attachment exports
from .attachment import (
    ProofAttachmentType,
    ProofAttachment,
    AttachedProofCard,
    attach_proof_to_proof_card,
    integrate_proof_into_linkedin_dm,
    integrate_proof_into_email,
)

# Assembler exports
from .assembler import (
    OutreachPackage,
    AssemblyValidationResult,
    assemble_outreach_package,
)

__all__ = [
    # Instructions
    "TacticalInstruction",
    "ActionInstructions",
    "InstructionCategory",
    "generate_action_instructions",
    # LinkedIn
    "LinkedInMessageType",
    "LinkedInDMTemplate",
    "generate_linkedin_dm",
    # Email
    "EmailCTAType",
    "EmailVariant",
    "ColdEmailPackage",
    "generate_cold_email",
    # Attachment
    "ProofAttachmentType",
    "ProofAttachment",
    "AttachedProofCard",
    "attach_proof_to_proof_card",
    "integrate_proof_into_linkedin_dm",
    "integrate_proof_into_email",
    # Assembler
    "OutreachPackage",
    "AssemblyValidationResult",
    "assemble_outreach_package",
]
