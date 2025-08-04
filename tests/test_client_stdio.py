import pytest
import sys
import os

# Allow import from mcp-sentiment directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-sentiment"))
)

from mcp_client_stdio import main as stdio_main


@pytest.mark.parametrize(
    "text, sentiment", [("I hate MCP!", "negative"), ("I love MCP!", "positive")]
)
@pytest.mark.asyncio
async def test_client_full_run(monkeypatch, text, sentiment):
    test_args = ["prog", text]
    monkeypatch.setattr(sys, "argv", test_args)

    results = await stdio_main()

    assert len(results) == 3
    assert results[2] == sentiment
