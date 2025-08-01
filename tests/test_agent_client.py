"""Unit tests for agent_client.py MCP agent.

Tests the agent client components including state transitions, message handling,
and graph execution using mocked components.
"""

import pytest
import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
from langchain.schema import AIMessage, HumanMessage
from langgraph.graph import END

# Allow import from mcp-agent directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-agent"))
)

# Import the module to test
from agent_client import (
    SYSTEM_MESSAGE,
    should_continue,
    call_model,
    should_exit,
    async_input,
    prompt_user,
    print_result,
    main,
)


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables."""
    # Store original environment
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ["OPENAI_API_KEY"] = "test_key"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.mark.asyncio
async def test_should_continue():
    """Test the should_continue function with different message states."""
    # Test with tool calls
    state_with_tool_calls = {"messages": [MagicMock(tool_calls=["some_tool"])]}
    assert should_continue(state_with_tool_calls) == "tools"

    # Test without tool calls
    state_without_tool_calls = {"messages": [MagicMock(tool_calls=None)]}
    assert should_continue(state_without_tool_calls) == END


@pytest.mark.asyncio
async def test_should_exit():
    """Test the should_exit function."""
    # Should exit
    state_exit = {"exit": True}
    assert should_exit(state_exit) == END

    # Should continue
    state_continue = {"exit": False}
    assert should_exit(state_continue) == "prompt_user"

    # Default case (no exit key)
    state_default = {}
    assert should_exit(state_default) == "prompt_user"


@pytest.mark.asyncio
async def test_call_model():
    """Test the call_model function with a mocked model."""
    with patch("agent_client.model_with_tools") as mock_model:
        # Setup mock
        mock_response = AIMessage(content="Test response")
        mock_model.ainvoke = AsyncMock(return_value=mock_response)

        # Test
        state = {"messages": [HumanMessage(content="Test input")]}
        result = await call_model(state)

        # Verify
        mock_model.ainvoke.assert_called_once_with([HumanMessage(content="Test input")])
        assert result == {"messages": [mock_response]}


@pytest.mark.asyncio
async def test_async_input():
    """Test the async_input function with mocked input."""
    with patch("agent_client.asyncio.to_thread") as mock_to_thread:
        # Setup mock
        future = asyncio.Future()
        future.set_result("test input")
        mock_to_thread.return_value = future

        # Test
        with patch("builtins.print") as mock_print:
            result = await async_input("Prompt: ")

        # Verify
        mock_to_thread.assert_called_once_with(input)
        mock_print.assert_called_once()
        assert result.result() == "test input"


@pytest.mark.asyncio
async def test_prompt_user_with_input():
    """Test the prompt_user function with user input."""
    with patch("agent_client.async_input") as mock_input:
        # Setup mock
        future = asyncio.Future()
        future.set_result("test question")
        mock_input.return_value = future

        # Test
        with patch("builtins.print"):
            result = await prompt_user({})

        # Verify that async_input was called once
        mock_input.assert_called_once()
        # Ensure the result contains the expected keys
        assert "messages" in result
        assert "exit" in result

        # Should not exit when user provides input
        assert not result["exit"]

        # The first message should be from the user
        assert result["messages"][0]["role"] == "user"

        # The content should match the mocked input
        assert result["messages"][0]["content"].result() == "test question"


@pytest.mark.asyncio
async def test_prompt_user_with_eof():
    """Test the prompt_user function with EOFError exception."""
    with patch("agent_client.async_input") as mock_input:
        # Setup mock to raise EOFError
        mock_input.side_effect = EOFError()

        # Test
        with patch("builtins.print") as mock_print:
            result = await prompt_user({})

        # Verify
        assert result == {"messages": [], "exit": True}
        mock_print.assert_called_with("\nEOF detected. Exiting...")


@pytest.mark.asyncio
async def test_print_result_with_content():
    """Test the print_result function with message content."""
    # Test with content
    with patch("builtins.print") as mock_print:
        state = {"messages": [AIMessage(content="Test response")]}
        result = await print_result(state)
        mock_print.assert_called_with("\nResponse: Test response")
        assert result == state


@pytest.mark.asyncio
async def test_print_result_without_content():
    """Test the print_result function without message content."""
    # Test without content attribute
    with patch("builtins.print") as mock_print:
        mock_message = MagicMock()
        del mock_message.content
        state = {"messages": [mock_message]}
        result = await print_result(state)
        mock_print.assert_called_once()
        assert result == state


@pytest.mark.asyncio
async def test_print_result_empty_messages():
    """Test the print_result function with empty messages."""
    # Test with empty messages
    with patch("builtins.print") as mock_print:
        state = {"messages": []}
        result = await print_result(state)
        mock_print.assert_not_called()
        assert result == state


@pytest.mark.asyncio
async def test_main_success():
    """Test successful execution of main function."""
    with patch("agent_client.interactive_graph") as mock_graph, patch("builtins.print"):

        # Setup mock
        mock_graph.ainvoke = AsyncMock()

        # Test
        await main()

        # Verify
        mock_graph.ainvoke.assert_called_once()
        assert mock_graph.ainvoke.call_args[0][0]["messages"][0] == SYSTEM_MESSAGE
        assert mock_graph.ainvoke.call_args[0][0]["exit"] is False


@pytest.mark.asyncio
async def test_main_exception():
    """Test main function handling exceptions."""
    with patch("agent_client.interactive_graph") as mock_graph, patch(
        "builtins.print"
    ) as mock_print:

        # Setup mock to raise exception
        mock_graph.ainvoke = AsyncMock(side_effect=Exception("Test error"))

        # Test
        await main()

        # Verify error was handled
        mock_print.assert_any_call("Error: Test error")
        mock_print.assert_any_call("Agent terminated due to an error.")
