import pytest
import sys
import os
from unittest.mock import AsyncMock, patch, MagicMock

# Allow import from mcp-sentiment directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-sentiment"))
)

from mcp_client_stdio import MCPClient, main as stdio_main


@pytest.mark.asyncio
class TestMCPClient:
    @pytest.fixture
    def client(self) -> MCPClient:
        """Fixture for MCPClient instance."""
        return MCPClient()

    @pytest.fixture
    def mock_session(self):
        """Fixture for a mock session with call_tool."""
        mock = MagicMock()
        mock.call_tool = AsyncMock()
        return mock

    @pytest.mark.asyncio
    async def test_mcp_request_success_json(self, client, mock_session):
        """Test mcp_request returns parsed JSON when call_tool returns JSON string.

        Args:
            client (MCPClient): The MCP client instance
            mock_session: Mocked session with call_tool
        """
        client.session = mock_session
        mock_session.call_tool.return_value = MagicMock(
            content='{"polarity": 1, "subjectivity": 0.5, "assessment": "positive"}'
        )
        result = await client.mcp_request("Great job!")
        assert result["polarity"] == 1
        assert result["subjectivity"] == 0.5
        assert result["assessment"] == "positive"

    @pytest.mark.asyncio
    async def test_mcp_request_success_list(self, client, mock_session):
        """Test mcp_request handles list of JSON string fragments.

        Args:
            client (MCPClient): The MCP client instance
            mock_session: Mocked session with call_tool
        """
        client.session = mock_session
        mock_session.call_tool.return_value = MagicMock(
            content=['{"polarity": 0, ', '"subjectivity": 1, "assessment": "neutral"}']
        )
        result = await client.mcp_request("Okay.")
        assert result["polarity"] == 0
        assert result["subjectivity"] == 1
        assert result["assessment"] == "neutral"

    @pytest.mark.asyncio
    async def test_mcp_request_list_non_json(self, client, mock_session):
        """Test mcp_request returns raw_content for list of non-JSON strings.

        Args:
            client (MCPClient): The MCP client instance
            mock_session: Mocked session with call_tool
        """
        client.session = mock_session
        mock_session.call_tool.return_value = MagicMock(content=["not", "json"])
        result = await client.mcp_request("???")
        assert "raw_content" in result
        assert result["raw_content"] == "notjson"

    @pytest.mark.asyncio
    async def test_mcp_request_call_tool_exception(self, client, mock_session):
        """Test mcp_request returns error string if call_tool raises exception.

        Args:
            client (MCPClient): The MCP client instance
            mock_session: Mocked session with call_tool
        """
        client.session = mock_session
        mock_session.call_tool.side_effect = Exception("tool error")
        result = await client.mcp_request("fail")
        assert "Error calling sentiment_analysis tool" in result

    @pytest.mark.asyncio
    async def test_mcp_request_invalid_text(self, client):
        """Test mcp_request raises ValueError for invalid text input.

        Args:
            client (MCPClient): The MCP client instance
        """
        client.session = MagicMock()
        with pytest.raises(ValueError):
            await client.mcp_request("")
        with pytest.raises(ValueError):
            await client.mcp_request(None)  # type: ignore

    @pytest.mark.asyncio
    async def test_mcp_request_not_connected(self, client):
        """Test mcp_request raises ConnectionError if not connected.

        Args:
            client (MCPClient): The MCP client instance
        """
        client.session = None
        with pytest.raises(ConnectionError):
            await client.mcp_request("test")


@pytest.mark.asyncio
async def test_stdio_client_full_run(monkeypatch):
    test_args = ["prog", "I love MCP!"]
    monkeypatch.setattr(sys, "argv", test_args)

    results = await stdio_main()

    assert len(results) == 3
    assert results[2] == "positive"
