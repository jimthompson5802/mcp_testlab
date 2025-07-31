"""Unit tests for math_tools MCP agent.

Tests the add and multiply tools using various input pairs.
"""

import pytest
import sys
import os

from fastmcp import FastMCP, Client

# Allow import from mcp-sentiment directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-agent"))
)


from math_tools import mcp


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 8),  # Positive numbers
        (-2, -7, -9),  # Negative numbers
        (10, 0, 10),  # Zero as second operand
        (0, 15, 15),  # Zero as first operand
    ],
)
@pytest.mark.asyncio
async def test_add(a: int, b: int, expected: int) -> None:
    """Test the add function with various number pairs.

    Args:
        a (int): First operand.
        b (int): Second operand.
        expected (int): Expected sum.

    Returns:
        None
    """
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": a, "b": b})
        assert result.structured_content["result"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 15),  # Positive numbers
        (-2, -7, 14),  # Negative numbers with positive result
        (10, 0, 0),  # Zero as second operand
        (0, 15, 0),  # Zero as first operand
        (-8, 12, -96),  # Mixed signs
    ],
)
async def test_multiply(a: int, b: int, expected: int) -> None:
    """Test the multiply function with various number pairs.

    Args:
        a (int): First operand.
        b (int): Second operand.
        expected (int): Expected product.

    Returns:
        None
    """
    async with Client(mcp) as client:
        result = await client.call_tool("multiply", {"a": a, "b": b})
        assert result.structured_content["result"] == expected
