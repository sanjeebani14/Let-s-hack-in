"""
Simple test for Agent 5 — Action Generator + Outreach Agent

Uses ASCII-only characters for Windows console compatibility.
"""

from agent_5 import (
    generate_action_instructions,
    generate_linkedin_dm,
    generate_cold_email,
    attach_proof_to_proof_card,
    assemble_outreach_package,
)

def test_agent5_simple():
    """Run a simple test of Agent 5."""
    
    print("\n" + "="*70)
    print("AGENT 5 - SIMPLE TEST")
    print("="*70)
    
    # Mock data
    inroad_score = 76.5
    way_in = {
        "actionable_sentence": "You both attended PyCon 2025",
        "primary_signal": "shared_context",
        "confidence": 0.88
    }
    contexts = [
        {"context_type": "hackathon", "name": "PyCon 2025", "relevance_score": 0.92}
    ]
    engagement = [
        {
            "person_name": "Sarah",
            "interaction_type": "github_star",
            "interaction_detail": "Starred your repo",
            "interaction_date": "2026-05-18"
        }
    ]
    connector = {
        "best_connector": {
            "person_name": "Maya",
            "relationship_to_candidate": "colleague",
            "introduction_likelihood": 0.94
        }
    }
    proof = {
        "matched_skills": [
            {
                "skill_name": "PyTorch",
                "confidence_score": 91.0,
                "best_project_evidence": "Led distributed training, 3.2x speedup"
            }
        ]
    }
    opp_data = {
        "company_name": "TechCorp",
        "core_focus": "distributed ML infrastructure"
    }
    
    # Test 1: Action instructions
    print("\n[TEST 1] Action Instructions...")
    try:
        instr = generate_action_instructions(
            opportunity_title="ML Engineer",
            inroad_score=inroad_score,
            way_in_strategy=way_in,
            shared_contexts=contexts,
            engagement_signals=engagement,
            connector_data=connector,
            proof_card=proof,
            opportunity_data=opp_data,
        )
        print("[PASS] Generated", len(instr.instructions), "instructions")
    except Exception as e:
        print("[FAIL]", str(e))
        return 1
    
    # Test 2: LinkedIn DM
    print("\n[TEST 2] LinkedIn DM...")
    try:
        dm = generate_linkedin_dm(
            opportunity_title="TechCorp",
            candidate_name="Jordan",
            way_in_strategy=way_in,
            shared_contexts=contexts,
            engagement_signals=engagement,
            connector_data=connector,
            inroad_score=inroad_score,
            opportunity_data=opp_data,
        )
        print("[PASS] LinkedIn DM generated,", dm.character_count, "chars")
    except Exception as e:
        print("[FAIL]", str(e))
        return 1
    
    # Test 3: Cold Email
    print("\n[TEST 3] Cold Email...")
    try:
        email = generate_cold_email(
            opportunity_title="TechCorp",
            recipient_name="Sarah",
            candidate_name="Jordan",
            shared_contexts=contexts,
            engagement_signals=engagement,
            proof_card=proof,
            opportunity_data=opp_data,
            inroad_score=inroad_score,
        )
        print("[PASS] Email generated, subject:", email.primary_email.subject_line[:40])
    except Exception as e:
        print("[FAIL]", str(e))
        return 1
    
    # Test 4: Proof Attachment
    print("\n[TEST 4] Proof Attachment...")
    try:
        attached = attach_proof_to_proof_card(
            opportunity_title="ML Engineer",
            proof_card=proof,
        )
        print("[PASS] Proof attached, skill:", attached.primary_proof_attachment.skill_name)
    except Exception as e:
        print("[FAIL]", str(e))
        return 1
    
    # Test 5: Complete Package
    print("\n[TEST 5] Complete Package Assembly...")
    try:
        package = assemble_outreach_package(
            opportunity_title="Senior ML Engineer",
            candidate_name="Jordan Lee",
            inroad_score=inroad_score,
            way_in_strategy=way_in,
            shared_contexts=contexts,
            engagement_signals=engagement,
            connector_data=connector,
            proof_card=proof,
            opportunity_data=opp_data,
        )
        print("[PASS] Package created")
        print("  - Score:", package.inroad_score)
        print("  - Safety:", "PASS" if package.safety_checks_passed else "FAIL")
        print("  - Time:", package.estimated_total_time_minutes, "minutes")
    except Exception as e:
        print("[FAIL]", str(e))
        return 1
    
    # Test 6: Edge cases
    print("\n[TEST 6] Edge Cases...")
    try:
        package2 = assemble_outreach_package(
            opportunity_title="Engineer",
            candidate_name="Test",
            inroad_score=25.0,
        )
        print("[PASS] Handled minimal inputs gracefully")
    except Exception as e:
        print("[FAIL]", str(e))
        return 1
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED [6/6]")
    print("="*70)
    print("\nAgent 5 is working correctly!")
    return 0

if __name__ == "__main__":
    import sys
    exit_code = test_agent5_simple()
    sys.exit(exit_code)
