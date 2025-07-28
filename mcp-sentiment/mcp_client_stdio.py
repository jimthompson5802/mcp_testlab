import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
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
        mcp_server_script = "mcp-sentiment/app_fastmcp.py"
        await client.connect_to_server(mcp_server_script)

        print("\nConnected to MCP server. Listing available tools...")
        tools = await client.list_tools()
        print("\ntools:", [tool.name for tool in tools])

        response = await client.mcp_request(text_to_test)
        print("\nSentiment Analysis Result:", response)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
