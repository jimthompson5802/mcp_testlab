"""
FastAPI Application Server for Swim Rules Agent
Web-based interface for USA Swimming rules analysis and violation checking.

Integrates with MCP Situation Analysis module as specified in PRD sections 4.2 and 4.3.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import os
import json

# FastMCP imports for proper MCP client integration
from fastmcp import Client
from fastmcp.client.transports import StdioTransport


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


class AnalysisResponse(BaseModel):
    """Response model for scenario analysis as specified in PRD Section 4.2.1"""

    decision: str  # "ALLOWED" or "DISQUALIFICATION"
    rationale: str
    rule_citations: List[str]  # List of relevant rule citations (identifiers)

    class Config:
        json_schema_extra = {
            "example": {
                "decision": "DISQUALIFICATION",
                "rationale": "The described scenario constitutes a violation of breaststroke technique requirements...",
                "rule_citations": ["101.2.2", "101.2.3", "102.5.1"],
            }
        }


# Initialize FastAPI app
app = FastAPI(
    title="Swim Rules Agent", description="Official Scenario Analysis for USA Swimming Rules", version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class MCPSituationAnalysisClient:
    """
    MCP Client for connecting to the Situation Analysis server
    Implements stdio transport as specified in PRD section 4.2.1
    Uses proper FastMCP client library
    """

    def __init__(self, server_script_path: str = "mcp_situation_analysis.py"):
        """
        Initialize MCP client for situation analysis

        Args:
            server_script_path: Path to the MCP situation analysis server script
        """
        self.server_script_path = server_script_path
        self.client: Optional[Client] = None
        self.transport: Optional[StdioTransport] = None
        self.initialized = False

    async def initialize(self):
        """Initialize the MCP connection to situation analysis server"""
        try:
            # Create stdio transport for MCP server
            current_dir = os.path.dirname(os.path.abspath(__file__))
            server_path = os.path.join(current_dir, self.server_script_path)

            if not os.path.exists(server_path):
                raise FileNotFoundError(f"MCP server script not found: {server_path}")

            # Initialize transport with the MCP server script
            self.transport = StdioTransport(command="python", args=[server_path])

            # Create FastMCP client
            self.client = Client(self.transport)

            # Start the client connection
            await self.client.__aenter__()

            self.initialized = True
            print("MCP Situation Analysis server started successfully")

        except Exception as e:
            print(f"Failed to initialize MCP client: {e}")
            raise RuntimeError(f"MCP client initialization failed: {e}")

    async def analyze_situation(self, scenario: str) -> Dict:
        """
        Call the analyze_situation MCP tool using proper FastMCP client

        Args:
            scenario: Natural language description of swimming scenario

        Returns:
            Dictionary with decision, rationale, and rule_citations
        """
        if not self.initialized or not self.client:
            raise RuntimeError("MCP client not initialized")

        try:
            # Call the MCP tool using FastMCP client
            response = await self.client.call_tool("analyze_situation", {"scenario": scenario})

            # Parse the response from FastMCP CallToolResult
            if hasattr(response, "data") and isinstance(response.data, dict):
                # The response.data contains the dictionary we need
                return response.data
            elif hasattr(response, "structured_content") and isinstance(response.structured_content, dict):
                # Alternative: use structured_content if available
                return response.structured_content
            elif hasattr(response, "content") and response.content:
                # Fallback: parse from content text
                content = response.content[0] if isinstance(response.content, list) else response.content
                if hasattr(content, "text") and hasattr(content, "type") and content.type == "text":
                    try:
                        return json.loads(content.text)
                    except json.JSONDecodeError:
                        return {"decision": "DISQUALIFICATION", "rationale": content.text, "rule_citations": []}

            # Final fallback
            return {"decision": "DISQUALIFICATION", "rationale": "Unable to parse MCP response", "rule_citations": []}

        except Exception as e:
            print(f"Error calling MCP analyze_situation: {e}")
            return {
                "decision": "DISQUALIFICATION",
                "rationale": f"Analysis error: {str(e)}. Please consult official swimming rules.",
                "rule_citations": [],
            }

    async def cleanup(self):
        """Cleanup MCP client connection"""
        if self.client:
            try:
                await self.client.__aexit__(None, None, None)
                print("MCP client connection closed")
            except Exception as e:
                print(f"Error closing MCP connection: {e}")
            finally:
                self.client = None
                self.transport = None
                self.initialized = False


# Initialize MCP client connection (placeholder for actual MCP integration)
mcp_client = None


@app.on_event("startup")
async def startup_event():
    """Initialize MCP client connection on startup"""
    global mcp_client
    try:
        print("Starting Swim Rules Agent server...")
        mcp_client = MCPSituationAnalysisClient()
        await mcp_client.initialize()
        print("MCP client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize MCP client: {e}")
        print("Server will continue with limited functionality")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup MCP client connection on shutdown"""
    global mcp_client
    if mcp_client:
        await mcp_client.cleanup()
        print("MCP client connection closed")


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
    Analyze swimming scenario for rule violations using MCP Situation Analysis

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

        # Check if MCP client is available
        if not mcp_client or not mcp_client.initialized:
            raise HTTPException(status_code=503, detail="MCP analysis service unavailable")

        # Call MCP situation analysis
        mcp_result = await mcp_client.analyze_situation(request.scenario)

        # Convert MCP result to API response format
        analysis_result = _convert_mcp_to_response(mcp_result)

        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def _convert_mcp_to_response(mcp_result: Dict) -> AnalysisResponse:
    """
    Convert MCP tool result to AnalysisResponse format

    Args:
        mcp_result: Result from MCP analyze_situation tool

    Returns:
        AnalysisResponse: Formatted response for API
    """
    # Extract decision and validate
    decision = mcp_result.get("decision", "DISQUALIFICATION")
    if decision not in ["ALLOWED", "DISQUALIFICATION"]:
        decision = "DISQUALIFICATION"

    # Extract rationale
    rationale = mcp_result.get("rationale", "No rationale provided")

    # Extract rule citations as simple list of strings
    rule_citations_list = mcp_result.get("rule_citations", [])
    citations = []

    for citation_id in rule_citations_list:
        if isinstance(citation_id, str) and citation_id.strip():
            citations.append(citation_id.strip())

    return AnalysisResponse(decision=decision, rationale=rationale, rule_citations=citations)


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
