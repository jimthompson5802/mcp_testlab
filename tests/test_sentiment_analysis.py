import json
import pytest

import sys
import os

# Allow import from mcp-sentiment directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-sentiment"))
)

from app_fastmcp import sentiment_analysis


@pytest.mark.parametrize(
    "text,expected_assessment",
    [
        ("I love this product. It's fantastic!", "positive"),
        ("This is the worst experience I've ever had.", "negative"),
        ("The product is okay. Nothing special.", "positive"),
        ("", "neutral"),
        ("I like the design, but the performance is terrible.", "negative"),
        ("I have mixed feelings about this.", "neutral"),
        ("", "neutral"),  # Empty string case
        ("12345", "neutral"),  # Numeric input
        ("@#$%^&*()", "neutral"),  # Special characters
    ],
)
def test_sentiment_analysis_assessment(text: str, expected_assessment: str):
    """
    Test sentiment_analysis assessment output for various inputs.

    Args:
        text (str): Input text for sentiment analysis
        expected_assessment (str): Expected sentiment assessment
    """
    result_json = sentiment_analysis(text)
    result = json.loads(result_json)
    assert "polarity" in result
    assert "subjectivity" in result
    assert "assessment" in result
    assert isinstance(result["polarity"], float)
    assert isinstance(result["subjectivity"], float)
    assert result["assessment"] == expected_assessment


def test_sentiment_analysis_error_handling(monkeypatch):
    """
    Test sentiment_analysis error handling for unexpected input.
    """

    def mock_textblob_fail(text):
        raise Exception("TextBlob failure")

    monkeypatch.setattr("app_fastmcp.TextBlob", mock_textblob_fail)
    with pytest.raises(Exception):
        sentiment_analysis("This should fail")
