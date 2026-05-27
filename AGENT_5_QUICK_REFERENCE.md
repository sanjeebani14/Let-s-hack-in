"""
Agent 5 — Quick Reference Guide

Copy-paste ready examples and field reference for all main functions.
"""

# ============================================================================

# QUICK START (2 MINUTES)

# ============================================================================

## Import Everything

```python
from agent_5 import *

# Or import specific functions
from agent_5 import (
    generate_action_instructions,
    generate_linkedin_dm,
    generate_cold_email,
    attach_proof_to_proof_card,
    assemble_outreach_package,
)
```

## Generate Complete Outreach Package

```python
from agent_5 import assemble_outreach_package

package = assemble_outreach_package(
    opportunity_title="Senior ML Engineer",
    candidate_name="Jordan Lee",
    inroad_score=76.5,
    way_in_strategy={
        "actionable_sentence": "You both attended PyCon 2025",
        "primary_signal": "shared_context",
        "confidence": 0.88
    },
    shared_contexts=[
        {
            "context_type": "hackathon",
            "name": "PyCon 2025 ML Challenge",
            "relevance_score": 0.92
        }
    ],
    engagement_signals=[
        {
            "person_name": "Sarah Chen",
            "interaction_type": "github_star",
            "interaction_detail": "Starred your PyTorch repo",
            "interaction_date": "2026-05-18"
        }
    ],
    connector_data={
        "best_connector": {
            "person_name": "Maya Patel",
            "relationship_to_candidate": "worked together 2022-2024",
            "introduction_likelihood": 0.94
        }
    },
    proof_card={
        "matched_skills": [
            {
                "skill_name": "PyTorch Optimization",
                "confidence_score": 91.0,
                "best_project_evidence": "Led distributed training system, 3.2x speedup"
            }
        ]
    },
    opportunity_data={
        "company_name": "QuantumLeap AI",
        "core_focus": "scalable distributed ML infrastructure"
    }
)

# Use it
print(f"Time to execute: {package.estimated_total_time_minutes} min")
print(f"Safety: {'✓' if package.safety_checks_passed else '✗'}")
print(f"LinkedIn:\n{package.enriched_linkedin_message}")
print(f"Email:\n{package.enriched_email_primary}")
```

# ============================================================================

# INDIVIDUAL COMPONENTS (COPY-PASTE READY)

# ============================================================================

## 1. ACTION INSTRUCTIONS

### Basic Usage

```python
from agent_5 import generate_action_instructions

instructions = generate_action_instructions(
    opportunity_title="Senior ML Engineer",
    inroad_score=76.5,
    way_in_strategy={"primary_signal": "shared_context"},
    shared_contexts=[{"context_type": "hackathon", "name": "PyCon 2025"}],
    engagement_signals=[],
    connector_data={},
)

# Access results
for i, instr in enumerate(instructions.instructions, 1):
    print(f"{i}. {instr.instruction}")
    print(f"   Why: {instr.reasoning}")
    print(f"   When: {instr.time_frame}")
    print()
```

### Full Parameters

```python
ActionInstructions(
    opportunity_title="Senior ML Engineer",           # Required: target opportunity name
    instructions=[                                    # List of 2-3 TacticalInstructions
        {
            "instruction": str,                       # Exact action (specific, not generic)
            "category": str,                          # technical_contribution, shared_context_reference, etc.
            "reasoning": str,                         # Why this action matters
            "time_frame": str                         # "immediate" / "this_week" / "before_outreach"
        }
    ],
    priority_sequence=[1, 2, 3],                     # Execution order (1-indexed)
    estimated_prep_time_minutes=30                  # Total prep time
)
```

---

## 2. LINKEDIN DM

### Basic Usage

```python
from agent_5 import generate_linkedin_dm

dm = generate_linkedin_dm(
    opportunity_title="QuantumLeap AI",
    candidate_name="Jordan Lee",
    way_in_strategy={"primary_signal": "engagement"},
    engagement_signals=[{
        "person_name": "Sarah Chen",
        "interaction_detail": "Starred your repo"
    }],
)

print(f"Subject: {dm.subject_line}")
print(f"---")
print(dm.message_body)
print(f"---")
print(f"Tone: {dm.tone_notes}")
```

### Full Parameters

```python
LinkedInDMTemplate(
    message_type="warm_connector",                   # Message type enum
    subject_line="Quick note on mutual interests",   # 30-60 characters optimal
    message_body="""Hi Sarah,

I noticed you starred our distributed training repo — that was great to see.
I've been diving into similar challenges at [company], and I think there's
real alignment with what you're building.

Would you have 15 minutes for a quick chat?

Jordan""",
    tone_notes="Peer-to-peer, genuine interest, brief",  # Delivery guidance
    character_count=487                              # Message body length
)
```

---

## 3. COLD EMAIL

### Basic Usage

```python
from agent_5 import generate_cold_email

email = generate_cold_email(
    opportunity_title="QuantumLeap AI",
    recipient_name="Sarah Chen",
    candidate_name="Jordan Lee",
    shared_contexts=[{"context_type": "hackathon", "name": "PyCon 2025"}],
    proof_card={"matched_skills": [{"skill_name": "PyTorch", "confidence_score": 91}]},
    inroad_score=76.5,
    include_variant_b=True
)

# Primary email
print(f"Subject (A): {email.primary_email.subject_line}")
print(f"Body (A):\n{email.primary_email.body}\n")

# Variant B
if email.variant_b:
    print(f"Subject (B): {email.variant_b.subject_line}")
    print(f"Body (B):\n{email.variant_b.body}\n")

print(f"Sending strategy: {email.sending_notes}")
print(f"Context used: {', '.join(email.context_bridges_included)}")
```

### Full Parameters

```python
ColdEmailPackage(
    opportunity_title="Senior ML Engineer",          # Target opportunity
    recipient_name="Sarah Chen",                     # Recipient name
    primary_email={                                  # Main email variant
        "variant_name": "A",
        "subject_line": "Re: Your PyTorch optimization talk",  # 40-60 optimal
        "body": """Hi Sarah,

I attended your talk at PyCon 2025 on distributed training at scale.
The architecture you described really resonated with me.

I've been working on similar challenges with PyTorch, and I achieved
a 3.2x speedup on transformer inference using kernel-level optimizations.

Would you have 15 minutes to discuss your approach?

Jordan""",
        "cta_type": "meeting_request",               # meeting_request, response_request, etc.
        "estimated_read_time_seconds": 45
    },
    variant_b={                                      # Alternative email (optional)
        "variant_name": "B",
        "subject_line": "Distributed training optimization insight",
        "body": "..."
    },
    sending_notes="High confidence. Send Tue-Thu 9-11am PT.",  # Timing advice
    context_bridges_included=["shared_hackathon"]   # Proof of personalization
)
```

---

## 4. PROOF ATTACHMENT

### Basic Usage

```python
from agent_5 import attach_proof_to_proof_card

proof = attach_proof_to_proof_card(
    opportunity_title="Senior ML Engineer",
    proof_card={
        "matched_skills": [
            {
                "skill_name": "Distributed Systems",
                "confidence_score": 91.0,
                "best_project_evidence": "Led framework handling 128 GPU clusters"
            }
        ]
    }
)

print(f"Primary skill: {proof.primary_proof_attachment.skill_name}")
print(f"Confidence: {proof.primary_proof_attachment.confidence_score}%")
print(f"\nLinkedIn: {proof.linkedin_dm_attachment_snippet}")
print(f"Email: {proof.email_body_attachment_snippet}")
print(f"\nIntegrity: {'✓ Pass' if proof.attachment_integrity_check else '✗ Fail'}")
```

### Full Parameters

```python
AttachedProofCard(
    opportunity_title="Senior ML Engineer",
    primary_proof_attachment={
        "skill_name": "PyTorch Distributed Training",           # Core skill being proven
        "confidence_score": 91.0,                               # 0-100
        "evidence_snippet": "Led framework 128 GPUs, 45% better",  # 150 max
        "evidence_source": "portfolio",                         # portfolio, github, blog
        "attachment_type": "inline_narrative",                  # How to attach
        "attachment_text": "My Distributed Systems experience..."
    },
    secondary_proof_attachments=[],                            # 0-2 supporting skills
    linkedin_dm_attachment_snippet="My distributed training work...",  # 120 max
    email_body_attachment_snippet="My background in distributed systems includes...",  # 300 max
    signature_proof_line="Distributed ML: 128 GPU clusters",   # Optional signature
    attachment_integrity_check=True                            # Is proof specific?
)
```

---

## 5. COMPLETE PACKAGE ASSEMBLY

### Basic Usage

```python
from agent_5 import assemble_outreach_package

package = assemble_outreach_package(
    opportunity_title="Senior ML Engineer",
    candidate_name="Jordan Lee",
    inroad_score=76.5,
    # ... all upstream data
)

# Check overall status
print(f"Generated: {package.generated_timestamp}")
print(f"Safety: {'✓ PASS' if package.safety_checks_passed else '✗ FAIL'}")
print(f"\nExecution order:")
for step in package.recommended_order:
    print(f"  → {step}")

# Export
import json
with open("outreach.json", "w") as f:
    json.dump(package.to_dict(), f, indent=2)
```

### Full Parameters

```python
OutreachPackage(
    opportunity_title="Senior ML Engineer",
    candidate_name="Jordan Lee",
    generated_timestamp="2026-05-27T14:32:15Z",      # ISO8601
    inroad_score=76.5,                               # 0-100

    action_instructions=ActionInstructions(...),      # Component 1
    linkedin_outreach=LinkedInDMTemplate(...),        # Component 2
    email_outreach=ColdEmailPackage(...),             # Component 3
    proof_attachment=AttachedProofCard(...),          # Component 4

    enriched_linkedin_message="""...""",              # With proof integrated
    enriched_email_primary="""...""",                 # With proof integrated

    safety_checks_passed=True,                        # Validation result
    validation_notes=[                                # Check details
        "✓ Action instructions generated",
        "✓ LinkedIn DM generated",
        "..."
    ],
    recommended_order=["action_instructions", "linkedin", "email_followup"],
    estimated_total_time_minutes=45
)
```

# ============================================================================

# DATA STRUCTURE QUICK REFERENCE

# ============================================================================

## Input Data (What to pass in)

```python
# Agent 3 outputs (Chemistry)
{
    "inroad_score": 76.5,                           # 0-100
    "way_in_strategy": {
        "actionable_sentence": str,
        "primary_signal": str,                      # connector, shared_context, engagement
        "confidence": float                         # 0-1
    },
    "shared_contexts": [
        {
            "context_type": str,                    # hackathon, opensource, community
            "name": str,
            "relevance_score": float
        }
    ],
    "engagement_signals": [
        {
            "person_name": str,
            "person_role": str,
            "company": str,
            "interaction_type": str,                # github_star, article_like, repo_fork
            "interaction_detail": str,
            "interaction_date": str                 # YYYY-MM-DD
        }
    ],
    "connector_data": {
        "best_connector": {
            "person_name": str,
            "relationship_to_candidate": str,
            "relationship_to_company": str,
            "introduction_likelihood": float        # 0-1
        }
    }
}

# Agent 4 outputs (Proof)
{
    "proof_card": {
        "matched_skills": [
            {
                "skill_name": str,
                "confidence_score": float,          # 0-100
                "proficiency_level": str,
                "best_project_evidence": str,       # Specific achievement
                "project_count": int
            }
        ]
    }
}

# Context
{
    "candidate_name": str,
    "opportunity_title": str,
    "opportunity_data": {
        "company_name": str,
        "hiring_contact": {"name": str, "title": str},
        "core_focus": str
    }
}
```

## Output Data (What you get back)

```python
{
    # Metadata
    "opportunity_title": str,
    "candidate_name": str,
    "inroad_score": float,
    "generated_timestamp": str,

    # Components
    "action_instructions": {
        "instructions": [...],                     # 2-3 TacticalInstructions
        "priority_sequence": [int],
        "estimated_prep_time_minutes": int
    },
    "linkedin_outreach": {
        "message_type": str,
        "subject_line": str,
        "message_body": str,
        "tone_notes": str,
        "character_count": int
    },
    "email_outreach": {
        "primary_email": {...},                    # EmailVariant
        "variant_b": {...},                        # Optional variant
        "sending_notes": str,
        "context_bridges_included": [str]
    },
    "proof_attachment": {
        "primary_proof_attachment": {...},
        "linkedin_dm_attachment_snippet": str,
        "email_body_attachment_snippet": str
    },

    # Ready-to-use
    "enriched_linkedin_message": str,              # Copy-paste into LinkedIn
    "enriched_email_primary": str,                 # Copy-paste into email

    # Validation
    "safety_checks_passed": bool,
    "validation_notes": [str],
    "recommended_order": [str],
    "estimated_total_time_minutes": int
}
```

# ============================================================================

# COMMON PATTERNS

# ============================================================================

## Pattern 1: High-Confidence Opportunities Only

```python
from agent_5 import assemble_outreach_package

opportunities = [...]  # Your list

for opp in opportunities:
    package = assemble_outreach_package(...)

    # Only process high-confidence
    if package.inroad_score >= 75 and package.safety_checks_passed:
        execute_outreach(package)
    else:
        log_for_review(package)
```

## Pattern 2: A/B Email Testing

```python
email_pkg = package.email_outreach

# Send variant A to 50%
if rand() > 0.5:
    variant = email_pkg.primary_email
else:
    variant = email_pkg.variant_b

send_email(
    to=recipient.email,
    subject=variant.subject_line,
    body=variant.body
)
```

## Pattern 3: Multi-Step Drip Campaign

```python
from datetime import datetime, timedelta

package = assemble_outreach_package(...)

# Day 0: Execute prep
for instr in package.action_instructions.instructions:
    if instr.time_frame == "immediate":
        execute(instr)

# Day 1: Send LinkedIn
schedule_task(
    when=now + timedelta(days=1),
    task="send_linkedin",
    data=package.enriched_linkedin_message
)

# Day 4: Send email
schedule_task(
    when=now + timedelta(days=4),
    task="send_email",
    data={
        "subject": package.email_outreach.primary_email.subject_line,
        "body": package.enriched_email_primary
    }
)

# Day 10: Follow-up
schedule_task(
    when=now + timedelta(days=10),
    task="send_email",
    data={
        "subject": package.email_outreach.variant_b.subject_line,
        "body": package.enriched_email_primary  # Or variant B body
    }
)
```

## Pattern 4: Batch Export for Review

```python
from agent_5 import assemble_outreach_package
import json

packages = []
for opp in opportunities:
    pkg = assemble_outreach_package(...)
    packages.append(pkg.to_dict())

# Export all
with open("outreach_batch.json", "w") as f:
    json.dump(packages, f, indent=2)

# Review in external tool
# Send selected packages programmatically
```

## Pattern 5: Conditional Message Selection

```python
package = assemble_outreach_package(...)

# If very high confidence, use warmer tone
if package.inroad_score >= 80:
    message = package.enriched_linkedin_message
else:
    # Fall back to less warm version
    message = package.linkedin_outreach.message_body

send_linkedin(message)
```

# ============================================================================

# TROUBLESHOOTING

# ============================================================================

## "safety_checks_passed: False"

Check `validation_notes` for details:

```python
if not package.safety_checks_passed:
    print("Validation issues:")
    for note in package.validation_notes:
        if note.startswith("[") or note.startswith("✗"):
            print(f"  {note}")
```

Common issues:

- Missing email CTA
- Message body too short
- Null values in components

## "character_count" too high

Messages will be truncated if over 2000 chars. Check:

```python
if package.linkedin_outreach.character_count > 1500:
    print("⚠ LinkedIn message may be too long")
    print(package.linkedin_outreach.message_body)
```

## Empty "shared_contexts"

If no shared contexts found, InRoad score will be lower:

```python
if not package.action_instructions.instructions:
    print("⚠ No action instructions generated (low signal)")
    # May need to manually create prep tasks
```

## "attachment_integrity_check: False"

Proof is vague or not sufficiently specific:

```python
if not package.proof_attachment.attachment_integrity_check:
    print("⚠ Proof evidence is too generic")
    print(f"  Evidence: {package.proof_attachment.primary_proof_attachment.evidence_snippet}")
    # Try providing more specific proof_card data
```

# ============================================================================

# QUICK CHECKLIST

# ============================================================================

Before sending outreach:

- [ ] Read `enriched_linkedin_message` — does it sound natural?
- [ ] Check LinkedIn subject line — avoid "marketing" language
- [ ] Read email subject — is it compelling?
- [ ] Scan email body — is proof integrated well?
- [ ] Verify all `@mentions` of names are spelled correctly
- [ ] Check `inroad_score` — is it priority-worthy (>70)?
- [ ] Review `estimated_total_time_minutes` — realistic?
- [ ] Confirm `safety_checks_passed: true`
- [ ] Validate `validation_notes` — no critical warnings?

# ============================================================================

# VERSION & SUPPORT

# ============================================================================

Agent 5 v1.0.0
Released: May 27, 2026

For issues or questions, see: AGENT_5_DOCUMENTATION.md (comprehensive)
For examples, see: example_agent_5_complete_workflow.py
For tests, run: python test_agent_5.py
"""
"""
