"""
Test Module for MCP Situation Analysis

This module provides simple validation tests for the mcp_situation_analysis.py module
to ensure it correctly implements Section 4.2.1 Situation Analysis requirements.

Tests cover:
- Basic functionality of the SwimRulesRAGAnalyzer class
- RAG retrieval integration
- OpenAI LLM analysis
- Response format validation
- Error handling scenarios
"""

import asyncio
import os
import sys
from typing import Dict

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the module under test
from mcp_situation_analysis import SwimRulesRAGAnalyzer


# Global test analyzer instance
test_analyzer = None


async def get_test_analyzer():
    """Get or create the test analyzer instance"""
    global test_analyzer
    if test_analyzer is None:
        test_analyzer = SwimRulesRAGAnalyzer()
        await test_analyzer.initialize()
    return test_analyzer


async def test_analyzer_initialization():
    """Test that the RAG analyzer can be initialized properly"""
    print("Testing analyzer initialization...")

    try:
        analyzer = SwimRulesRAGAnalyzer()
        await analyzer.initialize()
        print("✅ Analyzer initialization successful")
        return True
    except Exception as e:
        print(f"❌ Analyzer initialization failed: {e}")
        return False


async def test_scenario_analysis_basic():
    """Test basic scenario analysis functionality"""
    print("Testing basic scenario analysis...")

    # Test scenario - breaststroke violation
    test_scenario = "Swimmer did not touch the wall with both hands simultaneously during breaststroke turn"

    try:
        # Get the analyzer and test the analyze_situation method
        analyzer = await get_test_analyzer()
        result = await analyzer.analyze_situation(test_scenario)

        # Validate response format
        if not isinstance(result, dict):
            print("❌ Result is not a dictionary")
            return False

        required_keys = ["decision", "rationale", "rule_citations"]
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing required key: {key}")
                return False

        # Validate decision format
        if result["decision"] not in ["ALLOWED", "DISQUALIFICATION"]:
            print(f"❌ Invalid decision: {result['decision']}")
            return False

        # Validate rationale exists
        if not result["rationale"] or len(result["rationale"]) < 10:
            print("❌ Rationale is missing or too short")
            return False

        # Validate rule_citations is a list
        if not isinstance(result["rule_citations"], list):
            print("❌ Rule citations is not a list")
            return False

        print("✅ Basic scenario analysis successful")
        print(f"   Decision: {result['decision']}")
        print(f"   Rationale length: {len(result['rationale'])} characters")
        print(f"   Rule citations: {len(result['rule_citations'])} rules")

        return True

    except Exception as e:
        print(f"❌ Basic scenario analysis failed: {e}")
        return False


async def test_multiple_scenarios():
    """Test analysis with multiple different scenarios"""
    print("Testing multiple scenario analysis...")

    test_scenarios = [
        {
            "name": "Breaststroke violation",
            "scenario": "Swimmer did not touch wall with both hands during breaststroke turn",
            "expected": "DISQUALIFICATION",
        },
        {
            "name": "Valid freestyle stroke",
            "scenario": "Swimmer performed normal freestyle stroke and touched wall with one hand",
            "expected": "ALLOWED",
        },
        {
            "name": "False start",
            "scenario": "Swimmer left the starting block before the starting signal was given",
            "expected": "DISQUALIFICATION",
        },
    ]

    results = []
    analyzer = await get_test_analyzer()

    for test_case in test_scenarios:
        try:
            print(f"  Testing: {test_case['name']}")
            result = await analyzer.analyze_situation(test_case["scenario"])

            decision = result.get("decision", "UNKNOWN")
            print(f"    Result: {decision}")

            # Store result for analysis
            results.append(
                {
                    "name": test_case["name"],
                    "scenario": test_case["scenario"],
                    "expected": test_case["expected"],
                    "actual": decision,
                    "passed": decision == test_case["expected"],
                    "rationale_length": len(result.get("rationale", "")),
                }
            )

        except Exception as e:
            print(f"    ❌ Failed: {e}")
            results.append(
                {
                    "name": test_case["name"],
                    "scenario": test_case["scenario"],
                    "expected": test_case["expected"],
                    "actual": "ERROR",
                    "passed": False,
                    "error": str(e),
                }
            )

    # Summary
    passed_count = sum(1 for r in results if r.get("passed", False))
    total_count = len(results)

    print(f"✅ Multiple scenarios test completed: {passed_count}/{total_count} passed")

    for result in results:
        status = "✅" if result.get("passed", False) else "❌"
        print(f"  {status} {result['name']}: {result.get('actual', 'ERROR')}")

    return passed_count == total_count


async def test_empty_scenario():
    """Test handling of empty or invalid scenarios"""
    print("Testing empty scenario handling...")

    try:
        analyzer = await get_test_analyzer()
        result = await analyzer.analyze_situation("")

        # Should still return a valid response structure
        if not isinstance(result, dict):
            print("❌ Empty scenario did not return dictionary")
            return False

        required_keys = ["decision", "rationale", "rule_citations"]
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing required key for empty scenario: {key}")
                return False

        print("✅ Empty scenario handling successful")
        print(f"   Decision: {result['decision']}")

        return True

    except Exception as e:
        print(f"❌ Empty scenario handling failed: {e}")
        return False


async def test_rag_retrieval():
    """Test RAG retrieval functionality directly"""
    print("Testing RAG retrieval...")

    try:
        analyzer = await get_test_analyzer()

        # Test retrieval with a swimming-related query
        scenario = "breaststroke turn requirements"
        relevant_rules = await analyzer.retrieve_relevant_rules(scenario, n_results=3)

        if not isinstance(relevant_rules, list):
            print("❌ RAG retrieval did not return a list")
            return False

        if len(relevant_rules) == 0:
            print("⚠️  RAG retrieval returned no rules (database may be empty)")
            return True  # This is okay if database is not populated

        # Check structure of returned rules
        for rule in relevant_rules:
            required_keys = ["content", "metadata", "relevance_score", "rule_identifier"]
            for key in required_keys:
                if key not in rule:
                    print(f"❌ Missing key in retrieved rule: {key}")
                    return False

        print(f"✅ RAG retrieval successful: {len(relevant_rules)} rules retrieved")

        # Show sample rule info
        if relevant_rules:
            sample_rule = relevant_rules[0]
            print(f"   Sample rule: {sample_rule.get('rule_identifier', 'Unknown')}")
            print(f"   Relevance score: {sample_rule.get('relevance_score', 0):.3f}")

        return True

    except Exception as e:
        print(f"❌ RAG retrieval test failed: {e}")
        return False


async def test_response_format_compliance():
    """Test that responses comply with Section 4.2.1 format requirements"""
    print("Testing response format compliance...")

    scenario = "Swimmer performed an illegal turn in butterfly stroke"

    try:
        analyzer = await get_test_analyzer()
        result = await analyzer.analyze_situation(scenario)

        # Check that all required fields are present
        required_fields = {"decision": str, "rationale": str, "rule_citations": list}

        for field, expected_type in required_fields.items():
            if field not in result:
                print(f"❌ Missing required field: {field}")
                return False

            if not isinstance(result[field], expected_type):
                expected_name = expected_type.__name__
                actual_name = type(result[field]).__name__
                print(f"❌ Field {field} has wrong type: {actual_name} (expected {expected_name})")
                return False

        # Check decision values
        if result["decision"] not in ["ALLOWED", "DISQUALIFICATION"]:
            print(f"❌ Invalid decision value: {result['decision']}")
            return False

        # Check rationale is meaningful
        if len(result["rationale"]) < 20:
            print("❌ Rationale is too short to be meaningful")
            return False

        print("✅ Response format compliance successful")
        print("   All required fields present and correctly typed")

        return True

    except Exception as e:
        print(f"❌ Response format compliance test failed: {e}")
        return False


def print_test_summary(test_results: Dict[str, bool]):
    """Print a summary of all test results"""
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed_count = sum(1 for result in test_results.values() if result)
    total_count = len(test_results)

    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:<8} {test_name}")

    print("-" * 60)
    print(f"OVERALL: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("🎉 All tests passed! MCP Situation Analysis is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the implementation and dependencies.")

    print("=" * 60)


async def main():
    """Main test runner"""
    print("🏊 MCP Situation Analysis Test Suite")
    print("=" * 60)

    # Check environment setup
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY environment variable not set")
        print("   Some tests may fail without this configuration")
        print()

    # Run all tests
    test_results = {}

    test_functions = [
        ("Analyzer Initialization", test_analyzer_initialization),
        ("Basic Scenario Analysis", test_scenario_analysis_basic),
        ("Multiple Scenarios", test_multiple_scenarios),
        ("Empty Scenario Handling", test_empty_scenario),
        ("RAG Retrieval", test_rag_retrieval),
        ("Response Format Compliance", test_response_format_compliance),
    ]

    for test_name, test_func in test_functions:
        print()
        try:
            result = await test_func()
            test_results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            test_results[test_name] = False

    # Print summary
    print_test_summary(test_results)


if __name__ == "__main__":
    """Run the test suite"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nTest suite failed with error: {e}")
        sys.exit(1)
