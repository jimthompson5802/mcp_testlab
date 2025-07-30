import asyncio
import argparse
import json
from typing import Optional, List, Dict, Any, Union, Tuple
from contextlib import AsyncExitStack

from mcp import ClientSession, Tool
from mcp.client.sse import sse_client


class MCPClient:
    """Client for interacting with an MCP server using SSE transport.

    This class handles connection setup, tool discovery, and sentiment analysis
    requests using the Model Context Protocol over Server-Sent Events.
    """

    def __init__(self):
        """Initialize the MCP client with required resources."""
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_url: str) -> None:
        """Connect to an MCP server using SSE transport.

        This method establishes a connection to the specified MCP server endpoint
        using Server-Sent Events transport protocol.

        Args:
            server_url: URL of the SSE server endpoint

        Raises:
            ConnectionError: If connection to the server fails
        """
        try:
            sse_transport = await self.exit_stack.enter_async_context(
                sse_client(server_url)
            )
            self.sse, self.write = sse_transport
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(self.sse, self.write)
            )

            await self.session.initialize()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MCP server: {e}") from e

    async def list_tools(self) -> List[Tool]:
        """List available tools on the MCP server.

        Returns:
            List of Tool objects available on the connected MCP server

        Raises:
            RuntimeError: If the client is not connected to a server
        """
        if not self.session:
            raise RuntimeError("Not connected to an MCP server")

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        return tools

    async def mcp_request(self, text: str) -> Union[Dict[str, Any], str]:
        """Send a sentiment analysis request to the MCP server.

        This method sends the provided text to the sentiment_analysis tool on the
        connected MCP server and returns the parsed sentiment analysis result.

        Args:
            text (str): The text to analyze for sentiment.

        Returns:
            Dict[str, Any]: The sentiment analysis result as a dictionary containing
                polarity, subjectivity, and assessment values.
            str: An error message if the request fails.

        Raises:
            RuntimeError: If the client is not connected to a server.
        """
        if not self.session:
            raise RuntimeError("Not connected to an MCP server")

        try:
            # Use the session to call the sentiment_analysis tool with the text
            response = await self.session.call_tool(
                "sentiment_analysis", {"text": text}
            )

            return json.loads(response.structuredContent.get("result", "{}"))
        except Exception as e:
            return f"Error calling sentiment_analysis tool: {e}"

    async def cleanup(self) -> None:
        """Clean up resources and close connections.

        This method should be called when the client is no longer needed
        to ensure proper cleanup of all resources.
        """
        await self.exit_stack.aclose()


async def main() -> tuple[Any | None, Any | None, Any | None]:
    """Main entry point for the MCP SSE client.

    Parses command-line arguments, connects to the MCP server using SSE transport,
    lists available tools, and performs sentiment analysis on the provided text.

    Args:
        None

    Returns:
        tuple: A tuple containing the polarity, subjectivity, and assessment values from the sentiment analysis,
            or None for each if unavailable.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="MCP SSE Client for Sentiment Analysis"
    )
    parser.add_argument("text_to_test", type=str, help="Text to analyze for sentiment")
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000/sse",
        help="URL of the SSE server endpoint (default: http://localhost:8000/sse)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Display detailed information about available tools",
    )

    # Parse arguments
    args = parser.parse_args()

    client = MCPClient()
    polarity, subjectivity, assessment = None, None, None
    try:
        print(f"Connecting to MCP server at {args.url}...")
        try:
            await client.connect_to_server(args.url)
        except ConnectionError as e:
            print(f"Connection failed: {e}")
            return

        print("\nConnected to MCP server. Listing available tools...")
        try:
            tools = await client.list_tools()
            if args.verbose:
                # Display detailed information about each tool
                for tool in tools:
                    print(f"\n{tool.name}:")
                    print(f"  Description: {tool.description}")
                    # Display any other available attributes
                    for attr in dir(tool):
                        if not attr.startswith("_") and attr not in (
                            "name",
                            "description",
                        ):
                            try:
                                value = getattr(tool, attr)
                                if not callable(value):
                                    print(f"  {attr.capitalize()}: {value}")
                            except Exception:
                                pass
            else:
                # Just display the tool names
                print("\nAvailable tools:", [tool.name for tool in tools])

            print(f"\nAnalyzing sentiment for: '{args.text_to_test}'")
            response = await client.mcp_request(args.text_to_test)

            if isinstance(response, dict):
                print("\nSentiment Analysis Result:")
                print(
                    f"  Polarity: {response.get('polarity', 'N/A')} (-1=negative, 1=positive)"
                )
                print(
                    f"  Subjectivity: {response.get('subjectivity', 'N/A')} (0=objective, 1=subjective)"
                )
                print(f"  Assessment: {response.get('assessment', 'N/A')}")
                polarity = response.get("polarity")
                subjectivity = response.get("subjectivity")
                assessment = response.get("assessment")
            else:
                print(f"\nError: {response}")
        except RuntimeError as e:
            print(f"Error: {e}")
    finally:
        await client.cleanup()

    return polarity, subjectivity, assessment


if __name__ == "__main__":
    asyncio.run(main())
