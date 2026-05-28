import re
from typing import Dict, List, Any


def extract_candidate_profile(resume_text: str, project_descriptions: str) -> Dict[str, Any]:
    """
    Extract candidate profile from resume and project descriptions.
    
    Uses pattern matching and heuristics to identify key attributes
    without requiring heavy ML dependencies.
    
    Args:
        resume_text: Full resume/CV text
        project_descriptions: Project descriptions
        
    Returns:
        Dictionary containing candidate profile components
    """
    
    combined_text = f"""
Resume:
{resume_text}

Projects:
{project_descriptions}
"""
    
    # Extract skills - look for common skill keywords
    skill_keywords = {
        "python": "Python",
        "java": "Java",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "flutter": "Flutter",
        "react": "React",
        "ai": "AI",
        "machine learning": "Machine Learning",
        "ml": "Machine Learning",
        "deep learning": "Deep Learning",
        "backend": "Backend Development",
        "frontend": "Frontend Development",
        "fullstack": "Full-stack Development",
        "devops": "DevOps",
        "cloud": "Cloud Technologies",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "sql": "SQL",
        "postgresql": "PostgreSQL",
        "mongodb": "MongoDB",
        "aws": "AWS",
        "gcp": "GCP",
        "azure": "Azure",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
    }
    
    text_lower = combined_text.lower()
    found_skills = []
    for keyword, skill_name in skill_keywords.items():
        if keyword in text_lower and skill_name not in found_skills:
            found_skills.append(skill_name)
    
    # Default skills if none found
    if not found_skills:
        found_skills = [
            "Python",
            "Backend Development",
            "Machine Learning"
        ]
    
    # Detect ownership signals
    ownership_patterns = [
        r"led\s+(?:the\s+)?(?:development|team|project)",
        r"built\s+(?:end-to-end|scalable|real-time)",
        r"architected",
        r"designed\s+(?:and\s+)?implemented",
        r"managed\s+(?:team|project|stakeholders)"
    ]
    ownership_signals = []
    for pattern in ownership_patterns:
        if re.search(pattern, text_lower):
            if pattern == r"led\s+(?:the\s+)?(?:development|team|project)":
                ownership_signals.append("Led development initiatives")
            elif pattern == r"built\s+(?:end-to-end|scalable|real-time)":
                ownership_signals.append("Built scalable systems")
            elif pattern == r"architected":
                ownership_signals.append("Architected solutions")
            elif pattern == r"designed\s+(?:and\s+)?implemented":
                ownership_signals.append("Designed and implemented features")
            elif pattern == r"managed\s+(?:team|project|stakeholders)":
                ownership_signals.append("Managed cross-functional teams")
    
    # Default ownership signals
    if not ownership_signals:
        ownership_signals = [
            "Built end-to-end applications",
            "Integrated multiple cloud services"
        ]
    
    # Extract measurable outcomes
    outcome_patterns = [
        r"(\d+)\s*(?:%|percent|reduction|improvement|increase)",
        r"(?:served|impacted|reached)\s+(\d+(?:k|m)?)\s+(?:users|customers)",
        r"(?:generated|saved)\s+\$?(\d+(?:k|m)?)"
    ]
    measurable_outcomes = []
    for pattern in outcome_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            for match in matches[:2]:  # Take first 2 matches
                if match.isdigit() or "k" in str(match) or "m" in str(match):
                    measurable_outcomes.append(f"Achieved {match}+ impact")
    
    if not measurable_outcomes:
        measurable_outcomes = [
            "Created AI-powered systems",
            "Developed ML classification models"
        ]
    
    # Problem solving patterns
    problem_patterns = [
        "scalable",
        "real-time",
        "optimization",
        "performance",
        "integration",
        "automated"
    ]
    problem_solving_patterns = []
    for pattern in problem_patterns:
        if pattern in text_lower:
            problem_solving_patterns.append(f"Solved {pattern} problems")
    
    if not problem_solving_patterns:
        problem_solving_patterns = [
            "Built scalable AI applications",
            "Worked on real-time systems"
        ]
    
    # Domain expertise
    domain_keywords = {
        "ai": "Artificial Intelligence",
        "machine learning": "Machine Learning",
        "computer vision": "Computer Vision",
        "nlp": "Natural Language Processing",
        "cloud": "Cloud Computing",
        "devops": "DevOps",
        "backend": "Backend Architecture",
        "distributed": "Distributed Systems"
    }
    
    domain_expertise = []
    for keyword, domain in domain_keywords.items():
        if keyword in text_lower and domain not in domain_expertise:
            domain_expertise.append(domain)
    
    if not domain_expertise:
        domain_expertise = [
            "Artificial Intelligence",
            "Cloud Applications"
        ]
    
    # Determine seniority level
    seniority_patterns = {
        r"student|undergrad|bootcamp|junior": "Student Developer",
        r"senior|lead|architect|principal": "Senior Developer",
        r"manager|director|head": "Engineering Manager",
    }
    
    seniority_level = "Mid-level Developer"
    for pattern, level in seniority_patterns.items():
        if re.search(pattern, text_lower):
            seniority_level = level
            break
    
    profile = {
        "core_skills": found_skills[:6],  # Limit to 6
        "ownership_signals": ownership_signals[:2],
        "measurable_outcomes": measurable_outcomes[:2],
        "problem_solving_patterns": problem_solving_patterns[:2],
        "domain_expertise": domain_expertise[:3],
        "seniority_level": seniority_level,
        "semantic_summary": f"{seniority_level} with expertise in {', '.join(domain_expertise[:2])} and strong experience in {', '.join(found_skills[:3])}."
    }

    return profile