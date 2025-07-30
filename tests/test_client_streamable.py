import subprocess
import signal
import os
import sys
import time
import pytest

# Allow import from mcp-sentiment directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-sentiment"))
)

for p in sys.path:
    print(f"sys.path: {p}")

from mcp_client_streamable import main


@pytest.fixture(scope="session")
def spawned_program_pid():
    """
    Fixture to spawn a program, yield its PID, and ensure termination after tests.

    Yields:
        int: PID of the spawned process.
    """
    # Start the program (replace with your actual command)
    proc = subprocess.Popen(
        ["python", "mcp-sentiment/app_fastmcp.py", "--transport", "streamable-http"],
    )
    time.sleep(2)  # Give the server time to start
    print(f"Spawned program with PID: {proc.pid}")

    try:
        yield proc.pid
    finally:
        # Terminate the process
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

            proc.kill()


@pytest.mark.parametrize(
    "text, sentiment", [("I hate MCP!", "negative"), ("I love MCP!", "positive")]
)
@pytest.mark.asyncio
async def test_client_full_run(spawned_program_pid, monkeypatch, text, sentiment):
    test_args = ["prog", text]
    monkeypatch.setattr(sys, "argv", test_args)

    results = await main()
    print(f"Results: {results}")

    assert len(results) == 3
    assert results[2] == sentiment
