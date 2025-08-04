import asyncio
import argparse
import json
from typing import Tuple

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


async def run_client(server_url: str, text: str, verbose: bool) -> Tuple:
    """Run the MCP client with the specified server and text.

    Args:
        server_script: Path to the server script
        text: Text to analyze for sentiment
    """
    transport = StreamableHttpTransport(url=server_url)

    client = Client(transport)
    polarity, subjectivity, assessment = "N/A", "N/A", "unknown"
    print(f"\nConnected to MCP server at {server_url}")

    async with client:
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
            response = await client.call_tool("sentiment_analysis", {"text": text})

            data = json.loads(response.data.result)
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

    return polarity, subjectivity, assessment


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed command line arguments
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="MCP Streamable HTTP Client for Sentiment Analysis"
    )
    parser.add_argument("text_to_test", type=str, help="Text to analyze for sentiment")
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000/mcp",
        help="URL of the MCP server endpoint (default: http://localhost:8000/mcp)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Display detailed information about available tools",
    )

    # Parse arguments
    return parser.parse_args()


async def main() -> Tuple:
    """Main entry point for the MCP stdio client."""
    args = parse_arguments()
    results = await run_client(args.url, args.text_to_test, args.verbose)
    print(f"\nSentiment Analysis Result: {results}")
    return results


if __name__ == "__main__":
    asyncio.run(main())
