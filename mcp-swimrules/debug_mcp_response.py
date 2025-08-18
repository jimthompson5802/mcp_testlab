#!/usr/bin/env python3
"""
Debug script to examine the actual MCP response format from the analyze_situation tool
"""

import asyncio
import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastmcp import Client
from fastmcp.client.transports import StdioTransport


async def debug_mcp_response():
    """Debug the actual response format from MCP server"""

    print("Debugging MCP Response Format")
    print("=" * 40)

    # Initialize transport and client
    transport = StdioTransport(command="python", args=["mcp_situation_analysis.py"])

    client = Client(transport)

    try:
        async with client:
            print("✓ Connected to MCP server")

            # List available tools first
            tools = await client.list_tools()
            print(f"✓ Available tools: {[tool.name for tool in tools]}")

            # Test scenario
            test_scenario = "Swimmer did not touch the wall with both hands during breaststroke turn"
            print(f"\n📝 Testing scenario: {test_scenario}")

            # Call the tool and examine the response
            response = await client.call_tool("analyze_situation", {"scenario": test_scenario})

            print(f"\n🔍 Raw response type: {type(response)}")
            print(f"🔍 Raw response: {response}")

            if hasattr(response, "data"):
                print(f"🔍 Response.data type: {type(response.data)}")
                print(f"🔍 Response.data: {response.data}")

                if hasattr(response.data, "result"):
                    print(f"🔍 Response.data.result type: {type(response.data.result)}")
                    print(f"🔍 Response.data.result: {response.data.result}")

            # Try to access other attributes
            for attr in dir(response):
                if not attr.startswith("_"):
                    try:
                        value = getattr(response, attr)
                        print(f"🔍 response.{attr}: {value} (type: {type(value)})")
                    except Exception as e:
                        print(f"🔍 response.{attr}: Error accessing - {e}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(debug_mcp_response())
