import pytest
import subprocess
import os
import sys
import time


# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-sentiment")))

from mcp_client_mutli_transport import run_client  # noqa: E402


@pytest.fixture(scope="function")
def spawned_program_pid(transport_endpoint: str):
    """
    Fixture to spawn a program, yield its PID, and ensure termination after tests.

    Yields:
        int: PID of the spawned process.
    """
    if transport_endpoint.startswith("http"):
        if transport_endpoint.endswith("/mcp"):
            # Start the Streamable HTTP server
            proc = subprocess.Popen(
                ["python", "mcp-sentiment/app_fastmcp.py", "--transport", "streamable-http"],
            )
        else:
            # Start the SSE server
            proc = subprocess.Popen(
                ["python", "mcp-sentiment/app_fastmcp.py", "--transport", "sse"],
            )

        time.sleep(2)  # Give the server time to start
        print(f"Spawned program with PID: {proc.pid}")

        try:
            yield proc.pid
        finally:
            # Terminate the process
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()

                proc.kill()
    else:
        # For non-http transports, we assume the server is already running
        yield None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transport_endpoint,test_text,expected_assessment",
    [
        ("mcp-sentiment/app_fastmcp.py", "I love this project, it's amazing!", "positive"),
        ("http://localhost:8000/mcp", "I hate rainy days", "negative"),
        ("http://localhost:8000/sse", "The sky is blue", "neutral"),
    ],
)
async def test_sentiment_analysis_transports(
    spawned_program_pid, transport_endpoint: str, test_text: str, expected_assessment: str
):
    """Test sentiment analysis using different transport protocols.

    This test verifies that the sentiment analysis works correctly with
    different transport types (stdio, streamable-http, SSE).

    Args:
        transport_endpoint: The endpoint for the MCP server
        test_text: The text to analyze
        expected_assessment: The expected sentiment assessment
    """

    # Run the client with the specified transport
    polarity, subjectivity, assessment = await run_client(transport_endpoint, test_text, False)

    # Verify the results
    assert isinstance(polarity, (float, str))
    assert isinstance(subjectivity, (float, str))
    assert assessment.lower() == expected_assessment.lower()


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling when the server is not available."""
    with pytest.raises(Exception):
        # This should fail because the endpoint doesn't exist
        await run_client("nonexistent_endpoint", "test", False)
