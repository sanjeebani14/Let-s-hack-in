"""
Test Agent 4 modules to verify functionality
"""
import sys
sys.path.insert(0, '/c/Users/SANJEEBANI PARIDA/Let-s-hack-in')

# Test imports
print("Testing Agent 4 module imports...")
try:
    from agent_4 import (
        parse_project_narrative,
        detect_ownership_level,
        score_outcome_clarity,
        evaluate_complexity,
        calculate_confidence_score,
        build_skill_graph,
        generate_proof_card,
    )
    print("✓ All imports successful!")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test basic functionality
print("\nTesting basic functionality...")

# Test 1: Parse narrative
test_narrative = """
I led the development of a high-performance event streaming platform using Python and Apache Kafka.
Our system processed over 1 million events per second with sub-100ms latency.
I designed the distributed architecture, managed a team of 3 engineers, and overcame significant challenges 
with distributed consensus and data consistency.
The platform reduced our data processing time by 65% and improved system reliability to 99.99% uptime.
We used sophisticated technologies like Kubernetes for orchestration and PostgreSQL for persistent storage.
"""

narrative = parse_project_narrative(test_narrative)
print(f"✓ Parsed narrative: '{narrative.what_was_built[:50]}...'")

# Test 2: Ownership detection
ownership = detect_ownership_level(test_narrative, narrative.candidate_role)
print(f"✓ Ownership level: {ownership.ownership_level} (confidence: {ownership.confidence:.2f})")

# Test 3: Outcome clarity
clarity = score_outcome_clarity(narrative.outcome)
print(f"✓ Outcome clarity: {clarity.clarity_score:.2f} (is_specific: {clarity.is_specific})")
print(f"  - Measures found: {len(clarity.measures_found)}")

# Test 4: Complexity evaluation
complexity = evaluate_complexity(test_narrative, narrative.challenges_faced)
print(f"✓ Complexity: {complexity.complexity_level} (score: {complexity.complexity_score:.2f})")

# Test 5: Confidence score
confidence = calculate_confidence_score(
    "Python",
    ownership,
    clarity,
    complexity,
    project_count=1
)
print(f"✓ Skill confidence: {confidence.skill_name} = {confidence.confidence_score:.1f}/100 ({confidence.proficiency_level})")

# Test 6: Build graph (mock multiple skills)
from agent_4 import SkillConfidenceScore, build_skill_graph

# Create multiple skill scores
mock_scores = {
    "Python": [confidence],
    "Kubernetes": [
        SkillConfidenceScore(
            skill_name="Kubernetes",
            confidence_score=78.5,
            evidence_projects=1,
            components=[],
            proficiency_level="advanced",
            summary="Advanced: 78.5/100"
        )
    ]
}

graph = build_skill_graph(mock_scores)
print(f"✓ Built skill graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")

# Test 7: Generate proof card
opportunity = """
We are looking for a senior backend engineer with expertise in Python and distributed systems.
Required: Python, Kubernetes, PostgreSQL, system design expertise.
Preferred: Apache Kafka, microservices architecture, high-performance systems.
"""

proof_card = generate_proof_card(graph, opportunity, "Senior Backend Engineer", max_skills=3)
print(f"✓ Generated proof card: {len(proof_card.matched_skills)} matched skills")
for skill in proof_card.matched_skills:
    print(f"  - {skill.skill_name}: {skill.confidence_score:.1f}/100")

print("\n✅ All tests passed!")
