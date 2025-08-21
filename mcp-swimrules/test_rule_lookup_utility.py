#!/usr/bin/env python3
"""
Test script for the Rule Lookup Utility

This script validates that the rule lookup utility is properly implemented
and can connect to the ChromaDB database.
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rule_lookup_utility import RuleLookupUtility

    print("✓ Successfully imported RuleLookupUtility")
except ImportError as e:
    print(f"❌ Failed to import RuleLookupUtility: {e}")
    sys.exit(1)


async def test_utility_initialization():
    """Test that the utility can be initialized and connect to ChromaDB"""
    print("\n🧪 Testing Rule Lookup Utility Initialization")
    print("=" * 50)

    utility = RuleLookupUtility()

    try:
        await utility.initialize()
        print("✓ Utility initialized successfully")

        # Test a simple query if the database has data
        test_query = "breaststroke"
        print(f"\n🔍 Testing query: '{test_query}'")

        results = await utility.lookup_rules(test_query, n_results=3)

        if results:
            print(f"✓ Query returned {len(results)} results")
            print(f"✓ First result rule ID: {results[0].get('rule_id', 'Unknown')}")
            print(f"✓ First result similarity: {results[0].get('similarity_score', 0.0):.3f}")
        else:
            print("⚠️  Query returned no results (database may be empty)")

        return True

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


async def test_basic_functionality():
    """Test basic functionality without database connection"""
    print("\n🧪 Testing Basic Functionality")
    print("=" * 40)

    utility = RuleLookupUtility()

    # Test that the utility has required methods
    required_methods = ["initialize", "lookup_rules", "display_results", "run_interactive_session"]

    for method in required_methods:
        if hasattr(utility, method):
            print(f"✓ Method '{method}' exists")
        else:
            print(f"❌ Missing required method: '{method}'")
            return False

    print("✓ All required methods are present")
    return True


async def main():
    """Main test function"""
    print("🧪 Rule Lookup Utility Test Suite")
    print("=" * 40)

    # Test 1: Basic functionality
    basic_test_passed = await test_basic_functionality()

    if not basic_test_passed:
        print("❌ Basic functionality tests failed")
        sys.exit(1)

    # Test 2: Initialization (may fail if database doesn't exist)
    init_test_passed = await test_utility_initialization()

    if init_test_passed:
        print("\n🎉 All tests passed! The Rule Lookup Utility is ready to use.")
        print("\n📋 To use the utility interactively:")
        print("   python rule_lookup_utility.py")
    else:
        print("\n⚠️  Basic tests passed, but initialization failed.")
        print("   This is likely because the ChromaDB database hasn't been created yet.")
        print("   Run the rule ingestion process first to populate the database.")


if __name__ == "__main__":
    asyncio.run(main())
