# MCP Testbed

This project demonstrates sentiment analysis using the Model Context Protocol (MCP).

## Folder Structure

- `mcp-sentiment/app_fastmcp.py`: MCP server script for sentiment analysis.
- `mcp-sentiment/mcp_client_stdio.py`: MCP client that connects to the server and requests sentiment analysis via command line.

## Usage

To run sentiment analysis from the command line:

```bash
python mcp-sentiment/mcp_client_stdio.py "Your text to test sentiment"
```

If no text is provided, the program will exit with an error message.

## How It Works

The application uses Model Context Protocol (MCP) to facilitate communication between a client and a sentiment analysis server. When you run the client with a text string, it:

1. Connects to the server script (`app_fastmcp.py`)
2. Sends your text for sentiment analysis
3. Returns the sentiment result (positive, negative, or neutral)

## Requirements

- Python 3.8+
- MCP library (`pip install mcp`)
- Required NLP libraries for sentiment analysis

## Contributing

Feel free to submit issues or pull requests to improve this testbed!

