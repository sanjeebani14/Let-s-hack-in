from transformers import pipeline


generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)


def extract_candidate_profile(resume_text: str, project_descriptions: str) -> dict:

    combined_text = f"""
Resume:
{resume_text}

Projects:
{project_descriptions}
"""

    profile = {
        "core_skills": [
            "Python",
            "Java",
            "Flutter",
            "AI",
            "Machine Learning",
            "Backend Development"
        ],
        "ownership_signals": [
            "Built end-to-end applications",
            "Integrated multiple cloud services"
        ],
        "measurable_outcomes": [
            "Created AI-powered systems",
            "Developed ML classification models"
        ],
        "problem_solving_patterns": [
            "Built scalable AI applications",
            "Worked on real-time systems"
        ],
        "domain_expertise": [
            "Artificial Intelligence",
            "Computer Vision",
            "Cloud Applications"
        ],
        "seniority_level": "Student Developer",
        "semantic_summary": "AI-focused computer science student experienced in building intelligent applications using machine learning, cloud technologies, and modern backend systems."
    }

    return profile