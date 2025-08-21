#!/usr/bin/env python3
"""
Rule Lookup Utility - Section 4.5.1 Implementation

This debugging utility allows users to query the ChromaDB vector database
for relevant swimming rules based on natural language queries.

Features:
- Interactive query prompt
- ChromaDB vector similarity search
- Display rule metadata (ID, title, description) alongside rule text
- Efficient similarity searches using existing ChromaDB integration
"""

import asyncio
import os
import sys
from typing import List, Dict, Any
import textwrap

# Third-party imports
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
try:
    import load_dotenv

    load_dotenv.load_dotenv()
except ImportError:
    print("Warning: load_dotenv not available, ensure OPENAI_API_KEY is set in environment")


class RuleLookupUtility:
    """
    Rule lookup utility for debugging and exploring the ChromaDB rule database.

    This utility implements Section 4.5.1 requirements:
    - Prompt user for queries
    - Retrieve relevant rules using ChromaDB vector similarity search
    - Display rule metadata alongside rule text
    """

    def __init__(
        self,
        chroma_db_path: str = "./agent_swimrules_db",
        collection_name: str = "langchain",  # Updated to match actual collection name
    ):
        """
        Initialize the rule lookup utility.

        Args:
            chroma_db_path: Path to ChromaDB database directory
            collection_name: Name of the ChromaDB collection containing swim rules
        """
        self.chroma_db_path = chroma_db_path
        self.collection_name = collection_name

        # Initialize embeddings for query processing
        self.embeddings = None
        self.chroma_client = None
        self.collection = None

    async def initialize(self):
        """Initialize ChromaDB connection and embeddings"""
        try:
            # Check for OpenAI API key
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required for embeddings. "
                    "Please set it in your environment or .env file."
                )

            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

            # Initialize ChromaDB client with persistence
            self.chroma_client = chromadb.PersistentClient(
                path=self.chroma_db_path, settings=Settings(allow_reset=True, anonymized_telemetry=False)
            )

            # Get the collection
            try:
                self.collection = self.chroma_client.get_collection(name=self.collection_name)
                print(f"✓ Connected to ChromaDB collection '{self.collection_name}'")

                # Get collection stats
                count = self.collection.count()
                print(f"✓ Collection contains {count} rule documents")

            except Exception:
                raise RuntimeError(
                    f"Collection '{self.collection_name}' not found. "
                    "Please ensure the rule ingestion process has been completed."
                )

        except Exception as e:
            raise RuntimeError(f"Failed to initialize rule lookup utility: {e}")

    async def lookup_rules(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant rules from ChromaDB using semantic similarity.

        Args:
            query: Natural language query for rule lookup
            n_results: Number of top relevant rules to retrieve

        Returns:
            List of relevant rule documents with metadata and similarity scores
        """
        try:
            if not self.embeddings or not self.collection:
                raise RuntimeError("Utility not properly initialized")

            # Generate embedding for the query
            print(f"🔍 Generating embeddings for query: '{query}'")
            query_embedding = await asyncio.to_thread(self.embeddings.embed_query, query)

            # Query ChromaDB for similar rules
            print(f"🔍 Searching ChromaDB for {n_results} most relevant rules...")
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"],
            )

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
                            "similarity_score": 1.0 - distance,  # Convert distance to similarity
                            "rule_id": metadata.get("rule_number", "Unknown"),
                            "rule_title": metadata.get("rule_title", "No title"),
                            "category": metadata.get("category", "General"),
                            "stroke": metadata.get("stroke", "General"),
                        }
                    )

            return relevant_rules

        except Exception as e:
            print(f"❌ Error retrieving rules from ChromaDB: {e}")
            return []

    def display_results(self, query: str, results: List[Dict[str, Any]]):
        """
        Display search results in a formatted manner.

        Args:
            query: The original query
            results: List of rule documents with metadata
        """
        print("\n" + "=" * 80)
        print(f"🔍 RULE LOOKUP RESULTS FOR: '{query}'")
        print("=" * 80)

        if not results:
            print("❌ No relevant rules found for this query.")
            print("💡 Try different keywords or more specific terms.")
            return

        for i, rule in enumerate(results, 1):
            similarity = rule.get("similarity_score", 0.0)
            rule_id = rule.get("rule_id", "Unknown")
            rule_title = rule.get("rule_title", "No title")
            category = rule.get("category", "General")
            stroke = rule.get("stroke", "General")
            content = rule.get("content", "No content available")

            print(f"\n📖 RESULT #{i}")
            print(f"🏷️  Rule ID: {rule_id}")
            print(f"📝 Title: {rule_title}")
            print(f"🏊 Stroke: {stroke}")
            print(f"📂 Category: {category}")
            print(f"🎯 Similarity: {similarity:.3f}")
            print("-" * 60)

            # Wrap content for better readability
            wrapped_content = textwrap.fill(content, width=75, initial_indent="   ", subsequent_indent="   ")
            print(f"📄 Content:\n{wrapped_content}")
            print("-" * 60)

    async def run_interactive_session(self):
        """
        Run an interactive session allowing users to repeatedly query the rule database.
        """
        print(
            textwrap.dedent(
                """
            🏊‍♀️ SWIM RULES LOOKUP UTILITY 🏊‍♂️
            =====================================
            
            This utility allows you to search the USA Swimming rules database
            using natural language queries.
            
            Examples of good queries:
            - "breaststroke turn requirements"
            - "false start rules"
            - "butterfly stroke technique"
            - "relay exchange zone"
            - "disqualification procedures"
            
            Type 'quit', 'exit', or 'q' to stop.
            """
            )
        )

        while True:
            try:
                # Prompt for user query
                print("\n" + "=" * 50)
                query = input("🔍 Enter your rule query: ").strip()

                # Check for exit commands
                if query.lower() in ["quit", "exit", "q", ""]:
                    print("👋 Thank you for using the Rule Lookup Utility!")
                    break

                # Ask for number of results (optional)
                try:
                    n_results_input = input("📊 Number of results (1-10, default=5): ").strip()
                    n_results = int(n_results_input) if n_results_input else 5
                    n_results = max(1, min(10, n_results))  # Clamp between 1-10
                except ValueError:
                    n_results = 5
                    print("ℹ️  Using default of 5 results")

                # Perform the lookup
                results = await self.lookup_rules(query, n_results)

                # Display results
                self.display_results(query, results)

                # Option to see more details or continue
                print(f"\n💡 Found {len(results)} relevant rules")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error during lookup: {e}")
                print("Please try again with a different query.")


async def main():
    """Main function to run the rule lookup utility"""
    utility = RuleLookupUtility()

    try:
        print("🚀 Initializing Rule Lookup Utility...")
        await utility.initialize()
        await utility.run_interactive_session()

    except Exception as e:
        print(f"❌ Failed to start Rule Lookup Utility: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure OPENAI_API_KEY is set in your environment")
        print("2. Verify ChromaDB database exists in ./agent_swimrules_db")
        print("3. Run rule ingestion process if database is empty")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
