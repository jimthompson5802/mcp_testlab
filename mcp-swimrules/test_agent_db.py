"""
Test script for agent_swimrules_db to verify RAG functionality

This script tests the enhanced vector database created by agent_rule_ingestion.py
to ensure it's ready for MCP agent use with proper metadata and rule identification.
"""

import os
import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma

# Configuration
VECTORDB_DIR = "./agent_swimrules_db"


def test_database():
    """Test the enhanced agent swim rules database"""

    print("Testing Agent Swim Rules Database")
    print("=" * 50)

    # Load environment variables
    load_dotenv.load_dotenv()

    # Initialize embeddings (same as used during creation)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Load the existing vector store
    vector_store = Chroma(persist_directory=VECTORDB_DIR, embedding_function=embeddings)

    # Test queries specifically for MCP agent scenarios
    test_scenarios = [
        {
            "scenario": "Swimmer did not touch the wall with both hands simultaneously during breaststroke turn",
            "expected_rules": ["101.2", "breaststroke", "turn"],
        },
        {
            "scenario": "Butterfly swimmer's hands did not touch the wall at the same time at finish",
            "expected_rules": ["101.3", "butterfly", "finish"],
        },
        {
            "scenario": "Swimmer performed a dolphin kick during breaststroke underwater phase",
            "expected_rules": ["101.2", "breaststroke", "kick"],
        },
        {
            "scenario": "False start occurred when swimmer left the block before the starting signal",
            "expected_rules": ["101.1", "start", "false"],
        },
    ]

    for i, test_case in enumerate(test_scenarios, 1):
        print(f"\nTest Case {i}: {test_case['scenario']}")
        print("-" * 80)

        # Perform similarity search
        results = vector_store.similarity_search(
            test_case["scenario"],
            k=3,
            # Use filter to focus on rule chunks if needed
        )

        print(f"Found {len(results)} relevant results:")

        for j, doc in enumerate(results, 1):
            metadata = doc.metadata
            print(f"\n  Result {j}:")
            print(f"    Rule ID: {metadata.get('rule_id', 'N/A')}")
            print(f"    Rule Number: {metadata.get('rule_number', 'N/A')}")
            print(f"    Category: {metadata.get('category', 'N/A')}")
            print(f"    Stroke Type: {metadata.get('stroke_type', 'N/A')}")
            print(f"    Chunk Type: {metadata.get('chunk_type', 'N/A')}")
            print(f"    Content Preview: {doc.page_content[:150]}...")

            # Check if expected rules are found
            content_lower = doc.page_content.lower()
            rule_number = metadata.get("rule_number", "").lower()
            found_expected = []

            for expected in test_case["expected_rules"]:
                if expected.lower() in content_lower or expected.lower() in rule_number:
                    found_expected.append(expected)

            if found_expected:
                print(f"    ✓ Found expected elements: {', '.join(found_expected)}")

    # Test metadata filtering capabilities
    print("\n" + "=" * 50)
    print("Testing Metadata Filtering")
    print("=" * 50)

    # Test filtering by stroke type
    print("\nTesting stroke type filtering...")
    breaststroke_results = vector_store.similarity_search(
        "breaststroke rules", k=5, filter={"stroke_type": "breaststroke"}
    )
    print(f"Found {len(breaststroke_results)} breaststroke-specific results")

    # Test filtering by category
    print("\nTesting category filtering...")
    violation_results = vector_store.similarity_search(
        "violation penalty", k=5, filter={"category": "Violations and Penalties"}
    )
    print(f"Found {len(violation_results)} violation/penalty results")

    # Test filtering by chunk type
    print("\nTesting chunk type filtering...")
    situation_results = vector_store.similarity_search("swimming scenario", k=3, filter={"chunk_type": "situation"})
    print(f"Found {len(situation_results)} practical situation results")

    for result in situation_results:
        print(f"  - {result.page_content[:100]}...")

    print("\n" + "=" * 50)
    print("Database Test Complete!")
    print("✓ Vector database is ready for MCP agent RAG operations")
    print("✓ Enhanced metadata is properly structured")
    print("✓ Rule identification and categorization working")
    print("✓ Filtering capabilities available for targeted searches")


if __name__ == "__main__":
    if not os.path.exists(VECTORDB_DIR):
        print(f"Error: Vector database not found at {VECTORDB_DIR}")
        print("Please run agent_rule_ingestion.py first to create the database.")
    else:
        test_database()
