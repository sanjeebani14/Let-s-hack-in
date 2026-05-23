"""
Agent 3 — InRoad Chemistry Engine

Maps human pathways and cultural alignment between candidates and opportunity teams
using deterministic matching and heuristic scoring.

Components:
  - context_detector: Finds shared touchpoints (communities, hackathons, repos)
  - engagement: Checks employee interactions with candidate's work
  - connector: Finds second-degree connections (bridges)
  - team_analyzer: Compares seniority and working style
  - calculator: Combines signals into final InRoad score
  - way_in: Generates actionable sentence for entry strategy
"""

from .context_detector import (
    SharedContext,
    ContextDetectorResponse,
    detect_shared_contexts,
)
from .engagement import (
    EmployeeInteraction,
    EngagementResponse,
    check_engagement_signals,
)
from .connector import (
    ConnectorPerson,
    ConnectorResponse,
    find_connector_persons,
)
from .team_analyzer import (
    TeamFitCategory,
    TeamCompositionAnalysis,
    analyze_team_composition,
)
from .calculator import (
    InRoadScore,
    calculate_inroad_score,
)
from .way_in import (
    WayInStrategy,
    generate_way_in,
)

__all__ = [
    "SharedContext",
    "ContextDetectorResponse",
    "detect_shared_contexts",
    "EmployeeInteraction",
    "EngagementResponse",
    "check_engagement_signals",
    "ConnectorPerson",
    "ConnectorResponse",
    "find_connector_persons",
    "TeamFitCategory",
    "TeamCompositionAnalysis",
    "analyze_team_composition",
    "InRoadScore",
    "calculate_inroad_score",
    "WayInStrategy",
    "generate_way_in",
]
