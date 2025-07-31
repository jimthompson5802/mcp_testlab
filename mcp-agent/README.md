# MCP Agent

This directory contains implementations of Model Context Protocol (MCP) agents. These agents serve as intermediaries that connect clients to MCP-powered tools and services.

## Overview

MCP Agent facilitates communication between clients and sentiment analysis tools using the Model Context Protocol. It supports multiple transport protocols allowing flexible deployment in various environments.

## Module Summary

- **agent_client.py**  
  Implements a client for communicating with MCP agents.  
  This module provides classes and functions to:
  - Establish and manage connections to an MCP agent using supported transports (such as stdio)
  - Send requests and receive responses following the MCP message protocol
  - Handle session lifecycle, including initialization, message sequencing, and graceful shutdown
  - Abstract transport details so that higher-level code can interact with the agent in a uniform way
  - Provide error handling and reconnection logic to ensure robust client-agent communication
  - Support both synchronous and asynchronous usage patterns, enabling integration in various application types

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