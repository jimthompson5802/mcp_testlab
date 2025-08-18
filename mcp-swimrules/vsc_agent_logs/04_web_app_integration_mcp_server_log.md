jimthompson5802: refactor app_server.py to integrate with mcp_situation_analysis.py as described in PRD section 4.2 and 4.3.

GitHub Copilot: I'll help you refactor `app_server.py` to integrate with `mcp_situation_analysis.py` according to the PRD sections 4.2 and 4.3. Let me first examine the relevant files to understand the current implementation and requirements. Let me continue reading the PRD to understand the complete requirements: Now let me examine the current `app_server.py` and `mcp_situation_analysis.py` files to understand the current implementation: Now let me examine the `mcp_situation_analysis.py` file: Now let me check if there are any existing templates or static files: Now let me examine the existing template to understand the current UI structure: Now I need to refactor the app_server.py to integrate with the MCP situation analysis module. Based on the PRD requirements and the existing code, I need to:

1. Replace the mock analysis with actual MCP client integration
2. Set up MCP client connection to the situation analysis server
3. Update the response format to match the MCP tool output
4. Handle the stdio transport connection properly

Let me start by refactoring the app_server.py: 
```


Made changes.


```
Now let me add the MCP client integration class: 
```


Made changes.


```
Now let me update the startup and shutdown events to use the MCP client: 
```


Made changes.


```
Now let me update the analyze_scenario endpoint to use the MCP client instead of the mock function: 
```


Made changes.


```
Now I need to remove the old mock analysis function since we're replacing it with the MCP integration: 
```


Made changes.


```
Now I need to clean up the unused imports and fix the type annotations. Let me check the current status of the file: Let me fix these issues: 
```


Made changes.


```
Let me fix the type annotation issues and the f-string: 
```


Made changes.


```
Let me fix the type annotation properly: 
```


Made changes.


```

```


Made changes.


```

```


Made changes.


```
Now let me fix the issue with the stdin/stdout being None by adding proper type checks: 

Continue to iterate?
[object Object]

jimthompson5802: @agent Continue: "Continue to iterate?"

GitHub Copilot: 
```


Made changes.


```
Let me also fix the trailing whitespace issue: 
```


Made changes.


```
Now let's check if all errors are resolved: Great! Now let me create a simple test script to verify that the integration works properly. First, let me check if there are any requirements we need to install: Now let me check if we can run a basic test. But first, let me see if the MCP situation analysis module has been properly set up: Good, it looks like the ChromaDB database exists. Let me create a test script to verify the integration: 

Made changes.

Let me fix the import issue: 
```


Made changes.


```
Let me fix these import issues: 
```


Made changes.


```
Now let me also create a comprehensive implementation summary documenting the changes made: 

Made changes.

Now let me run a quick test to see if our integration works. First, let me check if the Python environment is properly configured: Let me run a simple syntax check on our refactored app_server.py: Great! The file compiles without errors. Now let me test if we can import the necessary modules: Excellent! Now let me run the integration test to verify everything works: I can see that the MCP client is starting successfully but there's an issue with the JSON-RPC request format. The MCP server is returning "Invalid request parameters". Let me fix this by adjusting the request format. Let me check the actual MCP server to understand the expected format: The MCP server is starting but I can see it's using FastMCP 2.0. Let me look at the actual MCP request/response protocol used by FastMCP. Let me examine the mcp_situation_analysis.py more carefully to understand the tool registration: Let me check if there are any demos showing how to call FastMCP tools properly: Let me check if there are other client examples in the project: Let me check the stdio client example to understand the proper request format: Perfect! I can see that the proper way to use FastMCP is through the `Client` class with `StdioTransport`. Let me refactor the MCP client to use the proper FastMCP client library instead of direct subprocess communication: 
```


Made changes.


```
Now let me completely refactor the MCP client class to use the proper FastMCP client: 
```


Made changes.


```
Let me fix the json import issue: 
```


Made changes.


```
Let me fix the json import issue: 
```


Made changes.


```
Great! Now let's test our updated integration: Good! Let's run the integration test again with the proper FastMCP client: Great! The MCP client is now connecting successfully (we can see the FastMCP banner), but we're getting "Unable to parse MCP response" which suggests the response format is different than expected. Let me create a simple debug script to see what the actual response format looks like: 

Made changes.

Perfect! Now I can see the actual response format. The FastMCP client returns a `CallToolResult` object with a `data` attribute that contains the dictionary we need. Let me update the MCP client to handle this properly: 
```


Made changes.


```
Let me fix the type checking for the content: 
```


Made changes.


```
Now let's test our updated integration: Excellent! 🎉 The integration is now working perfectly! Let me run one final test to make sure the FastAPI server can start properly with the MCP integration: Perfect! 🎉 The server starts successfully and the MCP integration is working flawlessly. 

## Summary

I have successfully refactored app_server.py to integrate with mcp_situation_analysis.py as specified in PRD sections 4.2 and 4.3. Here's what was accomplished:

### ✅ **Key Integration Achievements:**

1. **MCP Client Implementation**: 
   - Created `MCPSituationAnalysisClient` class using proper FastMCP client library
   - Implements stdio transport as required by PRD section 4.2.1
   - Handles proper connection lifecycle with startup/shutdown events

2. **Real AI-Powered Analysis**: 
   - Replaced mock keyword-based analysis with actual RAG-powered analysis
   - Integrates with ChromaDB vector database for rule retrieval
   - Uses OpenAI GPT-4o for sophisticated rule interpretation

3. **API Compatibility Maintained**:
   - `/api/analyze` endpoint maintains the same interface
   - Response format converted from MCP format to API format
   - Enhanced error handling for MCP service unavailability

4. **Working Integration**: 
   - Successfully tested with real scenarios from the test results:
     - ✅ "Breaststroke Two-Hand Touch Violation" → DISQUALIFICATION (with rule 101.2.4)
     - ✅ "Valid Backstroke Turn" → ALLOWED 
     - ✅ "False Start" → DISQUALIFICATION

### 🔧 **Technical Implementation:**

- **Transport**: stdio (as specified in PRD)
- **Protocol**: Proper FastMCP client with `StdioTransport`  
- **Response Parsing**: Handles `CallToolResult.data` format correctly
- **Error Recovery**: Graceful degradation when MCP service unavailable
- **Resource Management**: Proper cleanup in shutdown events

### 📋 **PRD Compliance:**

**Section 4.2.1 - Situation Analysis**: ✅ Complete
- ✅ Transport: stdio implementation
- ✅ Input: Natural language scenario description  
- ✅ RAG Integration: Via MCP tool using ChromaDB
- ✅ LLM: OpenAI GPT-4o via MCP tool
- ✅ Output: decision, rationale, rule_citations

**Section 4.3 - Web Interface Integration**: ✅ Complete  
- ✅ API endpoint maintains compatibility
- ✅ Input validation (2000 character limit)
- ✅ Enhanced error handling
- ✅ Response format preserved

The integration transforms the application from a simple keyword-based mock system into a sophisticated AI-powered rule analysis system while maintaining full API compatibility and user interface functionality. The system now provides real USA Swimming rule analysis using the complete rule database and advanced natural language processing.