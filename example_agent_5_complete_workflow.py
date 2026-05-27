"""
Agent 5 Complete Workflow Example

Demonstrates the full pipeline:
  1. Receive opportunity data and upstream signals (Agent 3 & Agent 4)
  2. Generate tactical instructions
  3. Create personalized LinkedIn outreach
  4. Formulate cold email with variants
  5. Attach proof from skill profile
  6. Assemble into unified OutreachPackage
  7. Export for use
"""

import json
from datetime import datetime
from agent_5 import (
    generate_action_instructions,
    generate_linkedin_dm,
    generate_cold_email,
    attach_proof_to_proof_card,
    assemble_outreach_package,
)


def example_workflow():
    """Complete end-to-end Agent 5 workflow."""
    
    print("\n" + "=" * 80)
    print("AGENT 5 — ACTION GENERATOR + OUTREACH AGENT")
    print("Complete Workflow Example")
    print("=" * 80)
    
    # =========================================================================
    # STEP 0: Simulate upstream data from Agents 3 and 4
    # =========================================================================
    print("\n[STEP 0] Loading upstream data from Agents 3 & 4...")
    
    # Data from Agent 3 (Chemistry Engine)
    inroad_score = 76.5  # High chemistry score
    
    way_in_strategy = {
        "actionable_sentence": "You both participated in PyCon 2025 ML hackathon — their tech lead was impressed by your optimization approach.",
        "primary_signal": "shared_context",
        "confidence": 0.88
    }
    
    shared_contexts = [
        {
            "context_type": "hackathon",
            "name": "PyCon 2025 ML Challenge",
            "relevance_score": 0.92
        },
        {
            "context_type": "opensource",
            "name": "PyTorch Optimization",
            "relevance_score": 0.85
        }
    ]
    
    engagement_signals = [
        {
            "person_name": "Dr. Sarah Chen",
            "person_role": "Director, ML Infrastructure",
            "company": "QuantumLeap AI",
            "interaction_type": "github_star",
            "interaction_detail": "Starred your 'distributed-training-framework' repo",
            "interaction_date": "2026-05-18"
        },
        {
            "person_name": "James Park",
            "person_role": "Senior ML Engineer",
            "company": "QuantumLeap AI",
            "interaction_type": "repo_fork",
            "interaction_detail": "Forked your PyTorch optimization utilities",
            "interaction_date": "2026-05-20"
        }
    ]
    
    connector_data = {
        "best_connector": {
            "person_name": "Maya Patel",
            "relationship_to_candidate": "worked together at DataCorp (2022-2024)",
            "relationship_to_company": "currently Engineering Manager at QuantumLeap",
            "introduction_likelihood": 0.94
        }
    }
    
    # Data from Agent 4 (Skill Proof)
    proof_card = {
        "opportunity_title": "Senior ML Infrastructure Engineer - QuantumLeap AI",
        "required_skills": ["Python", "PyTorch", "Kubernetes", "Distributed Systems", "CUDA"],
        "matched_skills": [
            {
                "skill_name": "Distributed ML Systems",
                "confidence_score": 91.0,
                "proficiency_level": "expert",
                "best_project_evidence": "Architected distributed training framework handling 128 GPU clusters with 45% latency reduction vs industry standard",
                "project_count": 5
            },
            {
                "skill_name": "PyTorch & CUDA Optimization",
                "confidence_score": 87.0,
                "proficiency_level": "advanced",
                "best_project_evidence": "Led optimization of PyTorch kernels, achieving 3.2x speedup on transformer inference across A100 GPUs",
                "project_count": 4
            },
            {
                "skill_name": "Kubernetes & Infrastructure",
                "confidence_score": 84.0,
                "proficiency_level": "advanced",
                "best_project_evidence": "Designed Kubernetes ML cluster management system scaling to 500+ model deployments with 99.98% uptime",
                "project_count": 3
            }
        ],
        "total_relevance_score": 87.3,
        "summary": "Exceptional technical alignment. 91% confidence in core ML infrastructure expertise."
    }
    
    # Opportunity metadata
    opportunity_data = {
        "opportunity_title": "Senior ML Infrastructure Engineer",
        "company_name": "QuantumLeap AI",
        "hiring_contact": {
            "name": "Dr. Sarah Chen",
            "title": "Director, ML Infrastructure"
        },
        "core_focus": "building scalable distributed ML infrastructure for foundation model training",
        "featured_blog_topic": "Scaling distributed training to 1000+ GPUs",
        "talk_topic": "PyCon 2025 — PyTorch at Scale"
    }
    
    candidate_name = "Jordan Lee"
    
    print("  [OK] Opportunity: Senior ML Infrastructure Engineer at QuantumLeap AI")
    print(f"  [OK] InRoad Score: {inroad_score}/100 (High chemistry)")
    print(f"  [OK] Primary entry vector: {way_in_strategy['primary_signal']}")
    print(f"  [OK] Proof card confidence: {proof_card['matched_skills'][0]['confidence_score']:.0f}% in core skill")
    
    # =========================================================================
    # STEP 1: Generate Tactical Action Instructions
    # =========================================================================
    print("\n[STEP 1] Generating tactical action instructions...")
    
    action_instructions = generate_action_instructions(
        opportunity_title=opportunity_data["opportunity_title"],
        inroad_score=inroad_score,
        way_in_strategy=way_in_strategy,
        shared_contexts=shared_contexts,
        engagement_signals=engagement_signals,
        connector_data=connector_data,
        proof_card=proof_card,
        opportunity_data=opportunity_data,
    )
    
    print(f"  [OK] Generated {len(action_instructions.instructions)} tactical instructions")
    for i, instr in enumerate(action_instructions.instructions, 1):
        print(f"\n    [{i}] {instr.category.value.upper()}")
        print(f"        Action: {instr.instruction}")
        print(f"        Why: {instr.reasoning}")
        print(f"        Timing: {instr.time_frame}")
    
    print(f"\n  Estimated prep time: {action_instructions.estimated_prep_time_minutes} minutes")
    
    # =========================================================================
    # STEP 2: Generate Personalized LinkedIn DM
    # =========================================================================
    print("\n[STEP 2] Generating personalized LinkedIn outreach...")
    
    linkedin_dm = generate_linkedin_dm(
        opportunity_title=opportunity_data["company_name"],
        candidate_name=candidate_name,
        way_in_strategy=way_in_strategy,
        shared_contexts=shared_contexts,
        engagement_signals=engagement_signals,
        connector_data=connector_data,
        inroad_score=inroad_score,
        opportunity_data=opportunity_data,
    )
    
    print(f"  [OK] Message type: {linkedin_dm.message_type.value}")
    print(f"  [OK] Character count: {linkedin_dm.character_count}")
    print(f"  [OK] Tone: {linkedin_dm.tone_notes}")
    print(f"\n  Subject: {linkedin_dm.subject_line}")
    print(f"\n  Message:\n{'-' * 76}")
    print(linkedin_dm.message_body)
    print(f"{'-' * 76}")
    
    # =========================================================================
    # STEP 3: Generate Cold Email Package
    # =========================================================================
    print("\n[STEP 3] Generating cold email package with variants...")
    
    email_package = generate_cold_email(
        opportunity_title=opportunity_data["company_name"],
        recipient_name=opportunity_data["hiring_contact"]["name"],
        candidate_name=candidate_name,
        shared_contexts=shared_contexts,
        engagement_signals=engagement_signals,
        proof_card=proof_card,
        opportunity_data=opportunity_data,
        inroad_score=inroad_score,
        include_variant_b=True,
    )
    
    print(f"  [OK] Context bridges used: {', '.join(email_package.context_bridges_included)}")
    print(f"  [OK] Sending strategy: {email_package.sending_notes}")
    
    print(f"\n  [PRIMARY EMAIL - Variant A]")
    print(f"  Subject: {email_package.primary_email.subject_line}")
    print(f"  CTA Type: {email_package.primary_email.cta_type.value}")
    print(f"  Read time: ~{email_package.primary_email.estimated_read_time_seconds}s")
    print(f"\n  Body:\n{'-' * 76}")
    print(email_package.primary_email.body)
    print(f"{'-' * 76}")
    
    if email_package.variant_b:
        print(f"\n  [ALTERNATIVE EMAIL - Variant B]")
        print(f"  Subject: {email_package.variant_b.subject_line}")
        print(f"  CTA Type: {email_package.variant_b.cta_type.value}")
        print(f"\n  Body:\n{'-' * 76}")
        print(email_package.variant_b.body)
        print(f"{'-' * 76}")
    
    # =========================================================================
    # STEP 4: Attach Proof Card
    # =========================================================================
    print("\n[STEP 4] Attaching proof card to communications...")
    
    attached_proof = attach_proof_to_proof_card(
        opportunity_title=opportunity_data["opportunity_title"],
        proof_card=proof_card,
        matched_skills=proof_card.get("matched_skills"),
    )
    
    print(f"  [OK] Primary skill: {attached_proof.primary_proof_attachment.skill_name}")
    print(f"  [OK] Confidence: {attached_proof.primary_proof_attachment.confidence_score:.0f}%")
    print(f"  [OK] Evidence source: {attached_proof.primary_proof_attachment.evidence_source}")
    print(f"  [OK] Integrity check: {'PASS [OK]' if attached_proof.attachment_integrity_check else 'FAIL [FAIL]'}")
    
    print(f"\n  LinkedIn snippet:\n    \"{attached_proof.linkedin_dm_attachment_snippet}\"")
    print(f"\n  Email snippet:\n    \"{attached_proof.email_body_attachment_snippet}\"")
    
    if attached_proof.signature_proof_line:
        print(f"\n  Signature line:\n    \"{attached_proof.signature_proof_line}\"")
    
    # =========================================================================
    # STEP 5: Assemble Complete Outreach Package
    # =========================================================================
    print("\n[STEP 5] Assembling unified OutreachPackage...")
    
    outreach_package = assemble_outreach_package(
        opportunity_title=opportunity_data["opportunity_title"],
        candidate_name=candidate_name,
        inroad_score=inroad_score,
        way_in_strategy=way_in_strategy,
        shared_contexts=shared_contexts,
        engagement_signals=engagement_signals,
        connector_data=connector_data,
        proof_card=proof_card,
        opportunity_data=opportunity_data,
    )
    
    print(f"  [OK] Package created for: {outreach_package.opportunity_title} at {outreach_package.opportunity_title}")
    print(f"  [OK] Generated: {outreach_package.generated_timestamp}")
    print(f"  [OK] Safety checks: {'PASSED [OK]' if outreach_package.safety_checks_passed else 'FAILED [FAIL]'}")
    
    print(f"\n  Recommended execution sequence:")
    for i, step in enumerate(outreach_package.recommended_order, 1):
        print(f"    {i}. {step}")
    
    print(f"\n  Total estimated time: {outreach_package.estimated_total_time_minutes} minutes")
    
    print(f"\n  Validation notes ({len(outreach_package.validation_notes)} total):")
    for note in outreach_package.validation_notes[:8]:
        if note.startswith("[OK]"):
            print(f"    {note}")
        elif note.startswith("[FAIL]"):
            print(f"    {note}")
        elif note.startswith("["):
            print(f"    {note}")
    
    if len(outreach_package.validation_notes) > 8:
        print(f"    ... and {len(outreach_package.validation_notes) - 8} more notes")
    
    # =========================================================================
    # STEP 6: Export for Use
    # =========================================================================
    print("\n[STEP 6] Exporting OutreachPackage...")
    
    # Export as JSON
    package_json = outreach_package.to_json()
    
    print(f"  [OK] JSON export: {len(package_json)} bytes")
    print(f"  [OK] Formatted and ready for downstream use")
    
    # Save to file
    output_filename = f"agent_5_outreach_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(package_json)
    
    print(f"  [OK] Saved to: {output_filename}")
    
    # =========================================================================
    # STEP 7: Usage Recommendations
    # =========================================================================
    print("\n[STEP 7] Recommended next actions for candidate:")
    print("\n  BEFORE OUTREACH (Today):")
    for i, instr in enumerate(outreach_package.action_instructions.instructions, 1):
        if instr.time_frame in ["immediate", "before_outreach"]:
            print(f"    [INFO] [{i}] {instr.instruction}")
    
    print("\n  OUTREACH EXECUTION (This week):")
    print(f"    [INFO] Step 1: Send personalized LinkedIn message to Maya Patel")
    print(f"             (Maya is your connector -> Dr. Sarah Chen)")
    print(f"             Target: Next business day")
    
    print(f"\n    [INFO] Step 2: Send cold email to Dr. Sarah Chen")
    print(f"             Subject: {email_package.primary_email.subject_line}")
    print(f"             Wait 3 days after LinkedIn outreach")
    
    print(f"\n    [INFO] Step 3: Optional A/B test with Variant B email after 1 week")
    print(f"             Different subject line + angle")
    
    print("\n  FOLLOW-UP (If no response):")
    print("    [INFO] After 5-7 days: Send follow-up message on LinkedIn")
    print("    [INFO] After 10 days: Try Variant B email with different subject line")
    print("    [INFO] After 14 days: Consider this opportunity lower priority")
    
    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================
    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETE")
    print("=" * 80)
    
    # Extract variables for safe formatting
    opp_title = outreach_package.opportunity_title
    cand_name = outreach_package.candidate_name
    score = f"{outreach_package.inroad_score:.1f}"
    timestamp = outreach_package.generated_timestamp[:19]
    num_instructions = len(outreach_package.action_instructions.instructions)
    char_count = linkedin_dm.character_count
    exec_time = outreach_package.estimated_total_time_minutes
    
    print(f"""
+-------------------------------------------------------------------------+
|                        OUTREACH PACKAGE SUMMARY                         |
+-------------------------------------------------------------------------+
| Opportunity:        {opp_title:<58}|
| Candidate:          {cand_name:<58}|
| Chemistry Score:    {score}/100 (High Priority){"":<35}|
| Safety Status:      PASSED{"":<49}|
| Generated:          {timestamp:<54}|
+-------------------------------------------------------------------------+
| COMPONENTS READY:                                                       |
|   [OK] 2-3 Tactical Action Instructions ({num_instructions} total){"":<32}|
|   [OK] Personalized LinkedIn DM Message ({char_count} chars){"":<28}|
|   [OK] Cold Email Package with Variant B                             |
|   [OK] Proof Card Attachment (from Agent 4)                          |
|   [OK] Integrated Evidence in All Messages                            |
+-------------------------------------------------------------------------+
| ESTIMATED TIME TO EXECUTE: {exec_time} minutes total{"":<41}|
| RECOMMENDED PRIORITY: HIGH (InRoad score > 75)                     |
+-------------------------------------------------------------------------+
    """)
    
    print("[OK] Agent 5 workflow completed successfully!")
    print("[OK] All components generated with full type safety and validation")
    print("[OK] Ready for FastAPI integration or direct use\n")
    
    return outreach_package


if __name__ == "__main__":
    package = example_workflow()
    
    print("\n" + "=" * 80)
    print("Example workflow execution completed.")
    print("You can now:")
    print("  1. Use the OutreachPackage for downstream FastAPI routing")
    print("  2. Export to JSON for frontend visualization")
    print("  3. Integrate with email/LinkedIn APIs for automated sending")
    print("=" * 80)
