"""
Member B - Mock Opportunity Dataset
Realistic hidden job/internship opportunities for AI and backend engineers.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta


def get_mock_opportunities() -> List[Dict[str, Any]]:
    """
    Returns a dataset of 10 highly realistic, 'hidden' job/internship opportunities.
    Each opportunity varies in source type and represents real-world hidden channels.
    
    Returns:
        List[Dict]: Collection of opportunity objects with required fields
    """
    
    opportunities = [
        {
            "id": 1,
            "title": "AI/ML Engineer - Early Stage",
            "company": "NeuralFlow Startup",
            "source_type": "founder_post",
            "description": "We're building an edge AI inference platform. Looking for an engineer experienced with TensorFlow and model optimization. Fully remote, equity heavy. Current team: 3 engineers + founder.",
            "team_size": 4,
            "stage": "seed",
            "posted_date": "2026-05-15"
        },
        {
            "id": 2,
            "title": "Backend Engineer - Python/FastAPI",
            "company": "DataFlow Collective",
            "source_type": "newsletter",
            "description": "Building data pipelines for climate tech. We use FastAPI, PostgreSQL, and async Python. Looking for someone who loves writing elegant, scalable backend code. Distributed team across 3 time zones.",
            "team_size": 8,
            "stage": "series_a",
            "posted_date": "2026-05-12"
        },
        {
            "id": 3,
            "title": "ML Infrastructure Intern",
            "company": "QuantumAI Labs",
            "source_type": "github_repo",
            "description": "Looking for an intern to help optimize our ML inference infrastructure. Open to hands-on work with Kubernetes, Docker, and PyTorch. Paid internship, 3-4 months flexible.",
            "team_size": 6,
            "stage": "series_b",
            "posted_date": "2026-05-18"
        },
        {
            "id": 4,
            "title": "Full Stack AI Developer",
            "company": "VisionTech Inc",
            "source_type": "employee_post",
            "description": "Our team is growing! We're hiring for someone who can build both ML models and production APIs. Python, React, cloud deployment. Company culture is very collaborative.",
            "team_size": 12,
            "stage": "series_b",
            "posted_date": "2026-05-10"
        },
        {
            "id": 5,
            "title": "Hackathon + Job Opportunity - AI/Web3",
            "company": "ChainML Venture Lab",
            "source_type": "hackathon",
            "description": "Participate in our 48-hour hackathon (May 30-June 1). Top 3 projects get offers. We're exploring ML + blockchain. Need Python backend and some ML experience.",
            "team_size": 15,
            "stage": "seed",
            "posted_date": "2026-05-08"
        },
        {
            "id": 6,
            "title": "Senior Backend Engineer - Distributed Systems",
            "company": "Infra Dynamics",
            "source_type": "founder_post",
            "description": "Building the next-gen distributed database. Hiring for backend engineers with experience in Go/Rust/Python. This is a deep technical role. Remote, competitive equity.",
            "team_size": 10,
            "stage": "series_a",
            "posted_date": "2026-05-14"
        },
        {
            "id": 7,
            "title": "AI Safety Research Engineer",
            "company": "AlignmentFirst",
            "source_type": "newsletter",
            "description": "We work on AI safety and alignment research. Looking for engineers who can help build tools for interpretability and evaluation. Python, some ML knowledge required.",
            "team_size": 7,
            "stage": "non_profit",
            "posted_date": "2026-05-16"
        },
        {
            "id": 8,
            "title": "Contract AI Engineer - 3 Month Project",
            "company": "Creative Studios XYZ",
            "source_type": "employee_post",
            "description": "We need someone to build a custom computer vision pipeline for our creative platform. 3-month contract, 30-40 hrs/week. Budget is there for the right person.",
            "team_size": 3,
            "stage": "bootstrapped",
            "posted_date": "2026-05-11"
        },
        {
            "id": 9,
            "title": "ML Platform Engineer",
            "company": "EdgeML Systems",
            "source_type": "github_repo",
            "description": "Open-source project turned product. We're hiring core maintainers. Work on ML model serving, optimization, and inference. Equity + salary in Y-combinator backed startup.",
            "team_size": 5,
            "stage": "series_a",
            "posted_date": "2026-05-13"
        },
        {
            "id": 10,
            "title": "Backend + Data Infrastructure Hybrid Role",
            "company": "DataVault Security",
            "source_type": "founder_post",
            "description": "Hybrid backend and data engineering role. Build APIs and data pipelines for secure data management. Python, SQL, some DevOps knowledge. Remote, serious team.",
            "team_size": 9,
            "stage": "series_a",
            "posted_date": "2026-05-09"
        }
    ]
    
    return opportunities
