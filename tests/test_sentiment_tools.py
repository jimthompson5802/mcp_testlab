"""Unit tests for sentiment_tools MCP agent.

Tests the analyze_sentiment tool using various input texts.
"""

import pytest
import sys
import os

from fastmcp import Client

# Allow import from mcp-agent directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-agent"))
)

from sentiment_tools import mcp


@pytest.mark.parametrize(
    "text, expected_assessment",
    [
        ("I love sunny days!", "positive"),
        ("This is terrible and I hate it.", "negative"),
        ("The book was okay.", "positive"),
        ("Absolutely wonderful experience!", "positive"),
        ("I am not happy with the service.", "negative"),
        ("It is a chair.", "neutral"),
    ],
)
@pytest.mark.asyncio
async def test_analyze_sentiment(text: str, expected_assessment: str) -> None:
    """Test the analyze_sentiment function with various text inputs.

    Args:
        text (str): Input text to analyze.
        expected_assessment (str): Expected sentiment assessment ("positive", "negative", "neutral").

    Returns:
        None
    """
    async with Client(mcp) as client:
        result = await client.call_tool("analyze_sentiment", {"text": text})
        assert result.structured_content["assessment"] == expected_assessment
