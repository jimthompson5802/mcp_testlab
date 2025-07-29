import asyncio
import argparse
import json
from typing import Optional, List, Dict, Any, Union, Callable
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:
    """Client for interacting with an MCP server using streamable-http transport.

    This class provides methods to connect to an MCP server, list available tools,
    and make sentiment analysis requests using the Model Context Protocol.
    """

    def __init__(self):
        """Initialize the MCP client with required resources.

        Sets up the session and AsyncExitStack for resource management.
        """
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack: AsyncExitStack = AsyncExitStack()
        self.streamable: Any = None
        self.write: Any = None
        self.get_session_id: Optional[Callable[[], Optional[str]]] = None

    async def connect_to_server(self, server_url: str) -> None:
        """Connect to an MCP server using streamable-http transport.

        Sets up the streamable HTTP transport and initializes the client session.

        Args:
            server_url: URL of the streamable-http server endpoint

        Returns:
            None

        Raises:
            ConnectionError: If connection to the server fails
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

    async def list_tools(self) -> List[Any]:
        """List available tools on the MCP server.

        Retrieves the list of tools available on the connected MCP server.

        Returns:
            List of tool objects provided by the MCP server

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

        Sends the provided text to the server using the 'sentiment_analysis' tool,
        and returns the parsed sentiment analysis result.

        Args:
            text (str): The text to analyze for sentiment.

        Returns:
            dict: Sentiment analysis result containing polarity, subjectivity, and assessment.
            str: Error message if the request fails.

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
        """Clean up resources.

        Closes all resources managed by the AsyncExitStack.

        Returns:
            None
        """
        await self.exit_stack.aclose()


async def main() -> None:
    """Main entry point for the MCP Streamable client application.

    Parses command-line arguments, connects to the MCP server,
    lists available tools, and performs sentiment analysis on the provided text.

    Returns:
        None
    """
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
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Display detailed information about available tools",
    )

    # Parse arguments
    args = parser.parse_args()

    client = MCPClient()
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
            else:
                print(f"\nError: {response}")
        except RuntimeError as e:
            print(f"Error: {e}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
