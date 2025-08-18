# Swim Rule Analysis

## High-level Overview

The `app_server.py` and `mcp_situation_analysis.py` modules are integrated to provide a web-based interface for situation analysis using the MCP sentiment analysis tool:

- The FastAPI application in `app_server.py` exposes an endpoint that receives a situation description from the web UI.
- Upon receiving a request, `app_server.py` calls the `analyze_situation` function from `mcp_situation_analysis.py`.
- The `analyze_situation` function communicates with the MCP server using the FastMCP client, analyzes the provided text, and returns the sentiment analysis results.
- The results are then returned by the FastAPI endpoint to the web UI for display.

This integration allows users to interactively analyze situations through a web interface, leveraging the MCP sentiment analysis tool as the backend.

---

## Example Screenshots of the Web UI

### Initial screen
![Screenshot 1](./images/swim_web1.png)

### Enter the situation description
![Screenshot 2](./images/swim_web2.png)

### Analysis of the situation after clicking the "Analyze" button
![Screenshot 3](./images/swim_web3.png)


