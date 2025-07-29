import asyncio
import argparse
from typing import Optional, List, Any
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client


class MCPClient:
    """Client for interacting with an MCP server using stdio transport.

    This class handles connection setup, tool discovery, and sentiment analysis
    requests using the Model Context Protocol.
    """

    def __init__(self):
        """Initialize the MCP client with required resources."""
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str) -> None:
        """Connect to an MCP server using stdio transport.

        Args:
            server_script_path: Path to the server script (.py or .js)

        Raises:
            ValueError: If the server script is not a .py or .js file
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

    async def list_tools(self) -> List[Tool]:
        """List available tools on the MCP server.

        Returns:
            List of Tool objects available on the connected MCP server

        Raises:
            ConnectionError: If not connected to a server
            RuntimeError: If the tool listing fails
        """
        if not self.session:
            raise ConnectionError("Not connected to an MCP server")

        try:
            # List available tools
            response = await self.session.list_tools()
            return response.tools
        except Exception as e:
            raise RuntimeError(f"Failed to list tools: {e}")

    async def mcp_request(self, text: str) -> Any:
        """Use MCP client to call sentiment analysis tool.

        Args:
            text: The text to analyze for sentiment

        Returns:
            The sentiment analysis result

        Raises:
            ConnectionError: If not connected to a server
            ValueError: If the input text is invalid
            RuntimeError: If the sentiment analysis fails
        """
        if not self.session:
            raise ConnectionError("Not connected to an MCP server")

        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")

        try:
            # Use the session to call the sentiment_analysis tool with the text
            response = await self.session.call_tool(
                "sentiment_analysis", {"text": text}
            )

            # Return the result content
            return response.content
        except ValueError as e:
            raise ValueError(f"Invalid input for sentiment analysis: {e}")
        except Exception as e:
            raise RuntimeError(f"Error calling sentiment_analysis tool: {e}")

    async def cleanup(self) -> None:
        """Clean up resources and close connections."""
        if self.exit_stack:
            await self.exit_stack.aclose()


async def run_client(server_script: str, text: str) -> None:
    """Run the MCP client with the specified server and text.

    Args:
        server_script: Path to the server script
        text: Text to analyze for sentiment
    """
    client = MCPClient()
    try:
        await client.connect_to_server(server_script)

        print(f"\nConnected to MCP server at {server_script}")
        print("Listing available tools...")

        tools = await client.list_tools()
        print("\nAvailable tools:", [tool.name for tool in tools])

        print(f"\nAnalyzing sentiment for: '{text}'")
        response = await client.mcp_request(text)
        print("\nSentiment Analysis Result:", response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.cleanup()


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="MCP Client for sentiment analysis using stdio transport"
    )
    parser.add_argument("text", help="Text to analyze for sentiment")
    parser.add_argument(
        "--server",
        default="mcp-sentiment/app_fastmcp.py",
        help="Path to the MCP server script (default: mcp-sentiment/app_fastmcp.py)",
    )
    return parser.parse_args()


async def main() -> None:
    """Main entry point for the MCP stdio client."""
    args = parse_arguments()
    await run_client(args.server, args.text)


if __name__ == "__main__":
    asyncio.run(main())
