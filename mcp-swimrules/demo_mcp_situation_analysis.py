#!/usr/bin/env python3
"""
Demo script for MCP Situation Analysis

This script demonstrates how to use the mcp_situation_analysis.py module
and runs basic tests to validate functionality.
"""

import asyncio
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_situation_analysis import SwimRulesRAGAnalyzer


async def demo_situation_analysis():
    """Demonstrate the situation analysis functionality"""
    print("🏊 MCP Situation Analysis Demo")
    print("=" * 50)

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Analysis may not work properly.")
        print("   Please set your OpenAI API key as an environment variable.")
        print()

    try:
        # Initialize the analyzer
        print("Initializing the swim rules analyzer...")
        analyzer = SwimRulesRAGAnalyzer()
        await analyzer.initialize()
        print("✅ Analyzer initialized successfully!")
        print()

        # Test scenarios
        test_scenarios = [
            "Swimmer did not touch the wall with both hands during breaststroke turn",
            "Swimmer left the starting block before the starting signal",
            "Swimmer performed a normal freestyle stroke and finish",
            "Swimmer did butterfly kick during breaststroke",
        ]

        for i, scenario in enumerate(test_scenarios, 1):
            print(f"Test {i}: {scenario}")
            print("-" * 40)

            try:
                result = await analyzer.analyze_situation(scenario)

                print(f"Decision: {result['decision']}")
                rationale = result["rationale"]
                if len(rationale) > 100:
                    print(f"Rationale: {rationale[:100]}...")
                else:
                    print(f"Rationale: {rationale}")
                print(f"Rule Citations: {result['rule_citations']}")
                print()

            except Exception as e:
                print(f"❌ Error analyzing scenario: {e}")
                print()

        print("🎉 Demo completed successfully!")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("This may be due to missing dependencies or configuration.")


if __name__ == "__main__":
    """Run the demo"""
    print("Starting MCP Situation Analysis Demo...")
    try:
        asyncio.run(demo_situation_analysis())
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
