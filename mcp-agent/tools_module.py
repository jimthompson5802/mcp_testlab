from fastmcp import FastMCP
from textblob import TextBlob

mcp = FastMCP("MathAndSentiment")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def analyze_sentiment(text: str) -> dict:
    """Analyze text sentiment; returns polarity and subjectivity."""
    blob = TextBlob(text)
    sentiment = blob.sentiment
    assessment = (
        "positive"
        if sentiment.polarity > 0
        else "negative" if sentiment.polarity < 0 else "neutral"
    )
    return {
        "polarity": sentiment.polarity,
        "subjectivity": sentiment.subjectivity,
        "assessment": assessment,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
