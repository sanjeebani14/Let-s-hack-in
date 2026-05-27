"""
Test Suite for Agent 5 — Action Generator + Outreach Agent

Validates all components of the outreach generation pipeline:
  - Action instruction generation
  - LinkedIn DM customization
  - Cold email package creation
  - Proof card attachment integration
  - Full outreach package assembly
"""

import sys
from pathlib import Path

# Test data fixtures
MOCK_OPPORTUNITY_DATA = {
    "opportunity_title": "Senior ML Engineer",
    "company_name": "TechCorp AI",
    "hiring_contact": {
        "name": "Sarah Chen",
        "title": "VP Engineering"
    },
    "core_focus": "scalable machine learning infrastructure",
    "featured_blog_topic": "distributed training at scale"
}

MOCK_INROAD_SCORE = 72.5

MOCK_WAY_IN_STRATEGY = {
    "actionable_sentence": "Their backend lead attended the same PyCon 2025 hackathon you did — that's your way in.",
    "primary_signal": "shared_context",
    "confidence": 0.85
}

MOCK_SHARED_CONTEXTS = [
    {
        "context_type": "hackathon",
        "name": "PyCon 2025 ML Challenge",
        "relevance_score": 0.9
    }
]

MOCK_ENGAGEMENT_SIGNALS = [
    {
        "person_name": "Sarah Chen",
        "person_role": "VP Engineering",
        "company": "TechCorp AI",
        "interaction_type": "github_star",
        "interaction_detail": "Starred your PyTorch distributed training repo",
        "interaction_date": "2026-05-15"
    }
]

MOCK_CONNECTOR_DATA = {
    "best_connector": {
        "person_name": "Alex Rodriguez",
        "relationship_to_candidate": "colleague from previous startup",
        "relationship_to_company": "worked with Sarah Chen on infrastructure team",
        "introduction_likelihood": 0.92
    }
}

MOCK_PROOF_CARD = {
    "opportunity_title": "Senior ML Engineer at TechCorp AI",
    "required_skills": ["Python", "PyTorch", "Kubernetes", "Distributed Systems"],
    "matched_skills": [
        {
            "skill_name": "PyTorch & Distributed Training",
            "confidence_score": 88.0,
            "proficiency_level": "advanced",
            "best_project_evidence": "Led development of PyTorch distributed training system handling 500k images/sec across 32 GPUs, reducing training time 60%",
            "project_count": 3
        },
        {
            "skill_name": "Kubernetes Infrastructure",
            "confidence_score": 82.0,
            "proficiency_level": "advanced",
            "best_project_evidence": "Architected Kubernetes-based ML infrastructure managing 200+ model deployments with 99.95% uptime",
            "project_count": 2
        },
        {
            "skill_name": "Python Backend Development",
            "confidence_score": 79.0,
            "proficiency_level": "advanced",
            "best_project_evidence": "Implemented core Python microservices handling 50k requests/sec with optimized memory footprint",
            "project_count": 4
        }
    ],
    "total_relevance_score": 83.0,
    "summary": "Strong technical match with proven expertise in ML infrastructure and distributed systems"
}


def test_action_instructions():
    """Test action instruction generation."""
    print("\n" + "=" * 70)
    print("TEST: Action Instruction Generation")
    print("=" * 70)
    
    from agent_5 import generate_action_instructions
    
    try:
        instructions = generate_action_instructions(
            opportunity_title=MOCK_OPPORTUNITY_DATA["opportunity_title"],
            inroad_score=MOCK_INROAD_SCORE,
            way_in_strategy=MOCK_WAY_IN_STRATEGY,
            shared_contexts=MOCK_SHARED_CONTEXTS,
            engagement_signals=MOCK_ENGAGEMENT_SIGNALS,
            connector_data=MOCK_CONNECTOR_DATA,
            proof_card=MOCK_PROOF_CARD,
            opportunity_data=MOCK_OPPORTUNITY_DATA,
        )
        
        print(f"✓ Generated {len(instructions.instructions)} instructions")
        print(f"  Estimated time: {instructions.estimated_prep_time_minutes} minutes")
        print(f"  Priority sequence: {instructions.priority_sequence}")
        
        for i, instr in enumerate(instructions.instructions, 1):
            print(f"\n  Instruction {i}: {instr.category.value}")
            print(f"  → {instr.instruction}")
            print(f"  Why: {instr.reasoning}")
            print(f"  When: {instr.time_frame}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_linkedin_dm_generation():
    """Test LinkedIn DM template generation."""
    print("\n" + "=" * 70)
    print("TEST: LinkedIn DM Generation")
    print("=" * 70)
    
    from agent_5 import generate_linkedin_dm
    
    try:
        dm = generate_linkedin_dm(
            opportunity_title=MOCK_OPPORTUNITY_DATA["company_name"],
            candidate_name="Alex Morgan",
            way_in_strategy=MOCK_WAY_IN_STRATEGY,
            shared_contexts=MOCK_SHARED_CONTEXTS,
            engagement_signals=MOCK_ENGAGEMENT_SIGNALS,
            connector_data=MOCK_CONNECTOR_DATA,
            inroad_score=MOCK_INROAD_SCORE,
            opportunity_data=MOCK_OPPORTUNITY_DATA,
        )
        
        print(f"✓ Generated LinkedIn DM")
        print(f"  Type: {dm.message_type.value}")
        print(f"  Subject: {dm.subject_line}")
        print(f"  Length: {dm.character_count} characters")
        print(f"  Tone: {dm.tone_notes}")
        print(f"\n  Message:\n  {dm.message_body[:200]}...")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_cold_email_generation():
    """Test cold email package generation."""
    print("\n" + "=" * 70)
    print("TEST: Cold Email Package Generation")
    print("=" * 70)
    
    from agent_5 import generate_cold_email
    
    try:
        email_pkg = generate_cold_email(
            opportunity_title=MOCK_OPPORTUNITY_DATA["company_name"],
            recipient_name="Sarah Chen",
            candidate_name="Alex Morgan",
            shared_contexts=MOCK_SHARED_CONTEXTS,
            engagement_signals=MOCK_ENGAGEMENT_SIGNALS,
            proof_card=MOCK_PROOF_CARD,
            opportunity_data=MOCK_OPPORTUNITY_DATA,
            inroad_score=MOCK_INROAD_SCORE,
            include_variant_b=True,
        )
        
        print(f"✓ Generated email package")
        print(f"  Recipient: {email_pkg.recipient_name}")
        print(f"  Context bridges: {', '.join(email_pkg.context_bridges_included)}")
        print(f"  Sending strategy: {email_pkg.sending_notes[:60]}...")
        
        print(f"\n  Primary Email (Variant A):")
        print(f"    Subject: {email_pkg.primary_email.subject_line}")
        print(f"    CTA Type: {email_pkg.primary_email.cta_type.value}")
        print(f"    Body preview: {email_pkg.primary_email.body[:150]}...")
        
        if email_pkg.variant_b:
            print(f"\n  Alternative Email (Variant B):")
            print(f"    Subject: {email_pkg.variant_b.subject_line}")
            print(f"    CTA Type: {email_pkg.variant_b.cta_type.value}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_proof_attachment():
    """Test proof card attachment integration."""
    print("\n" + "=" * 70)
    print("TEST: Proof Card Attachment")
    print("=" * 70)
    
    from agent_5 import attach_proof_to_proof_card
    
    try:
        attached = attach_proof_to_proof_card(
            opportunity_title=MOCK_OPPORTUNITY_DATA["opportunity_title"],
            proof_card=MOCK_PROOF_CARD,
            matched_skills=MOCK_PROOF_CARD.get("matched_skills"),
        )
        
        print(f"✓ Attached proof card")
        print(f"  Primary skill: {attached.primary_proof_attachment.skill_name}")
        print(f"  Confidence: {attached.primary_proof_attachment.confidence_score}/100")
        print(f"  Integrity check: {'PASS' if attached.attachment_integrity_check else 'FAIL'}")
        
        print(f"\n  LinkedIn snippet (max 120 chars):")
        print(f"    {attached.linkedin_dm_attachment_snippet}")
        
        print(f"\n  Email snippet (max 300 chars):")
        print(f"    {attached.email_body_attachment_snippet}")
        
        if attached.signature_proof_line:
            print(f"\n  Signature line:")
            print(f"    {attached.signature_proof_line}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_outreach_package_assembly():
    """Test complete outreach package assembly."""
    print("\n" + "=" * 70)
    print("TEST: Complete Outreach Package Assembly")
    print("=" * 70)
    
    from agent_5 import assemble_outreach_package
    
    try:
        package = assemble_outreach_package(
            opportunity_title=MOCK_OPPORTUNITY_DATA["opportunity_title"],
            candidate_name="Alex Morgan",
            inroad_score=MOCK_INROAD_SCORE,
            way_in_strategy=MOCK_WAY_IN_STRATEGY,
            shared_contexts=MOCK_SHARED_CONTEXTS,
            engagement_signals=MOCK_ENGAGEMENT_SIGNALS,
            connector_data=MOCK_CONNECTOR_DATA,
            proof_card=MOCK_PROOF_CARD,
            opportunity_data=MOCK_OPPORTUNITY_DATA,
        )
        
        print(f"✓ Assembled OutreachPackage")
        print(f"  Opportunity: {package.opportunity_title}")
        print(f"  Candidate: {package.candidate_name}")
        print(f"  InRoad Score: {package.inroad_score}/100")
        print(f"  Generated: {package.generated_timestamp}")
        
        print(f"\n  Safety Checks: {'✓ PASSED' if package.safety_checks_passed else '✗ FAILED'}")
        print(f"  Validation notes ({len(package.validation_notes)} total):")
        for note in package.validation_notes[:5]:
            print(f"    - {note}")
        if len(package.validation_notes) > 5:
            print(f"    ... and {len(package.validation_notes) - 5} more")
        
        print(f"\n  Recommended execution order: {' → '.join(package.recommended_order)}")
        print(f"  Estimated total time: {package.estimated_total_time_minutes} minutes")
        
        print(f"\n  Components:")
        print(f"    ✓ Action Instructions ({len(package.action_instructions.instructions)} instructions)")
        print(f"    ✓ LinkedIn DM ({package.linkedin_outreach.character_count} characters)")
        print(f"    ✓ Email Package ({len(package.email_outreach.context_bridges_included)} bridges)")
        print(f"    ✓ Proof Attachment ({package.proof_attachment.primary_proof_attachment.skill_name})")
        
        # Test JSON export
        json_str = package.to_json()
        print(f"\n  JSON export: {len(json_str)} bytes")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_cases():
    """Test edge cases and null safety."""
    print("\n" + "=" * 70)
    print("TEST: Edge Cases & Null Safety")
    print("=" * 70)
    
    from agent_5 import assemble_outreach_package
    
    try:
        # Test with minimal/empty inputs
        package = assemble_outreach_package(
            opportunity_title="Mystery Company",
            candidate_name="Test User",
            inroad_score=25.0,  # Low score
            way_in_strategy=None,  # No strategy
            shared_contexts=[],  # Empty contexts
            engagement_signals=[],  # No engagement
            connector_data=None,  # No connector
            proof_card=None,  # No proof
            opportunity_data=None,  # No opportunity data
        )
        
        print(f"✓ Handled minimal inputs gracefully")
        print(f"  Package still created: {package.opportunity_title}")
        print(f"  Safety checks: {'✓ PASSED' if package.safety_checks_passed else 'Note: Some checks failed'}")
        print(f"  Validation notes: {len(package.validation_notes)} entries")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "#" * 70)
    print("# AGENT 5 TEST SUITE")
    print("#" * 70)
    
    tests = [
        ("Action Instructions", test_action_instructions),
        ("LinkedIn DM Generation", test_linkedin_dm_generation),
        ("Cold Email Generation", test_cold_email_generation),
        ("Proof Attachment", test_proof_attachment),
        ("Outreach Package Assembly", test_outreach_package_assembly),
        ("Edge Cases & Null Safety", test_edge_cases),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ Test {test_name} encountered fatal error: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "#" * 70)
    print("# TEST SUMMARY")
    print("#" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Agent 5 is production-ready.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
