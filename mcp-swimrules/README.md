# Swim Rule Analysis

## Product Requirements Document
This example is based on a **Products Requirement Document** (PDR) for the SWIM Rules web application.  The PDR was used by Visual Studio Code Agent Mode to create and refactor the following modules.
* `app_server.py`:  FastAPI Web application server
* `mcp_situation_analysis.py`:  MCP Server performing RAG to retrieve relevant USA Swimming rules and interfacing with OpenAI LLM to render an analysis of the submitted situation.

In addition to the above modules, Visual Studio Code Agent Mode also created test utilities and implementation summary files.

The LLM used by Visual Studio Code Agent Mode was **Claude Sonnet 4**.  The Visual Studio Code Agent logs can be found in this [directory](./vsc_agent_logs). These logs summarize the chat converation with the agent in creating and refactoring the code. 


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


