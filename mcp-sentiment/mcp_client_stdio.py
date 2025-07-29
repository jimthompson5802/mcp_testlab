import asyncio
import argparse
import json
from typing import Optional, List, Any, Tuple
from contextlib import AsyncExitStack
import re

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

    async def cleanup(self) -> None:
        """Clean up resources and close connections."""
        if self.exit_stack:
            await self.exit_stack.aclose()


async def run_client(server_script: str, text: str, verbose: bool) -> Tuple:
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
        print("\nConnected to MCP server. Listing available tools...")
        try:
            tools = await client.list_tools()
            if verbose:
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

            print(f"\nAnalyzing sentiment for: '{text}'")
            response = await client.mcp_request(text)

            # Parse the JSON result into a dictionary
            s = response.get("raw_content", response)

            match = re.search(r"text='([^']+)'", s)
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                print(data)
            else:
                raise RuntimeError("Failed to parse sentiment analysis response")

            if isinstance(data, dict):
                print("\nSentiment Analysis Result:")
                print(
                    f"  Polarity: {data.get('polarity', 'N/A')} (-1=negative, 1=positive)"
                )
                print(
                    f"  Subjectivity: {data.get('subjectivity', 'N/A')} (0=objective, 1=subjective)"
                )
                print(f"  Assessment: {data.get('assessment', 'N/A')}")
                polarity = data.get("polarity", "N/A")
                subjectivity = data.get("subjectivity", "N/A")
                assessment = data.get("assessment", "unknown")
            else:
                print(f"\nError: {response}")
        except RuntimeError as e:
            print(f"Error: {e}")
    finally:
        await client.cleanup()

    return polarity, subjectivity, assessment


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
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Display detailed information about available tools",
    )

    return parser.parse_args()


async def main() -> None:
    """Main entry point for the MCP stdio client."""
    args = parse_arguments()
    results = await run_client(args.server, args.text, args.verbose)
    print(f"\nSentiment Analysis Result: {results}")
    return results


if __name__ == "__main__":
    asyncio.run(main())
