"""
FastAPI Application - Member B: The Opportunity Engine
Main orchestration endpoint that integrates Member A (Profile Extraction + Matching)
with Member B (Opportunity Discovery + Scoring).
"""

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_PATH)

from auth.dependencies import get_current_user, require_auth
from auth.firebase import (
    get_public_firebase_config,
    init_firebase,
    is_firebase_admin_configured,
    is_firebase_client_configured,
    set_user_role,
    VALID_ROLES,
)
from auth.profile_store import (
    create_user_on_register,
    get_user_profile,
    save_user_profile,
)
from member_a.profile_extractor import extract_candidate_profile
from member_a.resume_parser import extract_structured_sections, extract_text_from_file
from member_a.relevance_matching import rank_opportunity_matches
from member_b.dataset import get_mock_opportunities
from member_b.scorer import rank_opportunities
from agent_3.context_detector import detect_shared_contexts
from agent_3.engagement import check_engagement_signals
from agent_3.connector import find_connector_persons
from agent_3.team_analyzer import analyze_team_composition
from agent_3.calculator import calculate_inroad_score
from agent_3.way_in import generate_way_in
from agent_4 import (
    parse_project_narrative,
    detect_ownership_level,
    score_outcome_clarity,
    evaluate_complexity,
    calculate_confidence_score,
    build_skill_graph,
    generate_proof_card,
    proof_card_to_dict
)
from agent_5.assembler import assemble_outreach_package

# ============================================
# Setup Logging
# ============================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    allow_origins=["*", "http://localhost:5173", "http://localhost:5174"],  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ============================================
# Pydantic Models for Request/Response
# ============================================

class ExperienceEntry(BaseModel):
    title: str = ""
    company: str = ""
    duration: str = ""
    description: str = ""


class AnalyzeRequest(BaseModel):
    """Request schema for the /analyze endpoint."""
    resume_text: str = Field(
        ...,
        description="Full resume/CV text of the candidate",
        min_length=10
    )
    project_descriptions: str = Field(
        default="",
        description="Descriptions of candidate's projects and work experience",
    )
    skills: List[str] = Field(default_factory=list)
    experiences: List[ExperienceEntry] = Field(default_factory=list)
    internships: List[ExperienceEntry] = Field(default_factory=list)
    projects: List[ExperienceEntry] = Field(default_factory=list)


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
    skills: List[str] = Field(default_factory=list)
    experiences: List[ExperienceEntry] = Field(default_factory=list)
    internships: List[ExperienceEntry] = Field(default_factory=list)
    projects: List[ExperienceEntry] = Field(default_factory=list)


class AuthSyncRequest(BaseModel):
    role: str = Field(..., description="student | recruiter | admin")
    display_name: str = ""


class UserProfileUpdate(BaseModel):
    skills: List[str] = Field(default_factory=list)
    experiences: List[ExperienceEntry] = Field(default_factory=list)
    internships: List[ExperienceEntry] = Field(default_factory=list)
    resume_text: str = ""
    project_descriptions: str = ""
    display_name: str = ""


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


class OutreachRequest(BaseModel):
    """Generate outreach content for a matched opportunity."""
    opportunity_id: int
    candidate_name: str = Field(default="Candidate", min_length=1)
    opportunity: Dict[str, Any] = Field(
        ...,
        description="Matched opportunity object from /analyze response",
    )
    candidate_profile: Optional[Dict[str, Any]] = None


# ============================================
# Health Check Endpoint
# ============================================

@app.on_event("startup")
async def startup_firebase():
    init_firebase()


@app.get("/api/config/firebase")
async def firebase_client_config():
    """Public Firebase web config for the frontend SDK."""
    config = get_public_firebase_config()
    return {
        "configured": is_firebase_client_configured(),
        "admin_configured": is_firebase_admin_configured(),
        "config": config,
        "roles": sorted(VALID_ROLES),
    }


@app.post("/api/auth/sync")
async def sync_auth_user(
    body: AuthSyncRequest,
    user: dict = Depends(require_auth),
):
    """
    After Firebase sign-up/sign-in, sync role to Firestore and custom claims.
    """
    role = body.role.lower().strip()
    if role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail=f"Invalid role. Use: {', '.join(VALID_ROLES)}")

    profile = create_user_on_register(
        user["uid"],
        user.get("email") or "",
        role,
        body.display_name,
    )
    if is_firebase_admin_configured():
        set_user_role(user["uid"], role)

    return {"status": "ok", "user": profile}


@app.get("/api/profile")
async def read_profile(user: dict = Depends(require_auth)):
    profile = get_user_profile(user["uid"])
    if profile:
        return {"status": "ok", "profile": profile}
    return {
        "status": "ok",
        "profile": {
            "uid": user["uid"],
            "email": user.get("email"),
            "role": user.get("role", "student"),
            "skills": [],
            "experiences": [],
            "internships": [],
            "projects": [],
            "resume_text": "",
            "project_descriptions": "",
        },
    }


@app.put("/api/profile")
async def update_profile(
    body: UserProfileUpdate,
    user: dict = Depends(require_auth),
):
    try:
        saved = save_user_profile(
            user["uid"],
            user.get("email") or "",
            body.model_dump(),
        )
        return {"status": "ok", "profile": saved}
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Profile storage unavailable. Configure Firebase credentials.",
        )


@app.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user: Optional[dict] = Depends(get_current_user),
):
    """Upload resume file; return extracted text and structured sections."""
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    try:
        resume_text = extract_text_from_file(file.filename or "resume.txt", content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if len(resume_text) < 20:
        raise HTTPException(
            status_code=400,
            detail="Could not extract enough text from the file.",
        )

    structured = extract_structured_sections(resume_text)
    candidate_profile = extract_candidate_profile(
        resume_text,
        "",
        extra_skills=structured.get("skills"),
        experiences=structured.get("experiences"),
        internships=structured.get("internships"),
    )

    if user and user.get("uid"):
        try:
            save_user_profile(
                user["uid"],
                user.get("email") or "",
                {
                    "resume_text": resume_text,
                    "skills": structured.get("skills", []),
                    "experiences": structured.get("experiences", []),
                    "internships": structured.get("internships", []),
                    "projects": structured.get("projects", []),
                },
            )
        except RuntimeError:
            pass

    return {
        "status": "ok",
        "filename": file.filename,
        "resume_text": resume_text,
        "skills": structured.get("skills", []),
        "experiences": structured.get("experiences", []),
        "internships": structured.get("internships", []),
        "projects": structured.get("projects", []),
        "candidate_profile": candidate_profile,
    }


@app.get("/api/health", response_model=HealthResponse)
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
async def analyze_candidate(
    request: AnalyzeRequest,
    user: Optional[dict] = Depends(get_current_user),
):
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
            exp_dicts = [e.model_dump() for e in request.experiences]
            intern_dicts = [e.model_dump() for e in request.internships]
            project_text = request.project_descriptions or _build_projects_from_entries(
                exp_dicts, intern_dicts
            )
            candidate_profile = extract_candidate_profile(
                request.resume_text,
                project_text,
                extra_skills=request.skills,
                experiences=exp_dicts,
                internships=intern_dicts,
            )
            if user and user.get("uid"):
                try:
                    save_user_profile(
                        user["uid"],
                        user.get("email") or "",
                        {
                            "resume_text": request.resume_text,
                            "project_descriptions": project_text,
                            "skills": request.skills or candidate_profile.get("skills", []),
                            "experiences": exp_dicts,
                            "internships": intern_dicts,
                        },
                    )
                except RuntimeError:
                    pass
            logger.info(f"Profile extracted successfully: {candidate_profile['seniority_level']}")
        except Exception as e:
            logger.error(f"Profile extraction failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to extract candidate profile: {str(e)}"
            )
        
        # ============================================
        # Step 2: Get Top 3 Opportunities via Ranking
        # ============================================
        logger.info("Step 2: Discovering and ranking opportunities...")
        try:
            all_opportunities = get_mock_opportunities()
            top_opportunities = rank_opportunities(
                all_opportunities,
                top_k=3
            )
            logger.info(f"Ranked {len(top_opportunities)} top opportunities from {len(all_opportunities)} total")
        except Exception as e:
            logger.error(f"Opportunity ranking failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to rank opportunities: {str(e)}"
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
                        chemistry=chemistry
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
                "primary_domain": candidate_profile["domain_expertise"][0] if candidate_profile["domain_expertise"] else "General"
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
                    semantic_summary=candidate_profile["semantic_summary"],
                    skills=candidate_profile.get("skills", []),
                    experiences=[
                        ExperienceEntry(**e) for e in candidate_profile.get("experiences", [])
                    ],
                    internships=[
                        ExperienceEntry(**e) for e in candidate_profile.get("internships", [])
                    ],
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
# Outreach Generation Endpoint (Agent 5)
# ============================================

def _build_projects_from_entries(
    experiences: List[Dict[str, Any]],
    internships: List[Dict[str, Any]],
) -> str:
    """Synthesize project descriptions from structured work history."""
    lines = []
    for exp in experiences + internships:
        title = exp.get("title", "")
        company = exp.get("company", "")
        desc = exp.get("description", "")
        if title or company:
            lines.append(f"- {title} at {company}: {desc}".strip())
    return "\n".join(lines) if lines else "General professional experience from resume."


def _build_proof_card_from_profile(
    opportunity: Dict[str, Any],
    profile: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build a proof card using Agent 4."""
    profile = profile or {}
    
    # Extract candidate narrative
    narrative_text = profile.get("project_descriptions", "")
    if not narrative_text:
        # Fallback to semantic summary and experiences
        narrative_text = profile.get("semantic_summary", "")
        for exp in profile.get("experiences", []):
            if isinstance(exp, dict):
                narrative_text += f"\n- {exp.get('title', '')} at {exp.get('company', '')}: {exp.get('description', '')}"

    if not narrative_text.strip():
        narrative_text = "Experienced professional with a strong background."

    try:
        narrative = parse_project_narrative(narrative_text)
        ownership = detect_ownership_level(narrative_text, narrative.candidate_role)
        clarity = score_outcome_clarity(narrative.outcome)
        complexity = evaluate_complexity(narrative_text, narrative.challenges_faced)
        
        # Build confidence scores for top skills
        skills = profile.get("core_skills", [])[:5]
        if not skills:
            skills = ["General Professional"]
            
        mock_scores = {}
        for skill in skills:
            confidence = calculate_confidence_score(skill, ownership, clarity, complexity, project_count=1)
            mock_scores[skill] = [confidence]
            
        graph = build_skill_graph(mock_scores)
        
        # Opportunity text for parsing
        opp_text = f"{opportunity.get('title', '')} at {opportunity.get('company', '')}. {opportunity.get('match_reasoning', '')}"
        
        proof_card = generate_proof_card(graph, opp_text, opportunity.get("title", "Role"), max_skills=3)
        return proof_card_to_dict(proof_card)
    except Exception as e:
        logger.error(f"Agent 4 proof card generation failed: {e}")
        # Fallback to mock
        skills = profile.get("core_skills") or []
        matched = []
        for skill in skills[:6]:
            matched.append({
                "skill_name": skill,
                "confidence_score": 82.0,
                "proficiency_level": "advanced",
                "best_project_evidence": profile.get("semantic_summary", "")[:200],
                "project_count": 1,
            })
        return {
            "opportunity_title": opportunity.get("title", ""),
            "required_skills": skills,
            "matched_skills": matched,
            "total_relevance_score": opportunity.get("fit_score", 75.0),
            "summary": profile.get("semantic_summary", "Profile-aligned technical evidence."),
        }


@app.post("/outreach")
async def generate_outreach(request: OutreachRequest):
    """
    Generate LinkedIn + email outreach for a matched opportunity using Agent 5.
    Expects the opportunity payload returned by POST /analyze.
    """
    try:
        opp = request.opportunity
        chem = opp.get("chemistry") or {}
        profile = request.candidate_profile or {}

        way_in_strategy = {
            "actionable_sentence": chem.get("way_in_strategy", ""),
            "primary_signal": "connector",
            "confidence": chem.get("way_in_confidence", 0.7),
        }

        engagement_signals = []
        for interaction in chem.get("employee_interactions") or []:
            engagement_signals.append({
                "person_name": interaction.get("person_name", ""),
                "person_role": interaction.get("person_role", ""),
                "company": opp.get("company", ""),
                "interaction_type": interaction.get("interaction_type", "engagement"),
                "interaction_detail": interaction.get("interaction_detail", ""),
            })

        connector_data = {
            "best_connector": {
                "person_name": chem.get("best_connector_name", "Contact"),
                "relationship_to_candidate": chem.get("best_connector_intro", ""),
                "relationship_to_company": f"Connection at {opp.get('company', 'target company')}",
                "introduction_likelihood": chem.get("entry_probability", 0.5),
            }
        }

        shared_contexts = []
        if chem.get("shared_contexts_summary"):
            shared_contexts.append({
                "context_type": "community",
                "name": chem.get("shared_contexts_summary", ""),
                "relevance_score": min(1.0, (chem.get("shared_contexts_count", 0) or 0) / 5.0),
            })

        proof_card = _build_proof_card_from_profile(opp, profile)
        opportunity_data = {
            "opportunity_title": opp.get("title", ""),
            "company_name": opp.get("company", ""),
            "hiring_contact": {
                "name": chem.get("best_connector_name", "Hiring Team"),
                "title": "Hiring contact",
            },
        }

        package = assemble_outreach_package(
            opportunity_title=opp.get("company", opp.get("title", "Opportunity")),
            candidate_name=request.candidate_name,
            inroad_score=float(chem.get("inroad_score", opp.get("fit_score", 0))),
            way_in_strategy=way_in_strategy,
            shared_contexts=shared_contexts,
            engagement_signals=engagement_signals,
            connector_data=connector_data,
            proof_card=proof_card,
            opportunity_data=opportunity_data,
        )

        return {
            "status": "success",
            "opportunity_id": request.opportunity_id,
            "company_name": opp.get("company", ""),
            "linkedin_dm": package.linkedin_outreach.model_dump(),
            "email_package": package.email_outreach.model_dump(),
            "message_body": package.enriched_email_primary,
            "linkedin_body": package.enriched_linkedin_message,
            "action_instructions": package.action_instructions.model_dump(),
            "proof_attachment": package.proof_attachment.model_dump() if package.proof_attachment else None,
        }
    except Exception as e:
        logger.error(f"Outreach generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate outreach: {str(e)}",
        )


# ============================================
# Error Handlers
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


# ============================================
# Application Entry Point
# ============================================

# ============================================
# API Endpoints (Mapped for Frontend)
# ============================================

@app.post("/api/profile")
async def create_profile_endpoint(body: UserProfileUpdate, user: dict = Depends(require_auth)):
    return await update_profile(body, user)

@app.get("/api/profile/{userId}")
async def get_profile_by_id(userId: str, user: dict = Depends(require_auth)):
    return await read_profile(user)

@app.put("/api/profile/{userId}")
async def update_profile_by_id(userId: str, body: UserProfileUpdate, user: dict = Depends(require_auth)):
    return await update_profile(body, user)

@app.post("/api/resume/upload")
async def api_upload_resume(file: UploadFile = File(...), user: Optional[dict] = Depends(get_current_user)):
    return await upload_resume(file, user)

@app.post("/api/resume/extract")
async def api_extract_resume(file: UploadFile = File(...), user: Optional[dict] = Depends(get_current_user)):
    # Simply delegates to upload for now, which extracts sections
    return await upload_resume(file, user)

@app.get("/api/opportunities")
async def api_get_opportunities(user: dict = Depends(require_auth)):
    return {"status": "ok", "opportunities": get_mock_opportunities()}

@app.post("/api/opportunities/ingest")
async def api_ingest_opportunities(user: dict = Depends(require_auth)):
    return {"status": "ok", "message": "Ingestion pipeline triggered (stub)"}

@app.get("/api/opportunities/{id}")
async def api_get_opportunity(id: int, user: dict = Depends(require_auth)):
    opps = get_mock_opportunities()
    matched = next((o for o in opps if o["id"] == id), None)
    if not matched:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return {"status": "ok", "opportunity": matched}

@app.post("/api/match")
async def api_post_match(request: AnalyzeRequest, user: Optional[dict] = Depends(get_current_user)):
    return await analyze_candidate(request, user)

@app.get("/api/matches/{userId}")
async def api_get_matches(userId: str, user: dict = Depends(require_auth)):
    opps = get_mock_opportunities()
    # Mocking ranked output
    from member_b.scorer import rank_opportunities
    ranked = rank_opportunities(opps, top_k=5)
    return {"status": "ok", "matches": ranked}

class ChatMessage(BaseModel):
    message: str

@app.post("/api/mentor/chat")
async def api_mentor_chat(body: ChatMessage, user: dict = Depends(require_auth)):
    return {"status": "ok", "reply": "This is a simulated AI mentor response based on your profile."}

@app.post("/api/roadmap/generate")
async def api_roadmap_generate(user: dict = Depends(require_auth)):
    return {
        "status": "ok",
        "roadmap": [
            {"step": 1, "title": "Enhance System Design Skills", "status": "pending"},
            {"step": 2, "title": "Apply to Hidden Market Roles", "status": "active"},
        ]
    }

@app.get("/api/notifications/{userId}")
async def api_get_notifications(userId: str, user: dict = Depends(require_auth)):
    return {
        "status": "ok",
        "notifications": [
            {"id": 1, "message": "New hidden opportunity matching your skill profile.", "type": "match"}
        ]
    }


# ============================================
# Frontend Static Files (must be last)
# ============================================
FRONTEND_DIR = Path(__file__).resolve().parent / "frontend" / "public"
if FRONTEND_DIR.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=str(FRONTEND_DIR), html=True),
        name="frontend",
    )
    logger.info("Serving InRoad frontend from %s", FRONTEND_DIR)
else:
    logger.warning("Frontend directory not found: %s", FRONTEND_DIR)


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Opportunity Engine API server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
