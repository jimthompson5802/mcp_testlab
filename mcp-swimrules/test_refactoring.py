#!/usr/bin/env python3
"""
Test script to validate the refactored modules work correctly
according to PRD specifications in Section 4.2.1
"""

import asyncio
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import after path setup
from mcp_situation_analysis import SwimRulesRAGAnalyzer  # noqa: E402


async def test_analyze_situation():
    """Test the analyze_situation functionality"""
    print("Testing MCP Situation Analysis Module...")

    # Test scenario
    test_scenario = "Swimmer did not touch the wall with both hands simultaneously during breaststroke turn"

    try:
        # Initialize analyzer
        analyzer = SwimRulesRAGAnalyzer()
        await analyzer.initialize()

        # Perform analysis
        result = await analyzer.analyze_situation(test_scenario)

        # Validate response format according to PRD
        print("\n=== ANALYSIS RESULTS ===")
        print(f"Scenario: {test_scenario}")
        print(f"Decision: {result.get('decision', 'ERROR')}")
        print(f"Rationale: {result.get('rationale', 'No rationale')}")
        print(f"Rule Citations: {result.get('rule_citations', [])}")

        # Validate response structure
        required_fields = ["decision", "rationale", "rule_citations"]
        missing_fields = [field for field in required_fields if field not in result]

        if missing_fields:
            print(f"\n❌ FAILED: Missing required fields: {missing_fields}")
            return False

        if result["decision"] not in ["ALLOWED", "DISQUALIFICATION"]:
            print(f"\n❌ FAILED: Invalid decision value: {result['decision']}")
            return False

        if not isinstance(result["rule_citations"], list):
            print("\n❌ FAILED: Rule citations should be a list")
            return False

        print("\n✅ SUCCESS: Analysis completed according to PRD specification")
        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


async def main():
    """Main test function"""
    print("=" * 60)
    print("SWIM RULES AGENT - POST-REFACTORING VALIDATION")
    print("=" * 60)

    success = await test_analyze_situation()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED - Refactoring successful!")
        print("Modules are ready for use according to PRD specifications.")
    else:
        print("❌ TESTS FAILED - Please check the refactoring.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
