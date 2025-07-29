import asyncio
import argparse
import json
from typing import Optional, List, Dict, Any, Union
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

    async def mcp_request(self, text: str) -> Union[Dict[str, Any], str]:
        """Use MCP client to call sentiment analysis tool.

        This method sends the provided text to the server for sentiment analysis
        and returns the parsed result.

        Args:
            text: The text to analyze for sentiment

        Returns:
            The sentiment analysis result as a dictionary containing polarity,
            subjectivity, and assessment values, or an error message as string

        Raises:
            RuntimeError: If the client is not connected to a server
        """
        if not self.session:
            raise RuntimeError("Not connected to an MCP server")

        try:
            # Use the session to call the sentiment_analysis tool with the text
            response = await self.session.call_tool(
                "sentiment_analysis", {"text": text}
            )

            # Parse the JSON result into a dictionary
            content = response.content

            # Handle different content types
            if isinstance(content, str):
                return json.loads(content)
            elif isinstance(content, list):
                # Concatenate list items if it's a list of content blocks
                joined_content = "".join(str(item) for item in content)
                try:
                    return json.loads(joined_content)
                except json.JSONDecodeError:
                    return {"raw_content": joined_content}
            else:
                return {"raw_content": str(content)}
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
