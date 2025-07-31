from fastmcp import FastMCP
from textblob import TextBlob

mcp = FastMCP("MathAndSentiment")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: The first integer to add.
        b: The second integer to add.

    Returns:
        int: The sum of a and b.
    """
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers.

    Args:
        a: The first integer to multiply.
        b: The second integer to multiply.

    Returns:
        int: The product of a and b.
    """
    return a * b


@mcp.tool()
def analyze_sentiment(text: str) -> dict:
    """Analyze the sentiment of provided text.

    This function uses TextBlob to determine the emotional tone of the input text.
    It evaluates both polarity (positive/negative) and subjectivity (objective/subjective).

    Args:
        text: The input text string to analyze for sentiment

    Returns:
        dict: A dictionary containing:
            - polarity: Float between -1.0 (negative) and 1.0 (positive)
            - subjectivity: Float between 0.0 (objective) and 1.0 (subjective)
            - assessment: String classification ("positive", "negative", or "neutral")
    """
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
