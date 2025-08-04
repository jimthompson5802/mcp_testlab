# MCP Testbed

## Overview

This README provides documentation for the MCP Testbed, a project demonstrating sentiment analysis using the Model Context Protocol (MCP). It describes the architecture, main components, directory structure, and usage examples for the MCP server and three client implementations (stdio, SSE, and streamable-http). The guide includes instructions for running tests, using the MCP Inspector tool, and interacting with the sentiment analysis service via command-line or web-based transports.

## Main Components

### Architecture Diagram
```
+-------------------+                   +-------------------+
|                   |                   |                   |
| mcp_client_stdio  |<----------------->|                   |
|                   |      stdio        |                   |
+-------------------+                   |                   |
                                        |                   |
+-------------------+                   |                   |
|                   |<----------------->|                   |
| mcp_client_sse    |-----/sse--------->|   MCP Server      |
|                   |                   | (app_fastmcp.py)  |
+-------------------+                   |                   |
                                        |                   |
+-------------------+                   |                   |
|                   |<----------------->|                   |
| mcp_client_stream |----/mcp---------->|                   |
|     streamable.py |                   |                   |
+-------------------+                   +-------------------+
```

Each client module communicates with the MCP server using a different transport protocol:
- `mcp_client_stdio.py` uses stdio
- `mcp_client_sse.py` uses SSE (Server-Sent Events) at `/sse`
- `mcp_client_streamable.py` uses streamable-http at `/mcp`
- `mcp_client_multi_transport.py` supports all three transports

### Server

- **mcp-sentiment/app_fastmcp.py**  
  Implements the MCP server using FastMCP. Exposes a `sentiment_analysis` tool that uses TextBlob to analyze the sentiment of input text and returns polarity, subjectivity, and an overall assessment as JSON.

### Clients

- **mcp-sentiment/mcp_client_stdio.py**  
  MCP client using stdio transport. Connects to the server via subprocess, lists available tools, and sends text for sentiment analysis. Uses argparse for CLI.

- **mcp-sentiment/mcp_client_sse.py**  
  MCP client using Server-Sent Events (SSE) transport. Connects to the server via HTTP SSE endpoint, lists tools, and sends text for analysis. Uses argparse for CLI.

- **mcp-sentiment/mcp_client_streamable.py**  
  MCP client using streamable-http transport. Connects to the server via HTTP with bidirectional streaming, lists tools, and sends text for analysis. Uses argparse for CLI.

- **mcp-sentiment/mcp_client_multi_transport.py**  
  MCP client that can operate over multiple transports (`stdio`, `sse`, `streamable-http`). Connects to the server, lists available tools, and sends text for sentiment analysis. Uses argparse for CLI.

### Tests

- **tests/test_sentiment_analysis.py**  
  Unit tests for the sentiment analysis tool, checking various input cases and error handling.

- **tests/test_client_stdio.py**  
  Tests for the stdio client, including unit tests for request handling and integration tests for end-to-end sentiment analysis.

- **tests/test_client_sse.py**  
  Integration tests for the SSE client, including server process management and sentiment analysis checks.

- **tests/test_client_streamable.py**  
  Integration tests for the streamable-http client, including server process management and sentiment analysis checks.


## How It Works

The application uses Model Context Protocol (MCP) to facilitate communication between a client and a sentiment analysis server. When you run the client with a text string, it:

1. Connects to the server script (`app_fastmcp.py`) or `sse`/`streamable-http` endpoint
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
- Supports `stdio`, `sse`, or `streamable-http` transport for communication with clients

### Client (mcp_client_stdio.py)

The `mcp_client_stdio.py` file implements an MCP client that:
- Uses the argparse library for command-line argument handling
- Accepts text input as a required positional argument
- Accepts an optional `--server` parameter to specify the server script path (default: `mcp-sentiment/app_fastmcp.py`)
- Accepts an optional `--verbose` or `-v` flag to display detailed tool information
- Establishes a connection to the MCP server using stdio transport
- Lists available tools on the connected server
- Sends the input text to the `sentiment_analysis` tool
- Displays formatted sentiment results showing polarity, subjectivity, and assessment
- Properly manages resources with async context managers and AsyncExitStack

### Client (mcp_client_sse.py)

The `mcp_client_sse.py` file implements an MCP client that:
- Uses the argparse library for command-line argument handling
- Accepts text input as a required positional argument
- Accepts an optional `--url` parameter to specify the server endpoint (default: `http://localhost:8000/sse`)
- Accepts an optional `--verbose` or `-v` flag to display detailed tool information
- Establishes a connection to the MCP server using SSE transport
- Lists available tools on the connected server
- Sends the input text to the `sentiment_analysis` tool
- Displays formatted sentiment results showing polarity, subjectivity, and assessment
- Properly manages resources with async context managers and AsyncExitStack

### Client (mcp_client_streamable.py)

The `mcp_client_streamable.py` file implements an MCP client that:
- Uses the argparse library for command-line argument handling
- Accepts text input as a required positional argument
- Accepts an optional `--url` parameter to specify the server endpoint (default: `http://localhost:8000/mcp`)
- Accepts an optional `--verbose` or `-v` flag to display detailed tool information
- Establishes a connection to the MCP server using streamable-http transport
- Displays the session ID when available
- Lists available tools on the connected server
- Sends the input text to the `sentiment_analysis` tool
- Displays formatted sentiment results showing polarity, subjectivity, and assessment
- Properly manages resources with async context managers and AsyncExitStack

### Client (mcp_client_multi_transport.py)

The `mcp_client_multi_transport.py` file implements an MCP client that:
- Uses the argparse library for command-line argument handling
- Accepts text input as a required positional argument
- Accepts an optional `--endpoint` parameter to specify MCP server endpoint (python module for `stdio` or the streamable-http (\*/mcp) or SSE (\*/sse) transport type (default: `mcp-sentiment/app_fastmcp.py`)
- Accepts an optional `--verbose` or `-v` flag to display detailed tool information
- Establishes a connection to the MCP server using the selected transport
- Lists available tools on the connected server
- Sends the input text to the `sentiment_analysis` tool
- Displays formatted sentiment results showing polarity, subjectivity, and assessment
- Properly manages resources with async context managers and AsyncExitStack

### Example Usage with `stdio` Transport

**Command-line Arguments**
```bash
((venv) ) Mac:jim mcp_testlab[529]$ python mcp-sentiment/mcp_client_stdio.py --help
usage: mcp_client_stdio.py [-h] [--server SERVER] [--verbose] text

MCP Client for sentiment analysis using stdio transport

positional arguments:
  text             Text to analyze for sentiment

options:
  -h, --help       show this help message and exit
  --server SERVER  Path to the MCP server script (default: mcp-sentiment/app_fastmcp.py)
  --verbose, -v    Display detailed information about available tools


**Client**
```bash
((venv) ) Mac:jim mcp_testlab[512]$ python mcp-sentiment/mcp_client_stdio.py "i love  mcp"

Connected to MCP server at mcp-sentiment/app_fastmcp.py
Listing available tools...
[07/29/25 13:45:16] INFO     Processing request of type ListToolsRequest                                                             server.py:619

Connected to MCP server. Listing available tools...
                    INFO     Processing request of type ListToolsRequest                                                             server.py:619

Available tools: ['sentiment_analysis']

Analyzing sentiment for: 'i love  mcp'
                    INFO     Processing request of type CallToolRequest                                                              server.py:619
{'polarity': 0.5, 'subjectivity': 0.6, 'assessment': 'positive'}

Sentiment Analysis Result:
  Polarity: 0.5 (-1=negative, 1=positive)
  Subjectivity: 0.6 (0=objective, 1=subjective)
  Assessment: positive

Sentiment Analysis Result: (0.5, 0.6, 'positive')
((venv) ) Mac:jim mcp_testlab[513]$ python mcp-sentiment/mcp_client_stdio.py "i hate java"

Connected to MCP server at mcp-sentiment/app_fastmcp.py
Listing available tools...
[07/29/25 13:45:38] INFO     Processing request of type ListToolsRequest                                                             server.py:619

Connected to MCP server. Listing available tools...
                    INFO     Processing request of type ListToolsRequest                                                             server.py:619

Available tools: ['sentiment_analysis']

Analyzing sentiment for: 'i hate java'
                    INFO     Processing request of type CallToolRequest                                                              server.py:619
{'polarity': -0.8, 'subjectivity': 0.9, 'assessment': 'negative'}

Sentiment Analysis Result:
  Polarity: -0.8 (-1=negative, 1=positive)
  Subjectivity: 0.9 (0=objective, 1=subjective)
  Assessment: negative

Sentiment Analysis Result: (-0.8, 0.9, 'negative')

((venv) ) Mac:jim mcp_testlab[514]$ python mcp-sentiment/mcp_client_stdio.py "i really like python" -v

Connected to MCP server at mcp-sentiment/app_fastmcp.py
Listing available tools...
[07/29/25 13:46:35] INFO     Processing request of type ListToolsRequest                                                             server.py:619

Connected to MCP server. Listing available tools...
                    INFO     Processing request of type ListToolsRequest                                                             server.py:619

sentiment_analysis:
  Description: 
    Analyze the sentiment of the given text.

    Args:
        text (str): The text to analyze

    Returns:
        str: A JSON string containing polarity, subjectivity, and assessment
    
  Annotations: None
  Inputschema: {'properties': {'text': {'title': 'Text', 'type': 'string'}}, 'required': ['text'], 'title': 'sentiment_analysisArguments', 'type': 'object'}
  Meta: None
/Users/jim/Desktop/modelcontextprotocol/mcp_testlab/mcp-sentiment/mcp_client_stdio.py:154: PydanticDeprecatedSince211: Accessing the 'model_computed_fields' attribute on the instance is deprecated. Instead, you should access this attribute from the model class. Deprecated in Pydantic V2.11 to be removed in V3.0.
  value = getattr(tool, attr)
  Model_computed_fields: {}
  Model_config: {'extra': 'allow'}
  Model_extra: {}
/Users/jim/Desktop/modelcontextprotocol/mcp_testlab/mcp-sentiment/mcp_client_stdio.py:154: PydanticDeprecatedSince211: Accessing the 'model_fields' attribute on the instance is deprecated. Instead, you should access this attribute from the model class. Deprecated in Pydantic V2.11 to be removed in V3.0.
  value = getattr(tool, attr)
  Model_fields: {'name': FieldInfo(annotation=str, required=True), 'title': FieldInfo(annotation=Union[str, NoneType], required=False, default=None), 'description': FieldInfo(annotation=Union[str, NoneType], required=False, default=None), 'inputSchema': FieldInfo(annotation=dict[str, Any], required=True), 'outputSchema': FieldInfo(annotation=Union[dict[str, Any], NoneType], required=False, default=None), 'annotations': FieldInfo(annotation=Union[ToolAnnotations, NoneType], required=False, default=None), 'meta': FieldInfo(annotation=Union[dict[str, Any], NoneType], required=False, default=None, alias='_meta', alias_priority=2)}
  Model_fields_set: {'description', 'inputSchema', 'outputSchema', 'name'}
  Outputschema: {'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': 'sentiment_analysisOutput', 'type': 'object'}
  Title: None

Analyzing sentiment for: 'i really like python'
                    INFO     Processing request of type CallToolRequest                                                              server.py:619
{'polarity': 0.2, 'subjectivity': 0.2, 'assessment': 'positive'}

Sentiment Analysis Result:
  Polarity: 0.2 (-1=negative, 1=positive)
  Subjectivity: 0.2 (0=objective, 1=subjective)
  Assessment: positive

Sentiment Analysis Result: (0.2, 0.2, 'positive')
```

### Example Usage with `sse` Transport

**Command-line Arguments**
```bash
((venv) ) Mac:jim mcp_testlab[532]$ python mcp-sentiment/mcp_client_sse.py --help
usage: mcp_client_sse.py [-h] [--url URL] [--verbose] text_to_test

MCP SSE Client for Sentiment Analysis

positional arguments:
  text_to_test   Text to analyze for sentiment

options:
  -h, --help     show this help message and exit
  --url URL      URL of the SSE server endpoint (default: http://localhost:8000/sse)
  --verbose, -v  Display detailed information about available tools
```

**Client**
```bash
python mcp-sentiment/mcp_client_sse.py "i really like python" 
Connecting to MCP server at http://localhost:8000/sse...

Connected to MCP server. Listing available tools...

Available tools: ['sentiment_analysis']

Analyzing sentiment for: 'i really like python'

Sentiment Analysis Result:
  Polarity: 0.2 (-1=negative, 1=positive)
  Subjectivity: 0.2 (0=objective, 1=subjective)
  Assessment: positive
```

**SSE Server**
```bash
((venv) ) Mac:jim mcp_testlab[506]$ python mcp-sentiment/app_fastmcp.py --transport sse
INFO:     Started server process [8908]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:49538 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:49540 - "POST /messages/?session_id=fb1a89915f0b40e98f44385af5b6db58 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49540 - "POST /messages/?session_id=fb1a89915f0b40e98f44385af5b6db58 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49540 - "POST /messages/?session_id=fb1a89915f0b40e98f44385af5b6db58 HTTP/1.1" 202 Accepted
[07/29/25 06:13:08] INFO     Processing request of type ListToolsRequest                                                                                                                           server.py:619
INFO:     127.0.0.1:49540 - "POST /messages/?session_id=fb1a89915f0b40e98f44385af5b6db58 HTTP/1.1" 202 Accepted
                    INFO     Processing request of type CallToolRequest                                                                                                                            server.py:619
INFO:     127.0.0.1:49543 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:49545 - "POST /messages/?session_id=632a380ef69344eab4bf145158e05051 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49545 - "POST /messages/?session_id=632a380ef69344eab4bf145158e05051 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49545 - "POST /messages/?session_id=632a380ef69344eab4bf145158e05051 HTTP/1.1" 202 Accepted
[07/29/25 06:13:46] INFO     Processing request of type ListToolsRequest                                                                                                                           server.py:619
INFO:     127.0.0.1:49545 - "POST /messages/?session_id=632a380ef69344eab4bf145158e05051 HTTP/1.1" 202 Accepted
                    INFO     Processing request of type CallToolRequest                                                                                                                            server.py:619
INFO:     127.0.0.1:49547 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:49549 - "POST /messages/?session_id=f6a51e126c12412398bacc85753174a3 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49549 - "POST /messages/?session_id=f6a51e126c12412398bacc85753174a3 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49549 - "POST /messages/?session_id=f6a51e126c12412398bacc85753174a3 HTTP/1.1" 202 Accepted
[07/29/25 06:14:17] INFO     Processing request of type ListToolsRequest                                                                                                                           server.py:619
INFO:     127.0.0.1:49549 - "POST /messages/?session_id=f6a51e126c12412398bacc85753174a3 HTTP/1.1" 202 Accepted
                    INFO     Processing request of type CallToolRequest                                                                                                                            server.py:619
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [8908]
Terminated: 15             python mcp-sentiment/app_fastmcp.py --transport sse
```

### Example Usage with `streamable-http` Transport

**Command-line Arguments**
```bash
((venv) ) Mac:jim mcp_testlab[533]$ python mcp-sentiment/mcp_client_streamable.py --help
usage: mcp_client_streamable.py [-h] [--url URL] [--verbose] text_to_test

MCP Streamable Client for Sentiment Analysis

positional arguments:
  text_to_test   Text to analyze for sentiment

options:
  -h, --help     show this help message and exit
  --url URL      URL of the streamable-http server endpoint (default: http://localhost:8000/mcp)
  --verbose, -v  Display detailed information about available tools
```

**Client**
```bash
# Using the default URL
((venv) ) Mac:jim mcp_testlab[517]$ python mcp-sentiment/mcp_client_streamable.py "MCP is the best" 
Connecting to MCP server at http://localhost:8000/mcp...
Session ID: fdc3c721f04441a1ae4c22cadebc9226

Connected to MCP server. Listing available tools...

Available tools: ['sentiment_analysis']

Analyzing sentiment for: 'MCP is the best'

Sentiment Analysis Result:
  Polarity: 1.0 (-1=negative, 1=positive)
  Subjectivity: 0.3 (0=objective, 1=subjective)
  Assessment: positive
  
``` 

**Streamable-HTTP Server**
```bash
((venv) ) Mac:jim mcp_testlab[507]$ python mcp-sentiment/app_fastmcp.py --transport streamable-http
INFO:     Started server process [2701]
INFO:     Waiting for application startup.
[07/28/25 22:48:20] INFO     StreamableHTTP session manager started                                                                                                               streamable_http_manager.py:112
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:54049 - "POST /mcp HTTP/1.1" 307 Temporary Redirect
[07/28/25 22:48:29] INFO     Created new transport with session ID: 6a17c2206e6e478b830bd0da73771b8b                                                                              streamable_http_manager.py:229
INFO:     127.0.0.1:54049 - "POST /mcp/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54052 - "POST /mcp HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:54053 - "GET /mcp HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:54052 - "POST /mcp/ HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:54053 - "GET /mcp/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54055 - "POST /mcp HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:54055 - "POST /mcp/ HTTP/1.1" 200 OK
                    INFO     Processing request of type ListToolsRequest                                                                                                                           server.py:619
INFO:     127.0.0.1:54057 - "POST /mcp HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:54057 - "POST /mcp/ HTTP/1.1" 200 OK
                    INFO     Processing request of type CallToolRequest                                                                                                                            server.py:619
INFO:     127.0.0.1:54059 - "DELETE /mcp HTTP/1.1" 307 Temporary Redirect
                    INFO:     Terminating session: 6a17c2206e6e478b830bd0da73771b8b                                                                                                        streamable_http.py:633
INFO:     127.0.0.1:54059 - "DELETE /mcp/ HTTP/1.1" 200 OK
INFO:     Shutting down
INFO:     Waiting for application shutdown.
[07/28/25 22:48:42] INFO     StreamableHTTP session manager shutting down                                                                                                         streamable_http_manager.py:116
INFO:     Application shutdown complete.
INFO:     Finished server process [2701]
Terminated: 15             python mcp-sentiment/app_fastmcp.py --transport streamable-http
```

### Example Usage with multi-transport Client

**Command-line Arguments**
```bash
((venv) ) Mac:jim mcp_testlab[533]$ python mcp-sentiment/mcp_client_streamable.py --help
usage: mcp_client_streamable.py [-h] [--url URL] [--verbose] text_to_test((venv) ) Mac:jim mcp_testlab[504]$ python mcp-sentiment/mcp_client_mutli_transport.py --help
usage: mcp_client_mutli_transport.py [-h] [--endpoint ENDPOINT] [--verbose] text

MCP Client for sentiment analysis using specified transport

positional arguments:
  text                 Text to analyze for sentiment

options:
  -h, --help           show this help message and exit
  --endpoint ENDPOINT  Endpoint for the MCP server. Python module for stdio, sse (*/sse) or streamable-http (*/mcp) (default: mcp-
                       sentiment/app_fastmcp.py)
  --verbose, -v        Display detailed information about available tools
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

To run the MCP Inspector for server using `sse` or `streamable-http` transport, use the following command:

```bash
npx @modelcontextprotocol/inspector
```

### Connecting to the MCP Inspector
Open the browser to access the MCP Inspector interface, change from `http` to `https` if necessary.  Once the MCP Inspector is running, configure "Transport Type" for `sse` or `streamable-http` and set the server URL to point to your running MCP server (e.g., `http://localhost:8000/sse` or `http://localhost:8000/mcp`) and click "Connect" button.

**`sse` Server URL**: `http://localhost:8000/sse`
![](./images/mcp_inspector_connect_sse_server.png)

![](./images/mcp_inspector_sentiment_with_sse_server.png)


### Starting the `streamable-http` Server for testing
```bash
python mcp-sentiment/app_fastmcp.py --transport streamable-http
```

**`streamable-http` Server URL**: `http://localhost:8000/mcp`
![](./images/mcp_inspector_sentiment_with_streamable.png)




## Requirements

- Python 3.12+
- Dependencies: `pip install -r requirements.txt`
- Required NLP libraries for sentiment analysis
- Required version of `node` > v20.x to run MCP Inspector (see [GH Issue on unexpected token](https://github.com/modelcontextprotocol/python-sdk/issues/184#issuecomment-2788071291))


