# Tests matching agent with mock profile and mock opportunities — Owner: Member A
from member_a.profile_extractor import extract_candidate_profile
from member_a.relevance_matching import rank_opportunity_matches


def test_rank_opportunity_matches():
    resume_text = """
    B.Tech Computer Science student skilled in Python, Java, Flutter, AI, backend development, and cloud services.
    Built AI-powered applications using OpenAI, AWS, Firebase, and machine learning models.
    """

    project_descriptions = """
    MyKindBuddy: Built an AI-powered journaling app using Flutter, AWS Lambda, Cognito, DynamoDB, OpenAI GPT-4, and sentiment analysis.
    Project Drishti: Built an AI situational awareness platform using Vertex AI Vision, Gemini, and Firebase for public event safety.
    Vehicle Image Classification: Built an SVM-based ML model for vehicle image classification.
    """

    opportunities = [
        {
            "title": "AI Product Intern",
            "company": "MindLoop AI",
            "description": "Early-stage startup building AI mental wellness assistants. Looking for Flutter, AI chatbot, backend API, and sentiment analysis experience.",
            "stage": "Seed",
            "team_size": 8,
            "source_type": "Founder post"
        },
        {
            "title": "Frontend Intern",
            "company": "DashGrid",
            "description": "Startup building React dashboards for business analytics.",
            "stage": "Series A",
            "team_size": 35,
            "source_type": "Employee post"
        }
    ]

    candidate_profile = extract_candidate_profile(resume_text, project_descriptions)

    matches = rank_opportunity_matches(candidate_profile, opportunities)

    assert isinstance(matches, list)
    assert len(matches) == len(opportunities)

    for match in matches:
        assert "opportunity" in match
        assert "fit_score" in match
        assert "match_reasoning" in match
        assert isinstance(match["fit_score"], float)
        assert 0 <= match["fit_score"] <= 100
        assert isinstance(match["match_reasoning"], str)
        assert len(match["match_reasoning"]) > 0

    assert matches[0]["fit_score"] >= matches[1]["fit_score"]