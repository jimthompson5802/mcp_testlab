# Copilot Instructions

These instructions help GitHub Copilot understand how to assist with the MCP Testlab project.

## Project Overview

This project demonstrates using the Model Context Protocol (MCP). It uses the FastMCP Python SDK to create tools that can be accessed via multiple transport protocols. The main focus is on a sentiment analysis tool that can analyze text and return sentiment scores.

- An MCP server [FastMCP Server](https://gofastmcp.com/python-sdk/fastmcp-server-server)
- An MCP client [FastMCP Client](https://gofastmcp.com/python-sdk/fastmcp-client-client)
- Multiple MCP clients using different transport protocols (stdio, SSE, streamable-http)
- Command-line interfaces to interact with the sentiment analysis tool


## Coding Style

When contributing to this project, follow these coding style guidelines:

1. **Python Style**: 
   - Follow PEP 8 conventions for Python code
   - Allow line length up to 120 characters
   - Use PascalCase for class names (e.g., `SentimentAnalyzer`)
   - Use snake_case for variables and functions (e.g., `analyze_text`, `sentiment_score`)

2. **Type Hints**: Include type annotations for function parameters and return values

3. **Documentation**: 
   - Add docstrings to all functions and classes
   - Use Google-style docstrings with Args and Returns sections

4. **Error Handling**: 
   - Use try/except blocks for error handling
   - Provide descriptive error messages

5. **Async Programming**:
   - Use asyncio for asynchronous operations
   - Employ async context managers with AsyncExitStack for resource cleanup

6. **Command-line Interfaces**:
   - Use argparse for processing command-line arguments
   - Provide helpful descriptions for all arguments

7. **Code Organization**:
   - Keep classes focused on a single responsibility
   - Use clear, descriptive variable and function names
   - Group related functionality within classes

8. **LLM Prompt**
   - when a prompt will span muliple lines use the triple quotes `"""` to enclose the prompt text.
   - use `textwrap.dedent` to remove any common leading whitespace.

## Common Patterns

1. **MCP Client Initialization**:
   - Create a client class
   - Initialize with an AsyncExitStack for resource management
   - Connect to server using appropriate transport function
   - Initialize ClientSession with transport

2. **MCP Server Implementation**:
   - Create FastMCP instance with descriptive name
   - Define tool functions with appropriate decorators
   - Include detailed docstrings for each tool function
   - Process command-line arguments to configure transport

3. **Error Handling and Resource Cleanup**:
   - Use try/finally blocks to ensure cleanup
   - Implement cleanup methods to close resources properly
   - Use async context managers for resource management

## Transport Types

The project supports three transport types:

1. **stdio**: Direct input/output communication between client and server
2. **SSE (Server-Sent Events)**: Web-based event streaming protocol 
3. **streamable-http**: HTTP-based transport with bidirectional streaming support

When implementing new features, ensure they work with all transport types.

## Testing

tests located in directory `tests/`. Follow these guidelines for writing tests:

1. **Unit Tests**: 
   - Write unit tests for all functions and classes
   - Use pytest for testing framework
   - Include tests for both positive and negative cases
   - Mock external dependencies where necessary

2. **Integration Tests**: 
   - When adding new functionality:
   - Test with all three transport types
   - Test with positive and negative sentiment examples
   - Verify proper resource cleanup and error handling