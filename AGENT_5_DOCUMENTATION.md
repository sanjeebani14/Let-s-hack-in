"""
Agent 5 — Action Generator + Outreach Agent
Complete Implementation Documentation

Table of Contents:

1. Overview
2. Architecture & Components
3. Data Flow
4. API Reference
5. Usage Examples
6. Output Formats
7. Safety & Validation
8. Integration Guide
   """

# ============================================================================

# 1. OVERVIEW

# ============================================================================

## What is Agent 5?

Agent 5 converts raw technical alignment data and human pathway intelligence
from Agents 3 and 4 into concrete tactical plans and customized outreach
communications.

**Input**:

- InRoad Chemistry Score (from Agent 3)
- Chemistry signals: shared contexts, engagement, connectors
- Way-in strategy sentence
- Proof Card with matched skills (from Agent 4)

**Output**:

- 2-3 concrete tactical action instructions
- Personalized LinkedIn DM template
- Cold email package with A/B variants
- Proof card attachments integrated into messages
- Unified OutreachPackage for execution

**Philosophy**:

- No external AI calls — fully local execution
- Parameter-injection templates for ultra-personalization
- Organic, human tone — never "salesy"
- Concrete over generic
- Evidence-backed claims

# ============================================================================

# 2. ARCHITECTURE & COMPONENTS

# ============================================================================

## Module Structure

```
agent_5/
├── __init__.py              # Package exports (15 main symbols)
├── instructions.py          # Tactical action generator
│   ├── TacticalInstruction  # Single instruction model
│   ├── ActionInstructions   # Container for 2-3 instructions
│   └── generate_action_instructions()  # Main function
│
├── linkedin_templates.py    # LinkedIn DM customizer
│   ├── LinkedInMessageType  # Enum: WARM_CONNECTOR, SHARED_CONTEXT, etc.
│   ├── LinkedInDMTemplate   # Message container
│   └── generate_linkedin_dm()  # Main function
│
├── email_templates.py       # Cold email package builder
│   ├── EmailCTAType         # Enum: MEETING_REQUEST, RESPONSE_REQUEST, etc.
│   ├── EmailVariant         # Single email variant
│   ├── ColdEmailPackage     # Package with variants
│   └── generate_cold_email()  # Main function
│
├── attachment.py            # Proof card integration
│   ├── ProofAttachmentType  # How proof is attached
│   ├── ProofAttachment      # Single proof item
│   ├── AttachedProofCard    # Full proof integration
│   ├── attach_proof_to_proof_card()  # Prepare proof
│   ├── integrate_proof_into_linkedin_dm()  # Add to DM
│   └── integrate_proof_into_email()  # Add to email
│
└── assembler.py             # Master orchestrator
    ├── OutreachPackage      # Complete unified payload
    ├── AssemblyValidationResult  # Validation details
    └── assemble_outreach_package()  # Main function
```

## Component Dependencies

```
Agent 3 Output (InRoad Score)
    ↓
    ├→ way_in_strategy
    ├→ shared_contexts
    ├→ engagement_signals
    └→ connector_data
         ↓
    [Agent 5 Core]
         ↑
    Agent 4 Output (Proof Card)

    ↓ [Agent 5 Processing]

    ├→ generate_action_instructions()
    ├→ generate_linkedin_dm()
    ├→ generate_cold_email()
    ├→ attach_proof_to_proof_card()
    └→ assemble_outreach_package()

         ↓
    OutreachPackage (Unified)
         ↓
    [FastAPI Router / Export]
```

# ============================================================================

# 3. DATA FLOW

# ============================================================================

## Complete Pipeline

### Input Data Structure

```python
{
    # From Agent 3 (Chemistry Engine)
    "inroad_score": float,              # 0-100
    "way_in_strategy": {
        "actionable_sentence": str,     # Single specific sentence
        "primary_signal": str,           # "connector", "shared_context", etc.
        "confidence": float              # 0-1
    },
    "shared_contexts": [
        {
            "context_type": str,         # "hackathon", "opensource", "community"
            "name": str,
            "relevance_score": float
        }
    ],
    "engagement_signals": [
        {
            "person_name": str,
            "person_role": str,
            "company": str,
            "interaction_type": str,     # "github_star", "article_like", etc.
            "interaction_detail": str,
            "interaction_date": str
        }
    ],
    "connector_data": {
        "best_connector": {
            "person_name": str,
            "relationship_to_candidate": str,
            "relationship_to_company": str,
            "introduction_likelihood": float
        }
    },

    # From Agent 4 (Skill Proof)
    "proof_card": {
        "opportunity_title": str,
        "required_skills": [str],
        "matched_skills": [
            {
                "skill_name": str,
                "confidence_score": float,      # 0-100
                "proficiency_level": str,
                "best_project_evidence": str,   # Specific achievement
                "project_count": int
            }
        ],
        "total_relevance_score": float,
        "summary": str
    },

    # Context
    "candidate_name": str,
    "opportunity_title": str,
    "opportunity_data": {
        "company_name": str,
        "hiring_contact": {"name": str, "title": str},
        "core_focus": str,
        ...
    }
}
```

### Output: OutreachPackage

```python
{
    "opportunity_title": str,
    "candidate_name": str,
    "inroad_score": float,
    "generated_timestamp": str,           # ISO8601

    "action_instructions": {
        "instructions": [
            {
                "instruction": str,          # Exact action
                "category": str,
                "reasoning": str,
                "time_frame": str             # "immediate", "this_week"
            }
        ],
        "priority_sequence": [int],
        "estimated_prep_time_minutes": int
    },

    "linkedin_outreach": {
        "message_type": str,
        "subject_line": str,
        "message_body": str,               # Complete message
        "tone_notes": str,
        "character_count": int
    },

    "email_outreach": {
        "opportunity_title": str,
        "recipient_name": str,
        "primary_email": {
            "variant_name": str,           # "A"
            "subject_line": str,           # 40-60 chars optimal
            "body": str,                   # 150-250 words
            "cta_type": str,
            "estimated_read_time_seconds": int
        },
        "variant_b": {...},                # Alternative email
        "sending_notes": str,
        "context_bridges_included": [str]
    },

    "proof_attachment": {
        "primary_proof_attachment": {
            "skill_name": str,
            "confidence_score": float,
            "evidence_snippet": str,
            "evidence_source": str,
            "attachment_type": str,
            "attachment_text": str
        },
        "secondary_proof_attachments": [...],
        "linkedin_dm_attachment_snippet": str,  # Weaved into DM
        "email_body_attachment_snippet": str,   # Weaved into email
        "signature_proof_line": str,
        "attachment_integrity_check": bool
    },

    "enriched_linkedin_message": str,     # With proof integrated
    "enriched_email_primary": str,         # With proof integrated

    "safety_checks_passed": bool,
    "validation_notes": [str],
    "recommended_order": [str],            # ["action_instructions", "linkedin", ...]
    "estimated_total_time_minutes": int
}
```

# ============================================================================

# 4. API REFERENCE

# ============================================================================

## Main Functions

### 1. generate_action_instructions()

Generates 2-3 concrete, time-sensitive tactical instructions.

```python
from agent_5 import generate_action_instructions

instructions = generate_action_instructions(
    opportunity_title: str,
    inroad_score: float,
    way_in_strategy: Optional[Dict] = None,
    shared_contexts: Optional[List] = None,
    engagement_signals: Optional[List] = None,
    connector_data: Optional[Dict] = None,
    proof_card: Optional[Dict] = None,
    opportunity_data: Optional[Dict] = None,
) -> ActionInstructions

# Returns:
# - instructions: List[TacticalInstruction]  # 2-3 items
# - priority_sequence: List[int]             # Execution order
# - estimated_prep_time_minutes: int         # 15-45 min typically
```

**Instruction Categories**:

- `TECHNICAL_CONTRIBUTION`: "Contribute patch to their repo"
- `SHARED_CONTEXT_REFERENCE`: "Mention PyCon hackathon"
- `ENGAGEMENT_FOLLOW_UP`: "Reply to Sarah's GitHub star"
- `CONNECTOR_REQUEST`: "Ask Maya for introduction"
- `PUBLIC_VISIBILITY`: "Star their repo and comment"

**Time Frames**:

- `immediate`: Do today
- `this_week`: Before outreach
- `before_outreach`: Prep required

---

### 2. generate_linkedin_dm()

Creates hyper-personalized LinkedIn DM with professional, organic tone.

```python
from agent_5 import generate_linkedin_dm

dm = generate_linkedin_dm(
    opportunity_title: str,
    candidate_name: str,
    way_in_strategy: Optional[Dict] = None,
    shared_contexts: Optional[List] = None,
    engagement_signals: Optional[List] = None,
    connector_data: Optional[Dict] = None,
    inroad_score: float = 0.0,
    opportunity_data: Optional[Dict] = None,
) -> LinkedInDMTemplate

# Returns:
# - message_type: LinkedInMessageType       # Entry vector type
# - subject_line: str                       # For connection note
# - message_body: str                       # Complete message
# - tone_notes: str                         # How to send it
# - character_count: int                    # Actual length
```

**Message Types**:

- `WARM_CONNECTOR`: Via introduced contact
- `SHARED_CONTEXT`: Via shared event/community
- `ENGAGEMENT_FOLLOW_UP`: Replying to their action
- `COLLEAGUE_INQUIRY`: Peer-level approach
- `OPEN_INQUIRY`: Cold (fallback)

---

### 3. generate_cold_email()

Formulates complete email package with subject line, body, and CTA.

```python
from agent_5 import generate_cold_email

email_pkg = generate_cold_email(
    opportunity_title: str,
    recipient_name: str,
    candidate_name: str,
    shared_contexts: Optional[List] = None,
    engagement_signals: Optional[List] = None,
    proof_card: Optional[Dict] = None,
    opportunity_data: Optional[Dict] = None,
    inroad_score: float = 0.0,
    include_variant_b: bool = True,
) -> ColdEmailPackage

# Returns:
# - opportunity_title: str
# - recipient_name: str
# - primary_email: EmailVariant              # Variant A
#   - subject_line: str                      # 40-60 chars
#   - body: str                              # 150-250 words
#   - cta_type: EmailCTAType
#   - estimated_read_time_seconds: int
# - variant_b: Optional[EmailVariant]        # For A/B test
# - sending_notes: str                       # Timing advice
# - context_bridges_included: List[str]      # Proof of personalization
```

**CTA Types**:

- `MEETING_REQUEST`: "15 minutes this week?"
- `RESPONSE_REQUEST`: "Thoughts on this?"
- `INFORMATION_REQUEST`: "Love to learn more"
- `COLLABORATION_INQUIRY`: "Collaboration angle?"

---

### 4. attach_proof_to_proof_card()

Prepares proof card for integration into messages.

```python
from agent_5 import attach_proof_to_proof_card

attached = attach_proof_to_proof_card(
    opportunity_title: str,
    proof_card: Optional[Dict] = None,
    matched_skills: Optional[List] = None,
) -> AttachedProofCard

# Returns:
# - primary_proof_attachment: ProofAttachment
#   - skill_name: str
#   - confidence_score: float                # 0-100
#   - evidence_snippet: str                  # 150 chars max
#   - evidence_source: str                   # "portfolio", "github", etc.
#   - attachment_type: ProofAttachmentType
#   - attachment_text: str
# - secondary_proof_attachments: List[ProofAttachment]
# - linkedin_dm_attachment_snippet: str      # 120 chars max
# - email_body_attachment_snippet: str       # 300 chars max
# - signature_proof_line: Optional[str]      # For signature
# - attachment_integrity_check: bool         # Is proof specific?
```

**Proof Attachment Types**:

- `INLINE_NARRATIVE`: Woven into message
- `SIGNATURE_LINK`: In email signature
- `SUPPORTING_DOCUMENT`: Separate reference
- `REFERENCED_CLAIM`: Specific claim with evidence

---

### 5. assemble_outreach_package()

Master function combining all components into unified payload.

```python
from agent_5 import assemble_outreach_package

package = assemble_outreach_package(
    opportunity_title: str,
    candidate_name: str,
    inroad_score: float,
    way_in_strategy: Optional[Dict] = None,
    shared_contexts: Optional[List] = None,
    engagement_signals: Optional[List] = None,
    connector_data: Optional[Dict] = None,
    proof_card: Optional[Dict] = None,
    opportunity_data: Optional[Dict] = None,
) -> OutreachPackage

# Returns: Complete OutreachPackage (see data structure above)
# All validation and null-safety checks automatically performed
```

**Validation Checks Performed**:

- Component integrity validation
- Null-safety checks
- Message length validation
- CTA presence validation
- Proof attachment quality check

---

### Utility Functions

```python
# Proof integration into existing messages
from agent_5 import (
    integrate_proof_into_linkedin_dm,
    integrate_proof_into_email
)

enriched_dm = integrate_proof_into_linkedin_dm(
    dm_message_body: str,
    attached_proof: AttachedProofCard
) -> str

enriched_email = integrate_proof_into_email(
    email_body: str,
    attached_proof: AttachedProofCard
) -> str
```

# ============================================================================

# 5. USAGE EXAMPLES

# ============================================================================

## Example 1: Quick Outreach Package Generation

```python
from agent_5 import assemble_outreach_package
import json

# Prepare your data from Agents 3 & 4
inroad_data = {...}  # From Agent 3
proof_card = {...}   # From Agent 4

# Generate complete package
package = assemble_outreach_package(
    opportunity_title="Senior ML Engineer",
    candidate_name="Alex Morgan",
    inroad_score=76.5,
    way_in_strategy=inroad_data["way_in"],
    shared_contexts=inroad_data["contexts"],
    engagement_signals=inroad_data["engagement"],
    connector_data=inroad_data["connector"],
    proof_card=proof_card,
    opportunity_data=inroad_data["opportunity"]
)

# Export to JSON
json_output = package.to_json()
print(json_output)

# Or access directly
print(f"Instructions: {len(package.action_instructions.instructions)}")
print(f"LinkedIn message: {package.linkedin_outreach.character_count} chars")
print(f"Email subject: {package.email_outreach.primary_email.subject_line}")
print(f"Safety: {'✓ PASSED' if package.safety_checks_passed else '✗ FAILED'}")
```

## Example 2: Individual Component Usage

```python
from agent_5 import (
    generate_action_instructions,
    generate_linkedin_dm,
    generate_cold_email
)

# Generate just instructions
instructions = generate_action_instructions(
    opportunity_title="Senior ML Engineer",
    inroad_score=72.5,
    connector_data=connector_info,
    opportunity_data=opportunity_details
)

for instr in instructions.instructions:
    print(f"• {instr.instruction}")
    print(f"  Why: {instr.reasoning}")

# Generate just LinkedIn message
dm = generate_linkedin_dm(
    opportunity_title="TechCorp",
    candidate_name="Alex Morgan",
    way_in_strategy=way_in_info,
    engagement_signals=signals
)

print(dm.message_body)

# Generate just email
email = generate_cold_email(
    opportunity_title="TechCorp",
    recipient_name="Sarah Chen",
    candidate_name="Alex Morgan",
    shared_contexts=contexts,
    proof_card=proof
)

print(f"Subject: {email.primary_email.subject_line}")
print(f"Body: {email.primary_email.body}")
```

## Example 3: Accessing Enriched Messages

```python
# After assembly, messages have proof integrated
package = assemble_outreach_package(...)

# Use enriched versions (with proof embedded)
linkedin_ready = package.enriched_linkedin_message
email_ready = package.enriched_email_primary

# Send directly
send_linkedin_dm(linkedin_ready)
send_email(
    to=hiring_contact.email,
    subject=package.email_outreach.primary_email.subject_line,
    body=email_ready
)
```

## Example 4: A/B Testing

```python
email_pkg = package.email_outreach

# Variant A (primary)
variant_a = {
    "subject": email_pkg.primary_email.subject_line,
    "body": email_pkg.primary_email.body
}

# Variant B (alternative)
variant_b = {
    "subject": email_pkg.variant_b.subject_line,
    "body": email_pkg.variant_b.body
}

# Send variant A initially
send_email(**variant_a)

# After 7 days, try variant B if no response
if not received_response:
    send_email(**variant_b)
```

## Example 5: Batch Processing

```python
from agent_5 import assemble_outreach_package
import json

# Process multiple opportunities
opportunities = load_opportunities()
packages = []

for opp in opportunities:
    package = assemble_outreach_package(
        opportunity_title=opp["title"],
        candidate_name=opp["candidate"],
        inroad_score=opp["inroad_score"],
        way_in_strategy=opp["chemistry"]["way_in"],
        # ... other fields
    )

    if package.safety_checks_passed and package.inroad_score > 70:
        packages.append(package)

# Export all
output = [p.to_dict() for p in packages]
with open("outreach_packages.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated {len(packages)} ready-to-send outreach packages")
```

# ============================================================================

# 6. OUTPUT FORMATS

# ============================================================================

## JSON Export Format

```json
{
  "opportunity_title": "Senior ML Engineer",
  "candidate_name": "Alex Morgan",
  "generated_timestamp": "2026-05-27T14:32:15.123Z",
  "inroad_score": 76.5,

  "action_instructions": {
    "opportunity_title": "Senior ML Engineer",
    "instructions": [
      {
        "instruction": "Star their recent PyTorch optimization repo and leave a technical comment...",
        "category": "public_visibility",
        "reasoning": "Public contributions signal expertise and show up in notifications.",
        "time_frame": "this_week"
      }
    ],
    "priority_sequence": [1, 2],
    "estimated_prep_time_minutes": 30
  },

  "linkedin_outreach": {
    "message_type": "shared_context",
    "subject_line": "From PyCon 2025 — Your PyTorch optimization work",
    "message_body": "Hi Sarah,\n\nI noticed you starred our distributed...",
    "tone_notes": "Peer-to-peer, technical, curious.",
    "character_count": 487
  },

  "email_outreach": {
    "opportunity_title": "Senior ML Engineer",
    "recipient_name": "Sarah Chen",
    "primary_email": {
      "variant_name": "A",
      "subject_line": "Re: Your PyCon 2025 optimization talk",
      "body": "Hi Sarah,\n\nI attended your talk...",
      "cta_type": "meeting_request",
      "estimated_read_time_seconds": 45
    },
    "variant_b": {
      "variant_name": "B",
      "subject_line": "Distributed training optimization insight",
      ...
    },
    "sending_notes": "High confidence match. Send immediately.",
    "context_bridges_included": ["shared_hackathon", "engagement"]
  },

  "proof_attachment": {
    "primary_proof_attachment": {
      "skill_name": "Distributed ML Systems",
      "confidence_score": 91.0,
      "evidence_snippet": "Led distributed training framework...",
      "evidence_source": "portfolio",
      "attachment_type": "inline_narrative",
      "attachment_text": "My Distributed ML Systems experience..."
    },
    "linkedin_dm_attachment_snippet": "My distributed training work...",
    "email_body_attachment_snippet": "My background in distributed systems...",
    "attachment_integrity_check": true
  },

  "enriched_linkedin_message": "Hi Sarah,\n\nI noticed you starred our repo...\n\nMy distributed training work: Led framework...",
  "enriched_email_primary": "Hi Sarah,\n\nI attended your talk...\n\nMy background in distributed systems...",

  "safety_checks_passed": true,
  "validation_notes": [
    "✓ Action instructions generated",
    "✓ LinkedIn DM generated",
    "[action_instructions_valid]: true",
    "[linkedin_dm_valid]: true",
    ...
  ],
  "recommended_order": ["action_instructions", "linkedin", "email_followup"],
  "estimated_total_time_minutes": 45
}
```

## Direct Dictionary Export

```python
package_dict = package.to_dict()
# Can serialize/deserialize with json.dumps()/json.loads()
```

## Component Access

```python
# Individual message bodies
print(package.linkedin_outreach.message_body)
print(package.email_outreach.primary_email.body)

# Enriched with proof
print(package.enriched_linkedin_message)
print(package.enriched_email_primary)

# Instructions only
for instr in package.action_instructions.instructions:
    print(instr.instruction)

# Proof details
print(package.proof_attachment.primary_proof_attachment.evidence_snippet)
```

# ============================================================================

# 7. SAFETY & VALIDATION

# ============================================================================

## Null-Safety Guarantees

All functions include robust null-handling:

```python
# Safe defaults for missing inputs
way_in_strategy = way_in_strategy or {}
shared_contexts = shared_contexts or []
proof_card = proof_card or {}

# No null injection in templates
message = _sanitize_template_value(person_name, fallback="there")

# All optional fields have sensible fallbacks
connector_name = _safe_get_nested(
    connector_data,
    "best_connector",
    "person_name",
    default="your colleague"
)
```

## Validation Checks

All validation performed in `assemble_outreach_package()`:

1. **Action Instructions Validation**
   - Must have 2-3 items
   - Each must have non-empty instruction text
   - Must have valid time_frame

2. **LinkedIn DM Validation**
   - message_body > 20 characters
   - subject_line present
   - character_count < 2000

3. **Email Package Validation**
   - primary_email required
   - subject_line 10-60 characters
   - body 50-3000 characters
   - CTA present in body

4. **Proof Attachment Validation**
   - primary_proof_attachment non-null
   - evidence_snippet > 10 characters
   - attachment_integrity_check evaluated

5. **Null Safety Validation**
   - All major components non-null
   - Fallbacks applied where needed

## Validation Result Structure

```python
package.safety_checks_passed: bool       # Overall pass/fail
package.validation_notes: List[str]      # Individual check results
package.validation_notes[0]:             # "✓ Action instructions generated"
package.validation_notes[1]:             # "[check_name]: true/false"
```

## Error Handling Philosophy

- **No exceptions**: All errors caught and logged
- **Graceful degradation**: Creates minimal valid package if needed
- **Informative notes**: Validation notes explain what happened
- **Production ready**: Safe to use even with incomplete inputs

# ============================================================================

# 8. INTEGRATION GUIDE

# ============================================================================

## FastAPI Integration

```python
from fastapi import FastAPI
from agent_5 import assemble_outreach_package

app = FastAPI()

@app.post("/generate-outreach")
async def generate_outreach(request: dict):
    """Generate outreach package for opportunity."""

    package = assemble_outreach_package(
        opportunity_title=request["opportunity_title"],
        candidate_name=request["candidate_name"],
        inroad_score=request["inroad_score"],
        way_in_strategy=request.get("way_in_strategy"),
        shared_contexts=request.get("shared_contexts"),
        engagement_signals=request.get("engagement_signals"),
        connector_data=request.get("connector_data"),
        proof_card=request.get("proof_card"),
        opportunity_data=request.get("opportunity_data"),
    )

    return package.to_dict()

@app.get("/outreach/{opportunity_id}/execute")
async def execute_outreach(opportunity_id: str):
    """Execute outreach (send messages, etc.)"""

    package = load_outreach_package(opportunity_id)

    # Execute recommended order
    for step in package.recommended_order:
        if step == "action_instructions":
            execute_instructions(package.action_instructions)
        elif step == "linkedin":
            send_linkedin(package.enriched_linkedin_message)
        elif step == "email_followup":
            send_email(
                subject=package.email_outreach.primary_email.subject_line,
                body=package.enriched_email_primary
            )

    return {"status": "executed", "opportunity": opportunity_id}
```

## Database Storage

```python
import json
from datetime import datetime

class OutreachPackageRecord:
    def __init__(self, package: OutreachPackage):
        self.opportunity_title = package.opportunity_title
        self.candidate_name = package.candidate_name
        self.inroad_score = package.inroad_score
        self.generated_timestamp = package.generated_timestamp
        self.package_json = package.to_json()
        self.status = "generated"  # generated, sent, responded, etc.
        self.created_at = datetime.utcnow()

# Save to database
record = OutreachPackageRecord(package)
db.session.add(record)
db.session.commit()

# Retrieve
retrieved = db.query(OutreachPackageRecord).filter_by(
    opportunity_title="Senior ML Engineer"
).first()

# Reconstruct package
from agent_5 import OutreachPackage
package = OutreachPackage(**json.loads(retrieved.package_json))
```

## File Export

```python
from agent_5 import OutreachPackage
import json

# Save individual package
with open(f"outreach_{opportunity_id}.json", "w") as f:
    f.write(package.to_json())

# Load from file
with open(f"outreach_{opportunity_id}.json", "r") as f:
    data = json.load(f)
    package = OutreachPackage(**data)
```

## Next Steps Integration

```python
# After successful outreach, track follow-up
follow_ups = {
    "day_1": {
        "action": "wait",
        "reason": "Give them time to read first message"
    },
    "day_5": {
        "action": "check_response",
        "if_no_response": "send_linkedin_followup"
    },
    "day_7": {
        "action": "send_email_variant_b",
        "if_no_response": "continue_tracking"
    },
    "day_14": {
        "action": "lower_priority",
        "reason": "After 2 weeks with no response"
    }
}

# Schedule these checks
for day, action_plan in follow_ups.items():
    schedule_task(
        task_id=f"{opportunity_id}_{day}",
        when=f"+{day}",
        function="execute_followup_action",
        args={"opportunity_id": opportunity_id, **action_plan}
    )
```

---

## Performance Notes

- **Generation time**: ~50-100ms per package
- **JSON size**: ~3-5KB per package (compressed: ~1KB)
- **Memory**: Minimal footprint, all local execution
- **Scalability**: Linear with opportunity count, no API limits

---

## Version Information

- **Agent 5 Version**: 1.0.0
- **Python**: 3.11+
- **Dependencies**: Pydantic 2.13.4+
- **Last Updated**: May 27, 2026

---

"""
"""
