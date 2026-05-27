"""
Agent 4 Skill Proof Agent - Comprehensive Usage Example

Demonstrates the complete workflow of parsing portfolio descriptions,
calculating trust scores for technical competencies, and generating
visualization-ready data structures.
"""

import sys
sys.path.insert(0, '/c/Users/SANJEEBANI PARIDA/Let-s-hack-in')

from agent_4 import (
    parse_project_narrative,
    detect_ownership_level,
    score_outcome_clarity,
    evaluate_complexity,
    calculate_confidence_score,
    extract_skills_from_text,
    build_skill_graph,
    generate_proof_card,
    graph_to_dict,
    proof_card_to_dict,
)
import json


def demonstrate_agent_4_workflow():
    """
    Complete workflow demonstration of Agent 4.
    
    Shows how to:
    1. Parse project narratives
    2. Analyze ownership and contributions
    3. Evaluate outcome clarity with metrics
    4. Assess problem complexity
    5. Generate skill confidence scores
    6. Build visualization-ready skill graph
    7. Generate targeted proof cards for opportunities
    """
    
    # =====================================================================
    # PHASE 1: Parse Portfolio Project Descriptions
    # =====================================================================
    print("=" * 70)
    print("PHASE 1: Parsing Portfolio Projects")
    print("=" * 70)
    
    projects = [
        {
            "id": "project_1",
            "description": """
            Led the design and implementation of a real-time event streaming platform
            using Python, Apache Kafka, and PostgreSQL. Architected a distributed system
            that processes over 2 million events per second with sub-100ms latency.
            Managed a team of 4 engineers across design, implementation, and deployment.
            
            Faced significant challenges with distributed consensus and exactly-once
            semantics. Pioneered a novel approach combining Kafka offset management with
            custom checkpointing. The solution reduced data loss incidents by 100% and
            improved end-to-end consistency from 99.9% to 99.99%.
            
            Key decisions: Used Kubernetes for orchestration, implemented custom
            monitoring with Prometheus and Grafana. Migrated from RabbitMQ which couldn't
            handle the throughput requirements.
            """
        },
        {
            "id": "project_2",
            "description": """
            Developed a machine learning feature extraction pipeline for real-time
            recommendation system using Python, TensorFlow, and Redis.
            Implemented vector quantization techniques that reduced model size by 75%
            while maintaining 98% accuracy.
            
            Contributed to both the research phase and production implementation.
            Worked closely with ML researchers to productionize novel embedding techniques.
            Achieved 50% improvement in inference latency (from 200ms to 100ms) by
            optimizing vector operations with NumPy and Cython.
            """
        },
        {
            "id": "project_3",
            "description": """
            Built a React-based real-time dashboard for monitoring distributed systems.
            Implemented WebSocket connections for live data updates, state management
            with Redux, and created responsive UI components.
            
            Improved dashboard load time from 5 seconds to 800ms through code splitting
            and lazy loading. Added comprehensive unit tests achieving 92% code coverage.
            Collaborated with backend team on API design and data format optimization.
            """
        }
    ]
    
    # Parse each project
    parsed_projects = []
    for project in projects:
        narrative = parse_project_narrative(project["description"])
        project["parsed"] = narrative
        parsed_projects.append((project, narrative))
        
        print(f"\n[PROJECT] {project['id']}:")
        print(f"   Built: {narrative.what_was_built[:60]}...")
        print(f"   Role: {narrative.candidate_role[:50]}...")
        print(f"   Outcome: {narrative.outcome[:50]}...")
        print(f"   Challenges: {len(narrative.challenges_faced)} identified")
    
    # =====================================================================
    # PHASE 2: Analyze Ownership Depth
    # =====================================================================
    print("\n" + "=" * 70)
    print("PHASE 2: Analyzing Ownership Depth")
    print("=" * 70)
    
    ownership_analyses = []
    for project, narrative in parsed_projects:
        ownership = detect_ownership_level(
            project["description"],
            narrative.candidate_role
        )
        ownership_analyses.append(ownership)
        project["ownership"] = ownership
        
        print(f"\n{project['id']}:")
        print(f"  Ownership Level: {ownership.ownership_level.upper()}")
        print(f"  Action Verb Score: {ownership.action_verb_score:.2f}")
        print(f"  Is Vague: {ownership.is_vague}")
        print(f"  Evidence: '{ownership.evidence}'")
        print(f"  Confidence: {ownership.confidence:.2f}")
    
    # =====================================================================
    # PHASE 3: Evaluate Outcome Clarity
    # =====================================================================
    print("\n" + "=" * 70)
    print("PHASE 3: Evaluating Outcome Clarity")
    print("=" * 70)
    
    outcome_analyses = []
    for project, narrative in parsed_projects:
        clarity = score_outcome_clarity(narrative.outcome)
        outcome_analyses.append(clarity)
        project["clarity"] = clarity
        
        print(f"\n{project['id']}:")
        print(f"  Clarity Score: {clarity.clarity_score:.2f}")
        print(f"  Is Specific: {clarity.is_specific}")
        print(f"  Metrics Found: {len(clarity.measures_found)}")
        for measure in clarity.measures_found:
            print(f"    - {measure.value}{measure.unit}: {measure.full_statement}")
        print(f"  Summary: {clarity.summary}")
    
    # =====================================================================
    # PHASE 4: Assess Problem Complexity
    # =====================================================================
    print("\n" + "=" * 70)
    print("PHASE 4: Assessing Problem Complexity")
    print("=" * 70)
    
    complexity_analyses = []
    for project, narrative in parsed_projects:
        complexity = evaluate_complexity(
            project["description"],
            narrative.challenges_faced,
            narrative.outcome
        )
        complexity_analyses.append(complexity)
        project["complexity"] = complexity
        
        print(f"\n{project['id']}:")
        print(f"  Complexity Level: {complexity.complexity_level.upper()}")
        print(f"  Complexity Score: {complexity.complexity_score:.2f}")
        print(f"  Indicators Found: {len(complexity.indicators_found)}")
        for indicator in complexity.indicators_found:
            print(f"    - {indicator.indicator_type}: {indicator.description}")
        print(f"  Summary: {complexity.summary}")
    
    # =====================================================================
    # PHASE 5: Generate Skill Confidence Scores
    # =====================================================================
    print("\n" + "=" * 70)
    print("PHASE 5: Generating Skill Confidence Scores")
    print("=" * 70)
    
    # Extract skills mentioned in projects
    all_skills = set()
    for project in projects:
        skills = extract_skills_from_text(project["description"])
        all_skills.update(skills)
    
    print(f"\n[SUCCESS] Identified {len(all_skills)} unique technical skills")
    print(f"  Skills: {', '.join(sorted(all_skills)[:10])}")
    
    # Calculate confidence scores for each skill
    confidence_scores_by_skill = {}
    
    for project, narrative in parsed_projects:
        skills = extract_skills_from_text(project["description"])
        
        for skill in skills:
            if skill not in confidence_scores_by_skill:
                confidence_scores_by_skill[skill] = []
            
            confidence = calculate_confidence_score(
                skill,
                project["ownership"],
                project["clarity"],
                project["complexity"],
                project_count=1
            )
            confidence_scores_by_skill[skill].append(confidence)
    
    # Display confidence scores
    print(f"\n[SCORES] Skill Confidence Scores:")
    print("-" * 70)
    
    for skill in sorted(confidence_scores_by_skill.keys()):
        scores = confidence_scores_by_skill[skill]
        avg_score = sum(s.confidence_score for s in scores) / len(scores)
        
        print(f"\n  {skill}:")
        print(f"    Average Confidence: {avg_score:.1f}/100")
        print(f"    Proficiency: {scores[0].proficiency_level}")
        print(f"    Evidence Projects: {len(scores)}")
        print(f"    Summary: {scores[0].summary}")
    
    # =====================================================================
    # PHASE 6: Build Skill Graph
    # =====================================================================
    print("\n" + "=" * 70)
    print("PHASE 6: Building Skill Graph for Visualization")
    print("=" * 70)
    
    graph = build_skill_graph(confidence_scores_by_skill)
    
    print(f"\n[STATS] Skill Graph Statistics:")
    print(f"  - Total Skills (Nodes): {graph.stats['total_skills']}")
    print(f"  - Total Skill-Project Links (Edges): {graph.stats['total_edges']}")
    print(f"  - Average Skill Confidence: {graph.stats['average_skill_confidence']:.1f}/100")
    print(f"  - Projects Linked: {graph.stats['total_projects_linked']}")
    
    print(f"\n[TOP] Top Skills:")
    for i, skill in enumerate(graph.stats['top_skills'], 1):
        print(f"  {i}. {skill.name}: {skill.overall_confidence:.1f}/100 ({skill.proficiency_level})")
    
    # Convert graph to dictionary for visualization
    graph_dict = graph_to_dict(graph)
    print(f"\n[SUCCESS] Graph converted to frontend format ({len(json.dumps(graph_dict))} bytes)")
    
    # =====================================================================
    # PHASE 7: Generate Targeted Proof Cards
    # =====================================================================
    print("\n" + "=" * 70)
    print("PHASE 7: Generating Proof Cards for Target Opportunities")
    print("=" * 70)
    
    opportunities = [
        {
            "title": "Senior Backend Engineer - Real-time Systems",
            "description": """
            Seeking a senior backend engineer to lead our real-time data infrastructure.
            
            Required Skills:
            - Python (5+ years)
            - Distributed systems design
            - Kafka or similar event streaming
            - PostgreSQL
            
            Preferred Skills:
            - Kubernetes and containerization
            - System design at scale (millions of events/sec)
            - TensorFlow or ML infrastructure
            
            The role involves designing and implementing systems that process
            massive amounts of real-time data with strict latency requirements.
            """
        },
        {
            "title": "Full Stack Engineer - React & Python",
            "description": """
            Join our team as a full stack engineer combining frontend and backend expertise.
            
            Required: React, JavaScript, Python, REST APIs
            Preferred: WebSocket, Redux, performance optimization, Redis
            
            You'll work on both user-facing dashboards and backend systems.
            """
        }
    ]
    
    for opportunity in opportunities:
        print(f"\n[OPPORTUNITY] {opportunity['title']}")
        print(f"   {'-' * 66}")
        
        proof_card = generate_proof_card(
            graph,
            opportunity["description"],
            opportunity["title"],
            max_skills=5,
            min_confidence=50.0
        )
        
        print(f"\n   Relevance: {proof_card.total_relevance_score:.1f}/100")
        print(f"   Summary: {proof_card.summary}")
        
        print(f"\n   Matched Skills ({len(proof_card.matched_skills)}):")
        for skill in proof_card.matched_skills:
            print(f"   [MATCH] {skill.skill_name}")
            print(f"     Confidence: {skill.confidence_score:.1f}/100 ({skill.proficiency_level})")
            print(f"     Evidence: {skill.best_project_evidence}")
            print(f"     Project Evidence: {skill.project_count} project(s)")
        
        # Convert to dictionary format
        card_dict = proof_card_to_dict(proof_card)
        print(f"\n   Frontend format: {len(json.dumps(card_dict))} bytes")
    
    # =====================================================================
    # PHASE 8: Export Data
    # =====================================================================
    print("\n" + "=" * 70)
    print("PHASE 8: Data Export for Frontend Integration")
    print("=" * 70)
    
    # Export graph
    export_data = {
        "skillGraph": graph_dict,
        "opportunityProofCards": []
    }
    
    for opportunity in opportunities:
        proof_card = generate_proof_card(
            graph,
            opportunity["description"],
            opportunity["title"]
        )
        export_data["opportunityProofCards"].append(proof_card_to_dict(proof_card))
    
    # Save to file
    export_path = "agent_4_output.json"
    with open(export_path, "w") as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n[COMPLETE] Export complete!")
    print(f"  - File: agent_4_output.json")
    print(f"  - Size: {len(json.dumps(export_data, indent=2))} bytes")
    print(f"  - Format: Ready for frontend visualization")
    
    print("\n" + "=" * 70)
    print("\n[SUCCESS] Agent 4 Workflow Complete!")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_agent_4_workflow()
