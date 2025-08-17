"""
FastAPI Application Server for Swim Rules Agent
Web-based interface for USA Swimming rules analysis and violation checking.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List
import asyncio
import uvicorn


# Data models for API requests/responses
class ScenarioAnalysisRequest(BaseModel):
    """Request model for scenario analysis"""

    scenario: str

    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "Swimmer did not touch the wall with both hands simultaneously during breaststroke turn"
            }
        }


class RuleCitation(BaseModel):
    """Model for rule citation information"""

    rule_number: str
    rule_title: str
    rule_category: str


class AnalysisResponse(BaseModel):
    """Response model for scenario analysis"""

    decision: str  # "ALLOWED" or "DISQUALIFICATION"
    confidence: float  # 0-100
    rationale: str
    rule_citations: List[RuleCitation]

    class Config:
        json_schema_extra = {
            "example": {
                "decision": "DISQUALIFICATION",
                "confidence": 95.0,
                "rationale": "The described scenario constitutes a violation of breaststroke technique requirements...",
                "rule_citations": [
                    {
                        "rule_number": "101.2.2",
                        "rule_title": "Breaststroke Turn Requirements",
                        "rule_category": "Stroke Technique",
                    }
                ],
            }
        }


# Initialize FastAPI app
app = FastAPI(
    title="Swim Rules Agent", description="Official Scenario Analysis for USA Swimming Rules", version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize MCP client connection (placeholder for actual MCP integration)
mcp_client = None


@app.on_event("startup")
async def startup_event():
    """Initialize MCP client connection on startup"""
    global mcp_client
    # TODO: Initialize actual MCP client connection
    # This would connect to the MCP server with swim rules tools
    print("Starting Swim Rules Agent server...")
    print("MCP client initialization placeholder")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup MCP client connection on shutdown"""
    global mcp_client
    if mcp_client:
        # TODO: Properly close MCP client connection
        print("Shutting down MCP client connection")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "swim-rules-agent"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_scenario(request: ScenarioAnalysisRequest) -> AnalysisResponse:
    """
    Analyze swimming scenario for rule violations

    Args:
        request: Scenario analysis request containing the scenario description

    Returns:
        AnalysisResponse: Analysis results with decision, rationale, and citations

    Raises:
        HTTPException: If analysis fails or scenario is invalid
    """
    try:
        # Validate input
        if not request.scenario.strip():
            raise HTTPException(status_code=400, detail="Scenario description cannot be empty")

        if len(request.scenario) > 2000:
            raise HTTPException(status_code=400, detail="Scenario description too long (max 2000 characters)")

        # TODO: Replace with actual MCP tool call
        # For now, return a mock response based on scenario content
        analysis_result = await _mock_scenario_analysis(request.scenario)

        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


async def _mock_scenario_analysis(scenario: str) -> AnalysisResponse:
    """
    Mock scenario analysis function
    TODO: Replace with actual MCP tool integration

    Args:
        scenario: Scenario description to analyze

    Returns:
        AnalysisResponse: Mock analysis results
    """
    # Simple keyword-based mock analysis
    scenario_lower = scenario.lower()

    # Check for common violation keywords
    violation_keywords = {
        "both hands": ("breaststroke", "butterfly"),
        "false start": ("starting",),
        "lane violation": ("lane",),
        "stroke technique": ("stroke", "technique"),
        "turn": ("turn", "wall"),
    }

    decision = "ALLOWED"
    confidence = 85.0
    rationale = "The described scenario appears to be within regulation based on standard USA Swimming rules."
    citations = [
        RuleCitation(rule_number="102.1.1", rule_title="General Swimming Regulations", rule_category="General Rules")
    ]

    # Check for potential violations
    for keyword, strokes in violation_keywords.items():
        if keyword in scenario_lower:
            if any(stroke in scenario_lower for stroke in strokes):
                decision = "DISQUALIFICATION"
                confidence = 95.0

                if "both hands" in scenario_lower and (
                    "breaststroke" in scenario_lower or "butterfly" in scenario_lower
                ):
                    rationale = (
                        "The described scenario constitutes a violation of breaststroke/butterfly "
                        "technique requirements. USA Swimming rules mandate that swimmers must touch "
                        "the wall with both hands simultaneously during turns and finishes in "
                        "breaststroke and butterfly events. Failure to do so results in immediate "
                        "disqualification as it provides an unfair competitive advantage and violates "
                        "stroke technique standards.\n\n"
                        "The violation is clear and unambiguous, requiring no official discretion in application."
                    )

                    citations = [
                        RuleCitation(
                            rule_number="101.2.2",
                            rule_title="Breaststroke Turn Requirements",
                            rule_category="Stroke Technique",
                        ),
                        RuleCitation(
                            rule_number="101.2.3",
                            rule_title="Breaststroke Finish Requirements",
                            rule_category="Stroke Technique",
                        ),
                        RuleCitation(
                            rule_number="102.5.1", rule_title="Disqualification Procedures", rule_category="Officials"
                        ),
                    ]
                break

    # Simulate async processing delay
    await asyncio.sleep(0.1)

    return AnalysisResponse(decision=decision, confidence=confidence, rationale=rationale, rule_citations=citations)


@app.get("/api/scenario-examples")
async def get_scenario_examples() -> Dict[str, List[str]]:
    """Get example scenarios for different violation types"""
    return {
        "stroke_violations": [
            "Swimmer did not touch the wall with both hands simultaneously during breaststroke turn",
            "Butterfly swimmer used alternating arm strokes during the race",
            "Breaststroke swimmer performed dolphin kick after the turn",
        ],
        "starting_violations": [
            "Swimmer left the starting block before the starting signal",
            "Swimmer had both feet off the starting platform before the start",
            "Relay swimmer left the block before teammate touched the wall",
        ],
        "general_violations": [
            "Swimmer interfered with another swimmer in adjacent lane",
            "Swimmer used the lane rope for support during the race",
            "Swimmer walked on the pool bottom during competition",
        ],
    }


if __name__ == "__main__":
    # Development server configuration
    uvicorn.run("app_server:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
