"""
Connector Person Finder

Evaluates second-degree connection nodes. Identifies individuals who bridge
the candidate's network and the target company.
Returns connector's name, relationship to candidate, and relationship to company.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any


class ConnectorPerson(BaseModel):
    """A second-degree connection that bridges candidate and target company."""
    person_name: str = Field(
        ...,
        description="Name of the connector person",
        examples=["David Lee", "Maria Garcia"]
    )
    relationship_to_candidate: str = Field(
        ...,
        description="How they're connected to the candidate",
        examples=["Former classmate at MIT", "Collaborated on open-source project", "Mentor from hackathon"]
    )
    relationship_strength_to_candidate: float = Field(
        ...,
        description="Strength of connection to candidate (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    relationship_to_company: str = Field(
        ...,
        description="How they're connected to the target company",
        examples=["Works as Senior Engineer", "Founded the company", "On advisory board"]
    )
    relationship_strength_to_company: float = Field(
        ...,
        description="Strength of connection to company (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    introduction_likelihood: float = Field(
        ...,
        description="Likelihood they would introduce candidate to company (0.0-1.0)",
        ge=0.0,
        le=1.0
    )


class ConnectorResponse(BaseModel):
    """Response from connector person finding."""
    connectors: List[ConnectorPerson] = Field(
        ...,
        description="List of identified second-degree connections"
    )
    best_connector: ConnectorPerson = Field(
        ...,
        description="Highest-value connector for introduction"
    )
    entry_probability: float = Field(
        ...,
        description="Overall probability of getting introduction through connectors (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    summary: str = Field(
        ...,
        description="One-line summary of available connectors"
    )


def find_connector_persons(
    candidate_profile: Dict[str, Any],
    opportunity_data: Dict[str, Any]
) -> ConnectorResponse:
    """
    Identify second-degree connections bridging candidate and target company.
    
    Args:
        candidate_profile: Extracted candidate profile (from Member A)
        opportunity_data: Full opportunity data including target company
        
    Returns:
        ConnectorResponse: List of connectors with introduction likelihood
    """
    
    # Mock connector database
    # In real scenario, this would query LinkedIn, internal referral databases, etc.
    mock_connectors_db = {
        "NeuralFlow Startup": [
            {
                "person_name": "Michael Zhang",
                "relationship_to_candidate": "Was your mentor at AI Bootcamp 2024",
                "relationship_strength_to_candidate": 0.8,
                "relationship_to_company": "Works as Senior ML Engineer at NeuralFlow",
                "relationship_strength_to_company": 0.9,
                "introduction_likelihood": 0.85
            },
            {
                "person_name": "Priya Sharma",
                "relationship_to_candidate": "Collaborated on PyTorch open-source contributions",
                "relationship_strength_to_candidate": 0.65,
                "relationship_to_company": "Backend Engineer, close friends with CTO",
                "relationship_strength_to_company": 0.75,
                "introduction_likelihood": 0.72
            }
        ],
        "DataFlow Collective": [
            {
                "person_name": "Tom Anderson",
                "relationship_to_candidate": "Your college roommate from Stanford",
                "relationship_to_candidate_strength": 0.95,
                "relationship_to_company": "Co-founder and VP Product at DataFlow",
                "relationship_strength_to_company": 1.0,
                "introduction_likelihood": 0.95
            }
        ],
        "QuantumAI Labs": [
            {
                "person_name": "Dr. Yuki Tanaka",
                "relationship_to_candidate": "Reviewed your research paper at conference",
                "relationship_strength_to_candidate": 0.55,
                "relationship_to_company": "Head of Research at QuantumAI",
                "relationship_strength_to_company": 0.9,
                "introduction_likelihood": 0.60
            },
            {
                "person_name": "Nathan Brooks",
                "relationship_to_candidate": "Shared workspace at co-working space, frequent collaborator",
                "relationship_strength_to_candidate": 0.7,
                "relationship_to_company": "ML Infrastructure Lead",
                "relationship_strength_to_company": 0.8,
                "introduction_likelihood": 0.78
            }
        ],
        "VisionTech Inc": [
            {
                "person_name": "Jessica Chen",
                "relationship_to_candidate": "Former colleague at TechCorp internship",
                "relationship_strength_to_candidate": 0.6,
                "relationship_to_company": "Tech Lead, Backend at VisionTech",
                "relationship_strength_to_company": 0.85,
                "introduction_likelihood": 0.75
            }
        ],
        "default": []
    }
    
    company_name = opportunity_data.get("company", "")
    connectors_data = mock_connectors_db.get(company_name, mock_connectors_db["default"])
    
    # Convert to ConnectorPerson objects
    connectors = []
    for conn in connectors_data:
        connector = ConnectorPerson(
            person_name=conn["person_name"],
            relationship_to_candidate=conn["relationship_to_candidate"],
            relationship_strength_to_candidate=conn.get(
                "relationship_strength_to_candidate",
                conn.get("relationship_to_candidate_strength", 0.5)
            ),
            relationship_to_company=conn["relationship_to_company"],
            relationship_strength_to_company=conn["relationship_strength_to_company"],
            introduction_likelihood=conn["introduction_likelihood"]
        )
        connectors.append(connector)
    
    # Find best connector (highest introduction_likelihood)
    best_connector = (
        max(connectors, key=lambda c: c.introduction_likelihood)
        if connectors
        else ConnectorPerson(
            person_name="No direct connectors found",
            relationship_to_candidate="N/A",
            relationship_strength_to_candidate=0.0,
            relationship_to_company="N/A",
            relationship_strength_to_company=0.0,
            introduction_likelihood=0.0
        )
    )
    
    # Calculate overall entry probability
    if connectors:
        entry_probability = sum(
            c.introduction_likelihood for c in connectors
        ) / len(connectors)
    else:
        entry_probability = 0.0
    
    # Generate summary
    if connectors:
        summary = f"{len(connectors)} connectors identified; {best_connector.person_name} is the strongest bridge"
    else:
        summary = "No direct connectors identified, but opportunities to build network"
    
    return ConnectorResponse(
        connectors=connectors,
        best_connector=best_connector,
        entry_probability=entry_probability,
        summary=summary
    )
