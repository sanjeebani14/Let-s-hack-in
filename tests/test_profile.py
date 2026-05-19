# Tests profile extraction with sample resume and projects — Owner: Member A
from member_a.profile_extractor import extract_candidate_profile


def test_extract_candidate_profile():
    resume_text = """
    B.Tech Computer Science student skilled in Python, Java, Flutter, AI, backend development, and cloud services.
    Built AI-powered applications using OpenAI, AWS, Firebase, and machine learning models.
    """

    project_descriptions = """
    MyKindBuddy: Built an AI-powered journaling app using Flutter, AWS Lambda, Cognito, DynamoDB, OpenAI GPT-4, and sentiment analysis.
    Project Drishti: Built an AI situational awareness platform using Vertex AI Vision, Gemini, and Firebase for public event safety.
    Vehicle Image Classification: Built an SVM-based ML model for vehicle image classification.
    """

    profile = extract_candidate_profile(resume_text, project_descriptions)

    assert isinstance(profile, dict)
    assert "core_skills" in profile
    assert "ownership_signals" in profile
    assert "measurable_outcomes" in profile
    assert "problem_solving_patterns" in profile
    assert "domain_expertise" in profile
    assert "seniority_level" in profile
    assert "semantic_summary" in profile

    assert isinstance(profile["core_skills"], list)
    assert isinstance(profile["semantic_summary"], str)
    assert len(profile["semantic_summary"]) > 0