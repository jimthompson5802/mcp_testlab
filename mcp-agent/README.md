# MCP Agent

This directory contains implementations of Model Context Protocol (MCP) agents. These agents serve as intermediaries that connect clients to MCP-powered tools and services.

## Overview

MCP Agent facilitates communication between clients and sentiment analysis tools using the Model Context Protocol. It supports multiple transport protocols allowing flexible deployment in various environments.

## Module Summary

## Agent Client Module (agent_client.py)

This module implements an interactive AI agent that combines language model capabilities with specialized tools via the Model Context Protocol (MCP). It creates an intelligent assistant that can:

1. **Perform mathematical operations** using math tools
2. **Analyze sentiment in text** using sentiment analysis tools

### Key Components

- **Multi-server MCP Client**: Connects to two FastMCP servers (math and sentiment) using stdio transport
- **LangChain Integration**: Uses OpenAI's GPT-4o-mini model with tool binding
- **LangGraph Workflow**: Creates a directed graph for message processing with:
  - User input handling
  - LLM response generation
  - Tool execution
  - Response display

### Workflow

1. The agent initializes with a system message defining its capabilities
2. It dynamically loads available tools from MCP servers
3. When a user submits a query:
   - The LLM determines if tools are needed
   - If tools are required, it dispatches to the appropriate tool server
   - Results are formatted and presented to the user
4. The interaction loop continues until the user exits

### Technical Features

- **Asynchronous Design**: Uses `asyncio` for non-blocking operations
- **State Management**: Maintains conversation state through the graph workflow
- **Error Handling**: Gracefully handles exceptions and termination
- **Conditional Routing**: Directs flow based on message content and tool needs

The module provides a clean, interactive command-line interface for users to engage with the agent's capabilities while abstracting the complexity of the underlying tool connections.


- **math_tools.py**  
  Defines mathematical tool functions that can be registered with an MCP agent.  
  This module provides:
  - Implementations of basic mathematical operations (such as addition and multiplication)
  - Functions decorated for MCP tool registration, making them discoverable and callable via the MCP protocol
  - Input validation and error handling for mathematical operations
  - Docstrings describing each tool's purpose, input parameters, and return values, following Google-style documentation
  - Example usage patterns for integrating math tools into an MCP agent session

- **sentiment_tools.py**  
  Implements sentiment analysis tools for use with MCP agents.  
  This module provides:
  - Functions that analyze input text and return sentiment scores or labels (e.g., positive, negative, neutral)
  - Tool functions decorated for MCP registration, making them accessible to clients via the MCP protocol
  - Input validation to ensure text data is suitable for analysis
  - Error handling for invalid or unexpected input
  - Google-style docstrings for each tool, documenting arguments, return values, and example usage
  - Example integration patterns for registering sentiment tools with an MCP agent session


## Example Usage


### Starting the MCP Agent

To use the MCP Agent client, 
```bash
python mcp-agent/agent_client.py
((venv) ) Mac:jim mcp_testlab[514]$ python mcp-agent/agent_client.py 
[07/31/25 17:40:35] INFO     Starting MCP server 'MathTools' with transport 'stdio'                   server.py:1371
[07/31/25 17:40:35] INFO     Starting MCP server 'SentimentTools' with transport 'stdio'              server.py:1371

Welcome to the MCP Agent! Ask me questions and I'll use tools to help answer them.
Type an empty message to exit.

Enter your question (or press Enter to exit): 
```

### Available Tools

```bash
Enter your question (or press Enter to exit): what tools are available

Processing: 'what tools are available'

Response: I have access to two sets of tools:

1. Math tools: I can perform addition and multiplication of numbers.
2. Sentiment tools: I can analyze the sentiment of text to determine if it is positive, negative, or neutral.

Let me know if you need help with any mathematical operations or sentiment analysis!
```

### Tool Details
```bash
Enter your question (or press Enter to exit): list details about each tool

Processing: 'list details about each tool'

Response: Here are the details about each tool available:

### Math Tools
1. **Add**
   - **Function**: Adds two integers.
   - **Arguments**: 
     - `a`: The first integer to add.
     - `b`: The second integer to add.
   - **Returns**: The sum of `a` and `b`.

2. **Multiply**
   - **Function**: Multiplies two integers.
   - **Arguments**: 
     - `a`: The first integer to multiply.
     - `b`: The second integer to multiply.
   - **Returns**: The product of `a` and `b`.

### Sentiment Tools
1. **Analyze Sentiment**
   - **Function**: Analyzes the sentiment of provided text.
   - **Arguments**: 
     - `text`: The input text string to analyze for sentiment.
   - **Returns**: A dictionary containing:
     - `polarity`: Float between -1.0 (negative) and 1.0 (positive).
     - `subjectivity`: Float between 0.0 (objective) and 1.0 (subjective).
     - `assessment`: String classification ("positive", "negative", or "neutral").

If you would like to use any of these tools, just let me know how I can assist you!
```

### Using Math Tools

```bash
Enter your question (or press Enter to exit): what is 3 plus 4

Processing: 'what is 3 plus 4'
[07/31/25 17:44:43] INFO     Starting MCP server 'MathTools' with transport 'stdio'                   server.py:1371

Response: 3 plus 4 equals 7.

Enter your question (or press Enter to exit): what is 3 times 4

Processing: 'what is 3 times 4'
[07/31/25 17:44:54] INFO     Starting MCP server 'MathTools' with transport 'stdio'                   server.py:1371

Response: 3 times 4 equals 12.

Enter your question (or press Enter to exit): what is 8 divided by 4

Processing: 'what is 8 divided by 4'

Response: I cannot perform division operations. Please let me know if you need help with addition, multiplication, or sentiment analysis!
```
### Using Sentiment Tools
```bash
Enter your question (or press Enter to exit): I love MCP

Processing: 'I love MCP'
[07/31/25 17:45:52] INFO     Starting MCP server 'SentimentTools' with transport 'stdio'              server.py:1371

Response: The sentiment analysis of the text "I love MCP" is as follows:
- Polarity: 0.5 (positive)
- Subjectivity: 0.6 (subjective)
- Assessment: positive

Enter your question (or press Enter to exit): Learning Python is fun                  

Processing: 'Learning Python is fun'
[07/31/25 17:46:27] INFO     Starting MCP server 'SentimentTools' with transport 'stdio'              server.py:1371

Response: The sentiment analysis of the text "Learning Python is fun" is as follows:
- Polarity: 0.3 (positive)
- Subjectivity: 0.2 (objective)
- Assessment: positive

Enter your question (or press Enter to exit): Learning JAVA is very hard and difficult

Processing: 'Learning JAVA is very hard and difficult'
[07/31/25 17:46:40] INFO     Starting MCP server 'SentimentTools' with transport 'stdio'              server.py:1371

Response: The sentiment analysis of the text "Learning JAVA is very hard and difficult" is as follows:
- Polarity: -0.44 (negative)
- Subjectivity: 0.85 (subjective)
- Assessment: negative
```

### Question not Supported by Tools
```bash
Enter your question (or press Enter to exit): what is the capital of hawaii

Processing: 'what is the capital of hawaii'

Response: I cannot provide information on geographical locations or facts. However, if you have any mathematical operations or need sentiment analysis, feel free to ask!
```

## Module Relationship Diagram

```
            +-------------------+
            |   agent_client.py |
            +-------------------+
                /           \
               v             v
+-------------------+      +----------------------+
|   math_tools.py   |      |  sentiment_tools.py  |
+-------------------+      +----------------------+
```

## LangGraph Workflow in agent_client.py

```
+---------------------+
|   Start Session     |
+---------------------+
           |
           v
+---------------------+
|   Receive Input     |<-------+
+---------------------+        |
           |                   |
           v                   |
+---------------------+        |
|   Select Tool       |        |
| (math/sentiment)    |        |
+---------------------+        |
           |                   |
           v                   |
+---------------------+        |
|   Invoke Tool Node  |        |
+---------------------+        |
           |                   |
           v                   |
+---------------------+        |
|   Collect Result    |        |
+---------------------+        |
           |                   |
           v                   |
+---------------------+        |
|   Send Response     |        |
+---------------------+        |
           |                   |
           v                   |
+---------------------+        |
|  More Input?        |--Yes---+
+---------------------+
              |
              No
              v
+---------------------+ 
|   End Session       |
+---------------------+
```
