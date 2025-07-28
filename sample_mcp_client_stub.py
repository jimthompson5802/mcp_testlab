import aiohttp
import asyncio
import json


class MCPClient:
    def __init__(self, sse_url, post_url):
        self.sse_url = sse_url  # Endpoint for SSE connection
        self.post_url = post_url  # Endpoint for sending messages
        self.session_id = None
        self.session = aiohttp.ClientSession()
        self.running = True

    async def connect_sse(self):
        try:
            async with self.session.get(self.sse_url) as resp:
                if resp.status != 200:
                    print(f"Failed to connect to SSE: Status {resp.status}")
                    return
                # Extract session ID from headers
                self.session_id = resp.headers.get("Mcp-Session-Id")
                if not self.session_id:
                    print("No Mcp-Session-Id received in response headers.")
                    return
                print(f"SSE Connected. Session ID: {self.session_id}")

                # Read SSE events line by line
                async for line_bytes in resp.content:
                    line = line_bytes.decode("utf-8").strip()
                    if not line:
                        continue

                    # SSE event lines often start with "data:" - trim it if present
                    if line.startswith("data:"):
                        data_str = line.removeprefix("data:").strip()
                        try:
                            data = json.loads(data_str)
                            print(f"Received event data: {data}")
                            # Example: React to certain message by sending a reply
                            await self.handle_server_event(data)
                        except json.JSONDecodeError:
                            print(f"Received non-JSON data: {data_str}")
        except Exception as e:
            print(f"Exception in SSE connection: {e}")

    async def handle_server_event(self, event_data):
        # Example: On receiving a ping event, send a pong reply
        if "type" in event_data and event_data["type"] == "ping":
            print("Received ping, sending pong")
            await self.send_message({"type": "pong"})

    async def send_message(self, message):
        if not self.session_id:
            print("No session ID; cannot send message.")
            return

        headers = {
            "Mcp-Session-Id": self.session_id,
            "Content-Type": "application/json",
        }
        try:
            async with self.session.post(
                self.post_url, headers=headers, json=message
            ) as resp:
                if resp.status == 200:
                    resp_data = await resp.json()
                    print(f"Sent message response: {resp_data}")
                else:
                    print(f"Failed to send message: Status {resp.status}")
        except Exception as e:
            print(f"Exception in sending message: {e}")

    async def stop(self):
        self.running = False
        await self.session.close()


async def main():
    sse_url = "https://your-mcp-server/sse"  # Replace with your MCP SSE endpoint
    post_url = (
        "https://your-mcp-server/messages"  # Replace with MCP POST message endpoint
    )

    client = MCPClient(sse_url, post_url)

    # Run SSE connection in background task
    sse_task = asyncio.create_task(client.connect_sse())

    # Example: Periodically send messages every 10 seconds
    try:
        count = 0
        while client.running:
            # Wait some time (e.g., 10s)
            await asyncio.sleep(10)
            count += 1
            msg = {"type": "message", "content": f"Hello MCP! Message count: {count}"}
            await client.send_message(msg)
    except asyncio.CancelledError:
        pass
    finally:
        await client.stop()
        await sse_task


if __name__ == "__main__":
    asyncio.run(main())
