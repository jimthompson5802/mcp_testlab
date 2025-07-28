# MCP Testbed

This project demonstrates sentiment analysis using the Model Context Protocol (MCP) and is based on the [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course/unit2/introduction).  Instead of using the `gradio` library in the HuggingFace course, this project utilizes the `fastmcp` library to implement an MCP server and client.

## Folder Structure

- `mcp-sentiment/app_fastmcp.py`: MCP server script for sentiment analysis.
- `mcp-sentiment/mcp_client_stdio.py`: MCP client that connects to the server and requests sentiment analysis via command line.
- `mcp-sentiment/mcp_client_sse.py`: MCP client that connects to the server and requests sentiment analysis via SSE transport.

## Usage

To run sentiment analysis from the command line using stdio transport:

```bash
python mcp-sentiment/mcp_client_stdio.py "Your text to test sentiment"
```

To run sentiment analysis from the command line using SSE transport:

```bash
python mcp-sentiment/mcp_client_sse.py "Your text to test sentiment"
```

If no text is provided, the program will exit with an error message.

## How It Works

The application uses Model Context Protocol (MCP) to facilitate communication between a client and a sentiment analysis server. When you run the client with a text string, it:

1. Connects to the server script (`app_fastmcp.py`) or SSE endpoint
2. Sends your text for sentiment analysis
3. Returns the sentiment result (positive, negative, or neutral)

### Server (app_fastmcp.py)

The `app_fastmcp.py` file implements an MCP server using FastMCP that:
- Exposes a sentiment analysis tool via the Model Context Protocol
- Uses TextBlob library to analyze sentiment of provided text
- Returns JSON results with:
  - Polarity score (-1 to 1, negative to positive)
  - Subjectivity score (0 to 1, objective to subjective)
  - Overall assessment (positive, negative, or neutral)
- Supports `stdio` or `sse`transport for communication with clients

### Client (mcp_client_stdio.py)

The `mcp_client_stdio.py` file implements an MCP client that:
- Accepts text input from the command line
- Establishes a connection to the MCP server using stdio transport
- Lists available tools on the connected server
- Sends the input text to the sentiment_analysis tool
- Receives and displays the JSON response with sentiment results
- Properly manages resources with async context managers

### Client (mcp_client_sse.py)

The `mcp_client_sse.py` file implements an MCP client that:
- Accepts text input from the command line
- Establishes a connection to the MCP server using SSE transport
- Lists available tools on the connected server
- Sends the input text to the sentiment_analysis tool
- Receives and displays the JSON response with sentiment results
- Properly manages resources with async context managers

### Example Usage with `stdio` Transport

```bash
((venv) ) Mac:jim mcp_testlab[520]$ python mcp-sentiment/mcp_client_stdio.py "I love python"
```bash
((venv) ) Mac:jim mcp_testlab[520]$ python mcp-sentiment/mcp_client_stdio.py "I love python"

Connected to MCP server. Listing available tools...
[07/27/25 23:34:42] INFO     Processing request of type ListToolsRequest                                                                                                                       server.py:619

tools: ['sentiment_analysis']
                    INFO     Processing request of type CallToolRequest                                                                                                                        server.py:619

Sentiment Analysis Result: [TextContent(type='text', text='{"polarity": 0.5, "subjectivity": 0.6, "assessment": "positive"}', annotations=None, meta=None)]


((venv) ) Mac:jim mcp_testlab[523]$ python mcp-sentiment/mcp_client_stdio.py "I hate python"

Connected to MCP server. Listing available tools...
[07/27/25 23:36:35] INFO     Processing request of type ListToolsRequest                                                                                                                       server.py:619

tools: ['sentiment_analysis']
                    INFO     Processing request of type CallToolRequest                                                                                                                        server.py:619

Sentiment Analysis Result: [TextContent(type='text', text='{"polarity": -0.8, "subjectivity": 0.9, "assessment": "negative"}', annotations=None, meta=None)]
((venv) ) Mac:jim mcp_testlab[524]$ 
```

### Example Usage with `sse` Transport

**Client**
```bash
((venv) ) Mac:jim mcp_testlab[516]$ python mcp-sentiment/mcp_client_sse.py "I love kittens"

Connected to MCP server. Listing available tools...

tools: ['sentiment_analysis']

Sentiment Analysis Result: [TextContent(type='text', text='{"polarity": 0.5, "subjectivity": 0.6, "assessment": "positive"}', annotations=None, meta=None)]


((venv) ) Mac:jim mcp_testlab[517]$ python mcp-sentiment/mcp_client_sse.py "this movie is terrible, a waste of money"

Connected to MCP server. Listing available tools...

tools: ['sentiment_analysis']

Sentiment Analysis Result: [TextContent(type='text', text='{"polarity": -0.6, "subjectivity": 0.5, "assessment": "negative"}', annotations=None, meta=None)]
((venv) ) Mac:jim mcp_testlab[518]$ ```
``` 

**SSE Server**
```bash
((venv) ) Mac:jim mcp_testlab[517]$ python mcp-sentiment/app_fastmcp.py --transport sse
INFO:     Started server process [34093]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:50141 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:50143 - "POST /messages/?session_id=8a3facb39d544dca8acc9cd9af4893d9 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:50143 - "POST /messages/?session_id=8a3facb39d544dca8acc9cd9af4893d9 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:50143 - "POST /messages/?session_id=8a3facb39d544dca8acc9cd9af4893d9 HTTP/1.1" 202 Accepted
[07/28/25 06:51:02] INFO     Processing request of type ListToolsRequest                                                                                                                                               server.py:619
INFO:     127.0.0.1:50143 - "POST /messages/?session_id=8a3facb39d544dca8acc9cd9af4893d9 HTTP/1.1" 202 Accepted
                    INFO     Processing request of type CallToolRequest                                                                                                                                                server.py:619
INFO:     127.0.0.1:50146 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:50148 - "POST /messages/?session_id=68de3cfbb3b7440194c7884e42d85d3c HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:50148 - "POST /messages/?session_id=68de3cfbb3b7440194c7884e42d85d3c HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:50148 - "POST /messages/?session_id=68de3cfbb3b7440194c7884e42d85d3c HTTP/1.1" 202 Accepted
[07/28/25 06:51:06] INFO     Processing request of type ListToolsRequest                                                                                                                                               server.py:619
INFO:     127.0.0.1:50148 - "POST /messages/?session_id=68de3cfbb3b7440194c7884e42d85d3c HTTP/1.1" 202 Accepted
                    INFO     Processing request of type CallToolRequest                                                                                                                                                server.py:619
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [34093]
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
asyncio.exceptions.CancelledError

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/jim/Desktop/modelcontextprotocol/mcp_testlab/mcp-sentiment/app_fastmcp.py", line 52, in <module>
    mcp.run(transport=args.transport)
  File "/Users/jim/Desktop/modelcontextprotocol/mcp_testlab/venv/lib/python3.12/site-packages/mcp/server/fastmcp/server.py", line 228, in run
    anyio.run(lambda: self.run_sse_async(mount_path))
  File "/Users/jim/Desktop/modelcontextprotocol/mcp_testlab/venv/lib/python3.12/site-packages/anyio/_core/_eventloop.py", line 74, in run
    return async_backend.run(func, args, {}, backend_options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/jim/Desktop/modelcontextprotocol/mcp_testlab/venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 2310, in run
    return runner.run(wrapper())
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/lib/python3.12/asyncio/runners.py", line 123, in run
    raise KeyboardInterrupt()
KeyboardInterrupt
```

## MCP Inspector

The MCP Inspector is a tool for exploring and interacting with Model Context Protocol (MCP) servers. It provides a user-friendly interface for:

- Discovering available tools and their capabilities
- Sending requests to tools and viewing responses
- Debugging and testing MCP interactions

### Running MCP Inspector with `stdio` Transport
To run the MCP Inspector for server using `stdio` transport, use the following command:

```bash
mcp dev mcp-sentiment/app_fastmcp.py
```

Sample output will show the available tools and their descriptions, allowing you to interact with the sentiment analysis tool.

### MCP Inspector Listing Tools
![](./images/mcp_inspector_list_tools.png)

### MCP Inspector Testing Sentiment Analysis
![](./images/mcp_inspector_sentiment_tool.png)


### Running MCP Inspector with `sse` Transport



### Starting the `sse` Server for testing
```bash
python mcp-sentiment/app_fastmcp.py --transport sse
```

![](./images/mcp_inspector_starting_sse_server.png)

To run the MCP Inspector for server using `sse` transport, use the following command:

```bash
npx @modelcontextprotocol/inspector
```

### Connecting to the MCP Inspector
Open the browser to access the MCP Inspector interface, change from `http` to `https` if necessary.  Once the MCP Inspector is running, configure "Transport Type" for `sse` and set the server URL to point to your running MCP server (e.g., `http://localhost:8000/sse`) and click "Connect" button.
![](./images/mcp_inspector_connect_sse_server.png)


### MCP Inspector Testing Sentiment Analysis
![](./images/mcp_inspector_sentiment_with_sse_server.png)





## Requirements

- Python 3.12+
- Dependencies: `pip install -r requirements.txt`
- Required NLP libraries for sentiment analysis
- Required version of `node` > v20.x to run MCP Inspector (see [GH Issue on unexpected token](https://github.com/modelcontextprotocol/python-sdk/issues/184#issuecomment-2788071291))


