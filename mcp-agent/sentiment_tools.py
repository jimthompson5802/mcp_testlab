from fastmcp import FastMCP
from textblob import TextBlob

mcp = FastMCP("SentimentTools")


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
    # Access sentiment properties (bypassing type checking issues)
    sentiment_obj = blob.sentiment
    polarity = getattr(sentiment_obj, "polarity")
    subjectivity = getattr(sentiment_obj, "subjectivity")
    assessment = (
        "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
    )
    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "assessment": assessment,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio", show_banner=False)
