"""
MCP Situation Analysis Module for Swim Rules Agent

This module implements Section 4.2.1 Situation Analysis from the product requirements document.
Provides the `analyze_situation` MCP tool that uses RAG (Retrieval-Augmented Generation)
to analyze swimming scenarios and determine if they result in disqualification or are allowed.

The tool integrates:
- ChromaDB vector database for semantic rule retrieval
- OpenAI GPT-4o for analysis and decision making
- FastMCP for MCP server functionality

Transport: stdio
"""

import os
import asyncio
from typing import Dict, List, Any
from dataclasses import dataclass
import json

# Third-party imports
from fastmcp import FastMCP
import chromadb
from chromadb.config import Settings
from openai import AsyncOpenAI
from langchain_openai import OpenAIEmbeddings

# Load environment variables
try:
    import load_dotenv

    load_dotenv.load_dotenv()
except ImportError:
    pass


@dataclass
class RuleCitation:
    """Rule citation data structure"""

    identifier: str
    title: str
    relevance_score: float


@dataclass
class AnalysisResult:
    """Analysis result data structure"""

    decision: str  # "ALLOWED" or "DISQUALIFICATION"
    rationale: str
    rule_citations: List[str]
    confidence_score: float


class SwimRulesRAGAnalyzer:
    """
    RAG-based analyzer for swimming scenario analysis using ChromaDB and OpenAI

    This class implements the core logic for Section 4.2.1 Situation Analysis:
    1. Retrieve relevant rules from ChromaDB vector database
    2. Use OpenAI GPT-4o to analyze scenario with retrieved context
    3. Extract rule citations and provide structured analysis
    """

    def __init__(
        self,
        chroma_db_path: str = "./agent_swimrules_db",
        collection_name: str = "swim_rules",
        openai_model: str = "gpt-4o",
    ):
        """
        Initialize the RAG analyzer

        Args:
            chroma_db_path: Path to ChromaDB database directory
            collection_name: Name of the ChromaDB collection containing swim rules
            openai_model: OpenAI model to use for analysis
        """
        self.chroma_db_path = chroma_db_path
        self.collection_name = collection_name
        self.openai_model = openai_model

        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.openai_client = AsyncOpenAI(api_key=api_key)

        # Initialize ChromaDB client
        self.chroma_client = None
        self.collection = None

        # Initialize embeddings for query processing
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    async def initialize(self):
        """Initialize ChromaDB connection and collection"""
        try:
            # Initialize ChromaDB client with persistence
            self.chroma_client = chromadb.PersistentClient(
                path=self.chroma_db_path, settings=Settings(allow_reset=True, anonymized_telemetry=False)
            )

            # Get the collection
            try:
                self.collection = self.chroma_client.get_collection(name=self.collection_name)
                print(f"Connected to existing collection '{self.collection_name}'")
            except Exception:
                # Collection doesn't exist, create it
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name, metadata={"description": "USA Swimming rules and regulations"}
                )
                print(f"Created new collection '{self.collection_name}'")

        except Exception as e:
            raise RuntimeError(f"Failed to initialize ChromaDB: {e}")

    async def retrieve_relevant_rules(self, scenario: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant rules from ChromaDB using semantic similarity

        Args:
            scenario: Swimming scenario description
            n_results: Number of top relevant rules to retrieve

        Returns:
            List of relevant rule documents with metadata
        """
        try:
            # Generate embedding for the scenario
            scenario_embedding = await asyncio.to_thread(self.embeddings.embed_query, scenario)

            # Query ChromaDB for similar rules
            if self.collection is not None:
                results = self.collection.query(
                    query_embeddings=[scenario_embedding],
                    n_results=n_results,
                    include=["documents", "metadatas", "distances"],
                )
            else:
                raise RuntimeError("ChromaDB collection not initialized")

            # Format results
            relevant_rules = []
            if results and results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    distance = results["distances"][0][i] if results["distances"] else 1.0

                    relevant_rules.append(
                        {
                            "content": doc,
                            "metadata": metadata,
                            "relevance_score": 1.0 - distance,  # Convert distance to similarity
                            "rule_identifier": metadata.get("rule_number", "Unknown"),
                            "rule_title": metadata.get("rule_title", "No title"),
                            "category": metadata.get("category", "General"),
                        }
                    )

            return relevant_rules

        except Exception as e:
            print(f"Error retrieving rules from ChromaDB: {e}")
            return []

    async def analyze_with_llm(self, scenario: str, relevant_rules: List[Dict[str, Any]]) -> AnalysisResult:
        """
        Analyze scenario using OpenAI GPT-4o with retrieved rule context.

        Args:
            scenario (str): Swimming scenario description
            relevant_rules (List[Dict[str, Any]]): List of relevant rules retrieved from RAG

        Returns:
            AnalysisResult: Structured result with decision, rationale, and citations
        """
        import textwrap

        try:
            # Prepare context from retrieved rules
            context_text = self._format_rules_context(relevant_rules)

            # Create the analysis prompt using triple quotes and textwrap.dedent
            system_prompt = textwrap.dedent(
                """
                You are an expert USA Swimming official with comprehensive knowledge of
                swimming rules and regulations.

                Your task is to analyze swimming scenarios and determine if they constitute violations that would
                result in disqualification.

                For each scenario, you must:
                1. Carefully review the provided rule context
                2. Determine if the scenario describes a violation
                3. Provide your decision as either "ALLOWED" or "DISQUALIFICATION"
                4. Give a detailed rationale explaining your decision
                5. List the specific rule identifiers that support your decision

                Be precise and authoritative in your analysis. Base your decisions strictly on the provided rules.
                """
            )

            user_prompt = textwrap.dedent(
                f"""
                SCENARIO TO ANALYZE:
                {scenario}

                RELEVANT RULES CONTEXT:
                {context_text}

                Please analyze this scenario and provide your response in the following JSON format:
                {{
                    "decision": "ALLOWED" or "DISQUALIFICATION",
                    "rationale": "Detailed explanation of your decision",
                    "rule_citations": ["rule_id_1", "rule_id_2", ...],
                    "confidence_score": 0.95
                }}

                Focus on the specific rules that apply to this scenario and explain your reasoning clearly.
                """
            )

            # Call OpenAI API
            response = await self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=0.1,  # Low temperature for consistent analysis
                max_tokens=1000,
            )

            # Parse the response
            response_content = response.choices[0].message.content
            if response_content is None:
                response_content = "No response generated"
            return self._parse_llm_response(response_content, relevant_rules)

        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            # Return a fallback response
            return AnalysisResult(
                decision="DISQUALIFICATION",
                rationale=f"Error analyzing scenario: {str(e)}. When in doubt, consult official rules.",
                rule_citations=[],
                confidence_score=0.0,
            )

    def _format_rules_context(self, relevant_rules: List[Dict[str, Any]]) -> str:
        """Format retrieved rules into context text for LLM"""
        if not relevant_rules:
            return "No relevant rules found in database."

        context_parts = []
        for rule in relevant_rules:
            rule_id = rule.get("rule_identifier", "Unknown")
            rule_title = rule.get("rule_title", "No title")
            content = rule.get("content", "No content")
            category = rule.get("category", "General")

            context_parts.append(
                f"""
RULE {rule_id}: {rule_title}
Category: {category}
Content: {content}
---"""
            )

        return "\n".join(context_parts)

    def _parse_llm_response(self, response_content: str, relevant_rules: List[Dict[str, Any]]) -> AnalysisResult:
        """Parse LLM response into structured AnalysisResult"""
        try:
            # Try to parse as JSON
            if "{" in response_content and "}" in response_content:
                start_idx = response_content.find("{")
                end_idx = response_content.rfind("}") + 1
                json_content = response_content[start_idx:end_idx]
                parsed = json.loads(json_content)

                return AnalysisResult(
                    decision=parsed.get("decision", "DISQUALIFICATION"),
                    rationale=parsed.get("rationale", "Unable to parse analysis"),
                    rule_citations=parsed.get("rule_citations", []),
                    confidence_score=parsed.get("confidence_score", 0.5),
                )
            else:
                # Fallback parsing for non-JSON responses
                decision = "DISQUALIFICATION" if "disqualification" in response_content.lower() else "ALLOWED"
                return AnalysisResult(
                    decision=decision,
                    rationale=response_content,
                    rule_citations=[rule.get("rule_identifier", "") for rule in relevant_rules[:3]],
                    confidence_score=0.7,
                )

        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return AnalysisResult(
                decision="DISQUALIFICATION",
                rationale="Error parsing analysis response. Please consult official rules.",
                rule_citations=[],
                confidence_score=0.0,
            )

    async def analyze_situation(self, scenario: str) -> Dict[str, Any]:
        """
        Main analysis method implementing Section 4.2.1 requirements

        Args:
            scenario: Natural language description of swimming scenario

        Returns:
            Dictionary with decision, rationale, and rule_citations
        """
        try:
            # Step 1: Retrieve relevant rules using RAG
            relevant_rules = await self.retrieve_relevant_rules(scenario)

            # Step 2: Analyze with LLM
            analysis_result = await self.analyze_with_llm(scenario, relevant_rules)

            # Step 3: Format response according to requirements
            return {
                "decision": analysis_result.decision,
                "rationale": analysis_result.rationale,
                "rule_citations": analysis_result.rule_citations,
            }

        except Exception as e:
            print(f"Error in situation analysis: {e}")
            return {
                "decision": "DISQUALIFICATION",
                "rationale": f"Analysis error: {str(e)}. When in doubt, consult official swimming rules.",
                "rule_citations": [],
            }


# Initialize FastMCP server
mcp_server = FastMCP("swim-rules-analyzer")

# Global analyzer instance
analyzer = None


@mcp_server.tool()
async def analyze_situation(scenario: str) -> Dict[str, Any]:
    """
    Analyze specified situation to determine if legal or disqualification with rationale and rule citation.

    This tool implements Section 4.2.1 of the product requirements:
    - Uses RAG to retrieve relevant rules from ChromaDB vector database
    - Uses OpenAI LLM gpt-4o with retrieved documents to make decisions
    - Extracts rule citations from metadata

    Args:
        scenario: Natural language description of the swimming scenario

    Returns:
        Dictionary containing:
        - decision: "ALLOWED" or "DISQUALIFICATION"
        - rationale: Detailed explanation of the decision
        - rule_citations: List of relevant rule citations (identifiers)
    """
    global analyzer

    try:
        # Initialize analyzer if not already done
        if analyzer is None:
            analyzer = SwimRulesRAGAnalyzer()
            await analyzer.initialize()

        # Validate input
        if not scenario or not scenario.strip():
            return {
                "decision": "DISQUALIFICATION",
                "rationale": "No scenario provided for analysis. Unable to make determination.",
                "rule_citations": [],
            }

        # Perform analysis
        result = await analyzer.analyze_situation(scenario.strip())
        return result

    except Exception as e:
        print(f"Error in analyze_situation tool: {e}")
        return {
            "decision": "DISQUALIFICATION",
            "rationale": f"Tool error: {str(e)}. Please consult official swimming rules and qualified officials.",
            "rule_citations": [],
        }


if __name__ == "__main__":
    """
    Run the MCP server with stdio transport as specified in requirements
    """
    # Run with stdio transport
    mcp_server.run(transport="stdio")
