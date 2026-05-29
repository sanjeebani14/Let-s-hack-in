"""
FastAPI Application - Member B: The Opportunity Engine
Main orchestration endpoint that integrates Member A (Profile Extraction + Matching)
with Member B (Opportunity Discovery + Scoring).
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from member_a.profile_extractor import extract_candidate_profile
from member_a.relevance_matching import rank_opportunity_matches
from member_b.discovery_service import discover_opportunities as discover_live_opportunities
from member_b.scorer import rank_opportunities
from inroad_skill_pipeline import build_skill_graph_from_portfolio, build_proof_for_opportunity
from agent_5.assembler import assemble_outreach_package
from agent_3.context_detector import detect_shared_contexts
from agent_3.engagement import check_engagement_signals
from agent_3.connector import find_connector_persons
from agent_3.team_analyzer import analyze_team_composition
from agent_3.calculator import calculate_inroad_score
from agent_3.way_in import generate_way_in

# ============================================
# Setup Logging
# ============================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _model_to_dict(model: Any) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _build_outreach_summary(package: Any) -> "OutreachSummary":
    data = _model_to_dict(package)
    instructions = data.get("action_instructions", {})
    inst_list = instructions.get("instructions", []) if isinstance(instructions, dict) else []
    action_texts = [
        item.get("instruction", str(item)) if isinstance(item, dict) else str(item)
        for item in inst_list
    ]

    linkedin = data.get("enriched_linkedin_message") or data.get("linkedin_outreach", {}).get("message_body", "")
    email_primary = data.get("enriched_email_primary") or ""
    email_pkg = data.get("email_outreach", {}) or {}
    subject = ""
    if isinstance(email_pkg, dict) and email_pkg.get("primary_email"):
        subject = email_pkg["primary_email"].get("subject_line", "")

    return OutreachSummary(
        action_instructions=action_texts,
        linkedin_message=linkedin[:2000] if linkedin else "",
        email_subject=subject,
        email_body_preview=email_primary[:2000] if email_primary else "",
        recommended_order=data.get("recommended_order", []),
        estimated_total_time_minutes=data.get("estimated_total_time_minutes", 0),
    )

# ============================================
# Initialize FastAPI App
# ============================================
app = FastAPI(
    title="Opportunity Engine API",
    description="AI-powered candidate-opportunity matching system",
    version="1.0.0"
)

# ============================================
# CORS Middleware Configuration
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ============================================
# Pydantic Models for Request/Response
# ============================================

class AnalyzeRequest(BaseModel):
    """Request schema for the /analyze endpoint."""
    resume_text: str = Field(
        ...,
        description="Full resume/CV text of the candidate",
        min_length=10
    )
    project_descriptions: str = Field(
        ...,
        description="Descriptions of candidate's projects and work experience",
        min_length=10
    )
    candidate_name: Optional[str] = Field(
        default="Candidate",
        description="Display name for outreach generation",
        min_length=1,
        max_length=120,
    )


class ScoreDetail(BaseModel):
    """Detailed scoring breakdown for an opportunity."""
    competition_index: float
    response_probability: float
    growth_potential: float
    referral_likelihood: float
    opportunity_score: float
    score_reasoning: str


class MatchResult(BaseModel):
    """Individual opportunity match result."""
    opportunity_id: int
    title: str
    company: str
    source_type: str
    fit_score: float
    match_reasoning: str
    scores: ScoreDetail


class CandidateProfileResponse(BaseModel):
    """Extracted candidate profile summary."""
    core_skills: List[str]
    ownership_signals: List[str]
    measurable_outcomes: List[str]
    problem_solving_patterns: List[str]
    domain_expertise: List[str]
    seniority_level: str
    semantic_summary: str


class ChemistryAnalysis(BaseModel):
    """Agent 3: InRoad Chemistry analysis results."""
    inroad_score: float = Field(
        ...,
        description="Final combined InRoad Chemistry score (0-100)"
    )
    structural_explanation: str = Field(
        ...,
        description="One-line explanation of the InRoad score"
    )
    shared_contexts_count: int = Field(
        ...,
        description="Number of shared touchpoints detected"
    )
    shared_contexts_summary: str = Field(
        ...,
        description="Summary of shared contexts"
    )
    employee_interactions: List[Dict[str, Any]] = Field(
        ...,
        description="List of employee interactions with candidate's work"
    )
    engagement_strength: float = Field(
        ...,
        description="Engagement score (0.0-1.0)"
    )
    best_connector_name: str = Field(
        ...,
        description="Name of the best connector person"
    )
    best_connector_intro: str = Field(
        ...,
        description="How the best connector is related to candidate"
    )
    entry_probability: float = Field(
        ...,
        description="Probability of getting introduced (0.0-1.0)"
    )
    team_fit_category: str = Field(
        ...,
        description="Team composition fit: 'complements', 'neutral', or 'overlaps'"
    )
    team_chemistry_score: float = Field(
        ...,
        description="Team cultural fit score (0.0-1.0)"
    )
    way_in_strategy: str = Field(
        ...,
        description="Actionable entry strategy sentence"
    )
    way_in_confidence: float = Field(
        ...,
        description="Confidence in the entry strategy (0.0-1.0)"
    )


class ProofCardSummary(BaseModel):
    """Agent 4: skill proof for an opportunity."""
    opportunity_title: str
    summary: str
    total_relevance_score: float
    matched_skills: List[Dict[str, Any]]


class OutreachSummary(BaseModel):
    """Agent 5: outreach package summary for UI."""
    action_instructions: List[str]
    linkedin_message: str
    email_subject: str
    email_body_preview: str
    recommended_order: List[str]
    estimated_total_time_minutes: int


class EnhancedMatchResult(BaseModel):
    """Individual opportunity match result with chemistry analysis."""
    opportunity_id: int
    title: str
    company: str
    source_type: str
    fit_score: float
    match_reasoning: str
    scores: ScoreDetail
    chemistry: ChemistryAnalysis
    proof: ProofCardSummary
    outreach: OutreachSummary
    opportunity_url: Optional[str] = None


class AnalyzeResponse(BaseModel):
    """Response schema for the /analyze endpoint."""
    status: str = "success"
    timestamp: str
    candidate_profile: CandidateProfileResponse
    matched_opportunities: List[EnhancedMatchResult]
    summary: Dict[str, Any]


class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str
    engine: str
    timestamp: str


# ============================================
# Health Check Endpoint
# ============================================

@app.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for frontend verification.
    
    Returns:
        HealthResponse: Simple status confirmation
    """
    return {
        "status": "healthy",
        "engine": "Opportunity Engine Running",
        "timestamp": datetime.now().isoformat()
    }


# ============================================
# Master Analysis Endpoint
# ============================================

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_candidate(request: AnalyzeRequest):
    """
    Master analysis endpoint that orchestrates the full matching pipeline.
    
    Steps:
    1. Extract candidate profile from resume + projects (Member A)
    2. Rank opportunities by opportunity score (Member B)
    3. Match candidate profile with top opportunities (Member A)
    4. Aggregate and return unified response
    
    Args:
        request: AnalyzeRequest containing resume_text and project_descriptions
        
    Returns:
        AnalyzeResponse: Comprehensive analysis with profile, matches, and reasoning
        
    Raises:
        HTTPException: If processing fails at any stage
    """
    
    try:
        logger.info("Starting candidate analysis pipeline...")
        
        # ============================================
        # Step 1: Extract Candidate Profile
        # ============================================
        logger.info("Step 1: Extracting candidate profile...")
        try:
            candidate_profile = extract_candidate_profile(
                request.resume_text,
                request.project_descriptions
            )
            logger.info(f"Profile extracted successfully: {candidate_profile['seniority_level']}")
        except Exception as e:
            logger.error(f"Profile extraction failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to extract candidate profile: {str(e)}"
            )
        
        # ============================================
        # Step 2: Live discovery + rank opportunities
        # ============================================
        logger.info("Step 2: Discovering and ranking opportunities...")
        discovery_meta: Dict[str, Any] = {}
        try:
            discovery_result = discover_live_opportunities()
            all_opportunities = discovery_result["opportunities"]
            discovery_meta = {
                "discovery_mode": discovery_result["discovery_mode"],
                "source_status": discovery_result.get("source_status", {}),
            }

            if not all_opportunities:
                raise HTTPException(
                    status_code=503,
                    detail=(
                        "No opportunities discovered from live sources. "
                        "Check network, set GITHUB_TOKEN, or enable INROAD_ALLOW_MOCK_FALLBACK=true for dev only."
                    ),
                )

            top_opportunities = rank_opportunities(all_opportunities, top_k=3)
            logger.info(
                f"Ranked {len(top_opportunities)} top opportunities from {len(all_opportunities)} "
                f"(mode={discovery_meta['discovery_mode']})"
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Opportunity ranking failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to rank opportunities: {str(e)}"
            )

        # ============================================
        # Step 2b: Skill graph (Agent 4) from portfolio
        # ============================================
        logger.info("Step 2b: Building skill proof graph from portfolio...")
        try:
            skill_graph = build_skill_graph_from_portfolio(request.project_descriptions)
        except Exception as e:
            logger.error(f"Skill graph build failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to build skill proof graph: {str(e)}"
            )
        
        # ============================================
        # Step 3: Match Candidate with Top Opportunities
        # ============================================
        logger.info("Step 3: Matching candidate profile with opportunities...")
        try:
            match_results = rank_opportunity_matches(
                candidate_profile,
                top_opportunities
            )
            logger.info(f"Completed matching for {len(match_results)} opportunities")
        except Exception as e:
            logger.error(f"Opportunity matching failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to match opportunities: {str(e)}"
            )
        
        # ============================================
        # Step 4: Apply Agent 3 - InRoad Chemistry Analysis
        # ============================================
        logger.info("Step 4: Analyzing InRoad Chemistry for each opportunity...")
        try:
            matched_opportunities_list = []
            
            for match in match_results:
                opp = match["opportunity"]
                fit_score = match["fit_score"]
                
                # Step 4a: Detect shared contexts
                context_response = detect_shared_contexts(candidate_profile, opp)
                
                # Step 4b: Check engagement signals
                engagement_response = check_engagement_signals(candidate_profile, opp)
                
                # Step 4c: Find connector persons
                connector_response = find_connector_persons(candidate_profile, opp)
                
                # Step 4d: Analyze team composition
                team_analysis = analyze_team_composition(candidate_profile, opp)
                
                # Step 4e: Calculate InRoad score
                inroad_score = calculate_inroad_score(
                    fit_score,
                    context_response,
                    connector_response,
                    engagement_response,
                    opp.get("competition_index", 0.5),
                    opp
                )
                
                # Step 4f: Generate entry strategy
                way_in = generate_way_in(
                    candidate_profile,
                    opp,
                    context_response,
                    connector_response,
                    engagement_response,
                    team_analysis,
                    inroad_score
                )
                
                # Build chemistry analysis
                employee_interactions_list = []
                for interaction in engagement_response.interactions:
                    employee_interactions_list.append({
                        "person_name": interaction.person_name,
                        "person_role": interaction.person_role,
                        "interaction_type": interaction.interaction_type,
                        "interaction_detail": interaction.interaction_detail
                    })
                
                chemistry = ChemistryAnalysis(
                    inroad_score=inroad_score.inroad_score,
                    structural_explanation=inroad_score.structural_explanation,
                    shared_contexts_count=len(context_response.shared_contexts),
                    shared_contexts_summary=context_response.summary,
                    employee_interactions=employee_interactions_list,
                    engagement_strength=engagement_response.engagement_strength,
                    best_connector_name=connector_response.best_connector.person_name,
                    best_connector_intro=connector_response.best_connector.relationship_to_candidate,
                    entry_probability=connector_response.entry_probability,
                    team_fit_category=team_analysis.fit_category.value,
                    team_chemistry_score=team_analysis.chemistry_score,
                    way_in_strategy=way_in.actionable_sentence,
                    way_in_confidence=way_in.confidence
                )

                proof_dict = build_proof_for_opportunity(skill_graph, opp)
                proof_summary = ProofCardSummary(
                    opportunity_title=proof_dict.get("opportunity", {}).get("title", opp["title"]),
                    summary=proof_dict.get("match", {}).get("summary", ""),
                    total_relevance_score=float(proof_dict.get("match", {}).get("relevanceScore", 0)),
                    matched_skills=proof_dict.get("matched_skills", []),
                )

                shared_contexts_payload = [
                    {
                        "context_type": ctx.context_type,
                        "name": ctx.name,
                        "relevance_score": ctx.relevance_score,
                    }
                    for ctx in context_response.shared_contexts
                ]
                engagement_payload = [
                    {
                        "person_name": item.person_name,
                        "person_role": item.person_role,
                        "interaction_type": item.interaction_type,
                        "interaction_detail": item.interaction_detail,
                    }
                    for item in engagement_response.interactions
                ]
                connector_payload = {
                    "best_connector": {
                        "person_name": connector_response.best_connector.person_name,
                        "relationship_to_candidate": connector_response.best_connector.relationship_to_candidate,
                        "relationship_strength_to_candidate": connector_response.best_connector.relationship_strength_to_candidate,
                    },
                    "entry_probability": connector_response.entry_probability,
                }
                way_in_payload = {
                    "actionable_sentence": way_in.actionable_sentence,
                    "primary_signal": way_in.primary_signal,
                    "confidence": way_in.confidence,
                }

                outreach_package = assemble_outreach_package(
                    opportunity_title=opp["title"],
                    candidate_name=request.candidate_name or "Candidate",
                    inroad_score=inroad_score.inroad_score,
                    way_in_strategy=way_in_payload,
                    shared_contexts=shared_contexts_payload,
                    engagement_signals=engagement_payload,
                    connector_data=connector_payload,
                    proof_card=proof_dict,
                    opportunity_data=opp,
                )
                outreach_summary = _build_outreach_summary(outreach_package)
                
                matched_opportunities_list.append(
                    EnhancedMatchResult(
                        opportunity_id=opp["id"],
                        title=opp["title"],
                        company=opp["company"],
                        source_type=opp["source_type"],
                        fit_score=fit_score,
                        match_reasoning=match["match_reasoning"],
                        scores=ScoreDetail(
                            competition_index=opp["competition_index"],
                            response_probability=opp["response_probability"],
                            growth_potential=opp["growth_potential"],
                            referral_likelihood=opp["referral_likelihood"],
                            opportunity_score=opp["opportunity_score"],
                            score_reasoning=opp["score_reasoning"]
                        ),
                        chemistry=chemistry,
                        proof=proof_summary,
                        outreach=outreach_summary,
                        opportunity_url=opp.get("url"),
                    )
                )
            
            logger.info(f"Chemistry analysis completed for {len(matched_opportunities_list)} opportunities")
        except Exception as e:
            logger.error(f"Chemistry analysis failed: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze chemistry: {str(e)}"
            )
        
        # ============================================
        # Step 5: Aggregate Results
        # ============================================
        logger.info("Step 5: Aggregating final results...")
        try:
            # Calculate summary statistics
            fit_scores = [m.fit_score for m in matched_opportunities_list]
            chemistry_scores = [m.chemistry.inroad_score for m in matched_opportunities_list]
            avg_fit = sum(fit_scores) / len(fit_scores) if fit_scores else 0
            avg_chemistry = sum(chemistry_scores) / len(chemistry_scores) if chemistry_scores else 0
            
            summary = {
                "total_opportunities_evaluated": len(all_opportunities),
                "top_opportunities_matched": len(matched_opportunities_list),
                "average_fit_score": round(avg_fit, 2),
                "highest_fit_score": round(max(fit_scores), 2) if fit_scores else 0,
                "average_chemistry_score": round(avg_chemistry, 2),
                "highest_chemistry_score": round(max(chemistry_scores), 2) if chemistry_scores else 0,
                "seniority_level": candidate_profile["seniority_level"],
                "primary_domain": candidate_profile["domain_expertise"][0] if candidate_profile["domain_expertise"] else "General",
                "discovery_mode": discovery_meta.get("discovery_mode"),
                "discovery_sources": discovery_meta.get("source_status"),
            }
            
            logger.info("Analysis pipeline completed successfully")
            
            return AnalyzeResponse(
                status="success",
                timestamp=datetime.now().isoformat(),
                candidate_profile=CandidateProfileResponse(
                    core_skills=candidate_profile["core_skills"],
                    ownership_signals=candidate_profile["ownership_signals"],
                    measurable_outcomes=candidate_profile["measurable_outcomes"],
                    problem_solving_patterns=candidate_profile["problem_solving_patterns"],
                    domain_expertise=candidate_profile["domain_expertise"],
                    seniority_level=candidate_profile["seniority_level"],
                    semantic_summary=candidate_profile["semantic_summary"]
                ),
                matched_opportunities=matched_opportunities_list,
                summary=summary
            )
        
        except Exception as e:
            logger.error(f"Result aggregation failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to aggregate results: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analysis pipeline: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during analysis. Please try again."
        )


# ============================================
# Error Handlers
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return {
        "status": "error",
        "detail": exc.detail,
        "status_code": exc.status_code
    }


# ============================================
# Application Entry Point
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Opportunity Engine API server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
