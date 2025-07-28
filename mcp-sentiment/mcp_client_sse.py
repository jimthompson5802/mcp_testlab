import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client


class MCPClient:

    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_url: str):
        """Connect to an MCP server using SSE transport

        Args:
            server_url: URL of the SSE server endpoint
        """

        sse_transport = await self.exit_stack.enter_async_context(
            sse_client(server_url)
        )
        self.sse, self.write = sse_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.sse, self.write)
        )

        await self.session.initialize()

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
    if len(sys.argv) < 2:
        print("Text to test must be specified.")
        sys.exit(1)

    text_to_test = sys.argv[1]

    client = MCPClient()
    try:
        # Use the SSE endpoint URL for the sentiment analysis server
        mcp_server_url = "http://localhost:8000/sse"
        await client.connect_to_server(mcp_server_url)

        print("\nConnected to MCP server. Listing available tools...")
        tools = await client.list_tools()
        print("\ntools:", [tool.name for tool in tools])

        response = await client.mcp_request(text_to_test)
        print("\nSentiment Analysis Result:", response)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
