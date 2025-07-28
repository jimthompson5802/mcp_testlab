import json
from textblob import TextBlob
import argparse

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Text Sentiment Analysis", log_level="DEBUG")


@mcp.tool()
def sentiment_analysis(text: str) -> str:
    """
    Analyze the sentiment of the given text.

    Args:
        text (str): The text to analyze

    Returns:
        str: A JSON string containing polarity, subjectivity, and assessment
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment

    result = {
        "polarity": round(sentiment.polarity, 2),  # -1 (negative) to 1 (positive)
        "subjectivity": round(
            sentiment.subjectivity, 2
        ),  # 0 (objective) to 1 (subjective)
        "assessment": (
            "positive"
            if sentiment.polarity > 0
            else "negative" if sentiment.polarity < 0 else "neutral"
        ),
    }

    return json.dumps(result)


if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="MCP Sentiment Analysis Server")
    parser.add_argument(
        "--transport",
        type=str,
        default="stdio",
        help="MCP Server transport, default is 'stdio'",
    )
    args = parser.parse_args()

    # Run the MCP server with the specified transport
    mcp.run(transport=args.transport)
