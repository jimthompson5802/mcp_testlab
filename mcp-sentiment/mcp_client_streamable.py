import asyncio
import argparse
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:

    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_url: str):
        """Connect to an MCP server using streamable-http transport

        Args:
            server_url: URL of the streamable-http server endpoint
        """

        streamable_transport = await self.exit_stack.enter_async_context(
            streamablehttp_client(server_url)
        )
        self.streamable, self.write, self.get_session_id = streamable_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.streamable, self.write)
        )

        await self.session.initialize()
        # Print session ID using the get_session_id callback
        if self.get_session_id:
            session_id = self.get_session_id()
            if session_id:
                print(f"Session ID: {session_id}")

    async def list_tools(self):
        """List available tools on the MCP server"""

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        return tools

    async def mcp_request(self, text):
        """Use MCP client to call sentiment analysis tool

        Args:
            text: The text to analyze for sentiment

        Returns:
            The sentiment analysis result
        """
        try:
            # Use the session to call the sentiment_analysis tool with the text
            response = await self.session.call_tool(
                "sentiment_analysis", {"text": text}
            )

            # Return the result content
            return response.content
        except Exception as e:
            return f"Error calling sentiment_analysis tool: {e}"

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="MCP Streamable Client for Sentiment Analysis"
    )
    parser.add_argument("text_to_test", type=str, help="Text to analyze for sentiment")
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000/mcp",
        help="URL of the streamable-http server endpoint (default: http://localhost:8000/mcp)",
    )

    # Parse arguments
    args = parser.parse_args()

    client = MCPClient()
    try:
        # Use the provided server URL
        mcp_server_url = args.url
        await client.connect_to_server(mcp_server_url)

        print("\nConnected to MCP server. Listing available tools...")
        tools = await client.list_tools()
        print("\ntools:", [tool.name for tool in tools])

        response = await client.mcp_request(args.text_to_test)
        print("\nSentiment Analysis Result:", response)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
