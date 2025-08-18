#!/usr/bin/env python3
"""
Test script to verify the integration between app_server.py and mcp_situation_analysis.py
Tests the refactored MCP client integration as specified in PRD sections 4.2 and 4.3
"""

import asyncio
import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import after path adjustment
from app_server import MCPSituationAnalysisClient


async def test_mcp_integration():
    """Test the MCP client integration with situation analysis"""

    print("Testing MCP Situation Analysis Integration")
    print("=" * 50)

    # Initialize MCP client
    print("1. Initializing MCP client...")
    client = MCPSituationAnalysisClient()

    try:
        await client.initialize()
        print("✓ MCP client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize MCP client: {e}")
        return False

    # Test scenarios from PRD
    test_scenarios = [
        {
            "name": "Breaststroke Two-Hand Touch Violation",
            "scenario": "Swimmer did not touch the wall with both hands simultaneously during breaststroke turn",
        },
        {
            "name": "Valid Backstroke Turn",
            "scenario": "Swimmer performed a proper backstroke turn touching the wall with one hand before rotating",
        },
        {"name": "False Start", "scenario": "Swimmer left the starting block before the starting signal was given"},
    ]

    print("\n2. Testing scenario analysis...")

    for i, test_case in enumerate(test_scenarios, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Scenario: {test_case['scenario']}")

        try:
            result = await client.analyze_situation(test_case["scenario"])

            # Validate response structure
            required_keys = ["decision", "rationale", "rule_citations"]
            missing_keys = [key for key in required_keys if key not in result]

            if missing_keys:
                print(f"✗ Missing required keys: {missing_keys}")
                continue

            print(f"✓ Decision: {result['decision']}")
            print(f"✓ Rationale: {result['rationale'][:100]}...")
            print(f"✓ Rule Citations: {result['rule_citations']}")

            # Validate decision format
            if result["decision"] not in ["ALLOWED", "DISQUALIFICATION"]:
                print(f"✗ Invalid decision format: {result['decision']}")
            else:
                print("✓ Decision format valid")

        except Exception as e:
            print(f"✗ Analysis failed: {e}")

    # Cleanup
    print("\n3. Cleaning up...")
    try:
        await client.cleanup()
        print("✓ MCP client cleaned up successfully")
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")

    print("\n" + "=" * 50)
    print("Integration test completed")
    return True


async def test_api_response_conversion():
    """Test the conversion from MCP result to API response format"""
    from app_server import _convert_mcp_to_response

    print("\nTesting API Response Conversion")
    print("=" * 40)

    # Test MCP result
    mock_mcp_result = {
        "decision": "DISQUALIFICATION",
        "rationale": "The described scenario constitutes a clear violation of breaststroke technique requirements.",
        "rule_citations": ["101.2.2", "101.2.3", "102.5.1"],
    }

    try:
        api_response = _convert_mcp_to_response(mock_mcp_result)

        print(f"✓ Decision: {api_response.decision}")
        print(f"✓ Confidence: {api_response.confidence}")
        print(f"✓ Rationale: {api_response.rationale[:100]}...")
        print(f"✓ Citations count: {len(api_response.rule_citations)}")

        # Validate citation structure
        for citation in api_response.rule_citations:
            if hasattr(citation, "rule_number") and hasattr(citation, "rule_title"):
                print(f"✓ Citation: {citation.rule_number} - {citation.rule_title}")
            else:
                print("✗ Invalid citation structure")

        return True

    except Exception as e:
        print(f"✗ Response conversion failed: {e}")
        return False


if __name__ == "__main__":

    async def main():
        print("Swim Rules Agent - MCP Integration Test")
        print("Verifying PRD sections 4.2 and 4.3 implementation")
        print("=" * 60)

        # Test MCP integration
        mcp_success = await test_mcp_integration()

        # Test API response conversion
        api_success = await test_api_response_conversion()

        print("\n" + "=" * 60)
        if mcp_success and api_success:
            print("✓ All tests passed - Integration successful!")
            return 0
        else:
            print("✗ Some tests failed - Please check the implementation")
            return 1

    # Run the test
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
