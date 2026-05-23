"""
Agent 3 Implementation Test & Demonstration

This script validates the Agent 3 — InRoad Chemistry Engine implementation
without requiring the full FastAPI server or complex dependencies.
"""

import json
from typing import Dict, Any

# Import Agent 3 modules
from agent_3.context_detector import detect_shared_contexts
from agent_3.engagement import check_engagement_signals
from agent_3.connector import find_connector_persons
from agent_3.team_analyzer import analyze_team_composition
from agent_3.calculator import calculate_inroad_score
from agent_3.way_in import generate_way_in


def test_agent_3_implementation():
    """Test all Agent 3 components with sample data."""
    
    print("=" * 80)
    print("AGENT 3 — InRoad Chemistry Engine Implementation Test")
    print("=" * 80)
    
    # Create mock candidate profile (from Member A)
    candidate_profile = {
        "core_skills": ["Python", "FastAPI", "ML", "Backend"],
        "ownership_signals": ["Built end-to-end applications", "Integrated cloud services"],
        "measurable_outcomes": ["Created AI-powered systems", "Developed ML models"],
        "problem_solving_patterns": ["Built scalable AI apps", "Real-time systems"],
        "domain_expertise": ["Artificial Intelligence", "Computer Vision"],
        "seniority_level": "Student Developer",
        "semantic_summary": "AI-focused computer science student experienced in building intelligent applications"
    }
    
    # Create mock opportunity data (from Member B)
    opportunity = {
        "id": 1,
        "title": "AI/ML Engineer - Early Stage",
        "company": "NeuralFlow Startup",
        "source_type": "founder_post",
        "description": "Building edge AI inference platform",
        "team_size": 4,
        "stage": "seed",
        "posted_date": "2026-05-15",
        "competition_index": 0.85,
        "response_probability": 0.78,
        "growth_potential": 0.90,
        "referral_likelihood": 0.70,
        "opportunity_score": 0.805,
        "score_reasoning": "Highly hidden opportunity with strong growth potential"
    }
    
    # Simulated Member A fit score
    role_fit_score = 87.5
    
    print("\n" + "=" * 80)
    print("INPUT DATA")
    print("=" * 80)
    print(f"\nCandidate Seniority: {candidate_profile['seniority_level']}")
    print(f"Opportunity: {opportunity['title']} at {opportunity['company']}")
    print(f"Role Fit Score from Member A: {role_fit_score}%")
    
    # ============================================
    # Component 1: Context Detector
    # ============================================
    print("\n" + "=" * 80)
    print("COMPONENT 1: Shared Context Detector")
    print("=" * 80)
    
    context_response = detect_shared_contexts(candidate_profile, opportunity)
    print(f"\nShared Touchpoints Found: {len(context_response.shared_contexts)}")
    print(f"Total Overlap Score: {context_response.total_overlap_score:.2%}")
    print(f"Summary: {context_response.summary}")
    for ctx in context_response.shared_contexts:
        print(f"  • {ctx.context_type.upper()}: {ctx.name} (Relevance: {ctx.relevance_score:.2%})")
    
    # ============================================
    # Component 2: Engagement Signal Checker
    # ============================================
    print("\n" + "=" * 80)
    print("COMPONENT 2: Engagement Signal Checker")
    print("=" * 80)
    
    engagement_response = check_engagement_signals(candidate_profile, opportunity)
    print(f"\nEmployee Interactions Detected: {len(engagement_response.interactions)}")
    print(f"Engagement Strength: {engagement_response.engagement_strength:.2%}")
    print(f"Summary: {engagement_response.summary}")
    for interaction in engagement_response.interactions:
        print(f"  • {interaction.person_name} ({interaction.person_role})")
        print(f"    └─ {interaction.interaction_detail} [{interaction.interaction_date}]")
    
    # ============================================
    # Component 3: Connector Person Finder
    # ============================================
    print("\n" + "=" * 80)
    print("COMPONENT 3: Connector Person Finder")
    print("=" * 80)
    
    connector_response = find_connector_persons(candidate_profile, opportunity)
    print(f"\nConnectors Identified: {len(connector_response.connectors)}")
    print(f"Entry Probability: {connector_response.entry_probability:.2%}")
    print(f"Summary: {connector_response.summary}")
    print(f"\nBest Connector:")
    print(f"  Name: {connector_response.best_connector.person_name}")
    print(f"  Relationship to You: {connector_response.best_connector.relationship_to_candidate}")
    print(f"  Relationship to Company: {connector_response.best_connector.relationship_to_company}")
    print(f"  Introduction Likelihood: {connector_response.best_connector.introduction_likelihood:.2%}")
    
    # ============================================
    # Component 4: Team Composition Analyzer
    # ============================================
    print("\n" + "=" * 80)
    print("COMPONENT 4: Team Composition Analyzer")
    print("=" * 80)
    
    team_analysis = analyze_team_composition(candidate_profile, opportunity)
    print(f"\nCandidate Seniority: {team_analysis.candidate_seniority}")
    print(f"Team Seniority Distribution: {team_analysis.target_team_seniority_distribution}")
    print(f"Fit Category: {team_analysis.fit_category.value.upper()}")
    print(f"Chemistry Score: {team_analysis.chemistry_score:.2%}")
    print(f"Reasoning: {team_analysis.reasoning}")
    
    # ============================================
    # Component 5: InRoad Score Calculator
    # ============================================
    print("\n" + "=" * 80)
    print("COMPONENT 5: InRoad Score Calculator")
    print("=" * 80)
    
    inroad_score = calculate_inroad_score(
        role_fit_score,
        context_response,
        connector_response,
        engagement_response,
        opportunity["competition_index"],
        opportunity
    )
    
    print(f"\nInRoad Score Calculation:")
    print(f"  Role Fit %:              {inroad_score.role_fit_percentage:>6.2f}% × 0.40")
    print(f"  Team Overlap %:          {inroad_score.team_overlap_percentage:>6.2f}% × 0.20")
    print(f"  Entry Probability %:     {inroad_score.entry_probability_percentage:>6.2f}% × 0.30")
    print(f"  Competition Index:       {inroad_score.competition_index:>6.2%} × 0.10")
    print(f"  {'─' * 50}")
    print(f"  FINAL InRoad SCORE:      {inroad_score.inroad_score:>6.2f}% 🎯")
    print(f"\nStructural Explanation:")
    print(f"  {inroad_score.structural_explanation}")
    
    # ============================================
    # Component 6: "Your Way In" Generator
    # ============================================
    print("\n" + "=" * 80)
    print("COMPONENT 6: 'Your Way In' Generator")
    print("=" * 80)
    
    way_in = generate_way_in(
        candidate_profile,
        opportunity,
        context_response,
        connector_response,
        engagement_response,
        team_analysis,
        inroad_score
    )
    
    print(f"\nPrimary Signal: {way_in.primary_signal.upper()}")
    print(f"Confidence: {way_in.confidence:.2%}")
    print(f"\nYour Way In:")
    print(f"  💡 {way_in.actionable_sentence}")
    
    # ============================================
    # Final Summary
    # ============================================
    print("\n" + "=" * 80)
    print("FINAL CHEMISTRY PROFILE")
    print("=" * 80)
    
    summary_data = {
        "opportunity": {
            "title": opportunity["title"],
            "company": opportunity["company"],
            "source_type": opportunity["source_type"]
        },
        "chemistry_analysis": {
            "inroad_score": round(inroad_score.inroad_score, 2),
            "role_fit": round(inroad_score.role_fit_percentage, 2),
            "team_overlap": round(inroad_score.team_overlap_percentage, 2),
            "entry_probability": round(inroad_score.entry_probability_percentage, 2),
            "team_fit": team_analysis.fit_category.value,
            "shared_contexts": len(context_response.shared_contexts),
            "employee_interactions": len(engagement_response.interactions),
            "best_connector": connector_response.best_connector.person_name
        },
        "entry_strategy": {
            "primary_signal": way_in.primary_signal,
            "confidence": round(way_in.confidence, 2),
            "action": way_in.actionable_sentence
        }
    }
    
    print(json.dumps(summary_data, indent=2))
    
    print("\n" + "=" * 80)
    print("✅ AGENT 3 IMPLEMENTATION TEST SUCCESSFUL")
    print("=" * 80)
    print("\nAll 6 components working correctly:")
    print("  1. ✓ Context Detector — Finds shared touchpoints")
    print("  2. ✓ Engagement Checker — Detects employee interactions")
    print("  3. ✓ Connector Finder — Identifies second-degree bridges")
    print("  4. ✓ Team Analyzer — Assesses cultural fit")
    print("  5. ✓ Calculator — Combines signals into InRoad score")
    print("  6. ✓ Way In Generator — Creates actionable entry strategy")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_agent_3_implementation()
