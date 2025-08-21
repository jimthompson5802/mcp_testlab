# MCP Situation Analysis

This module implements **Section 4.2.1 Situation Analysis** from the product requirements document for the Swim Rules Agent.

## Overview

The `mcp_situation_analysis.py` module provides an MCP (Model Context Protocol) tool that analyzes swimming scenarios to determine if they result in disqualification or are allowed. It uses:

- **RAG (Retrieval-Augmented Generation)** with ChromaDB for rule retrieval
- **OpenAI GPT-4o** for analysis and decision making
- **FastMCP** for MCP server functionality

## Features

- **analyze_situation** MCP tool that:
  - Takes natural language descriptions of swimming scenarios
  - Uses semantic search to retrieve relevant rules from ChromaDB
  - Analyzes scenarios with OpenAI's GPT-4o model
  - Returns structured decisions with rationale and rule citations

## Files

- `mcp_situation_analysis.py` - Main implementation module
- `test_mcp_situation_analysis.py` - Comprehensive test suite
- `demo_mcp_situation_analysis.py` - Simple demonstration script

## Requirements

### Environment Variables

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Dependencies

The module requires the following Python packages (see requirements.txt):
- `fastmcp` - MCP server framework
- `chromadb` - Vector database for rule storage
- `openai` - OpenAI API client
- `langchain-openai` - OpenAI embeddings
- `python-dotenv` - Environment variable loading

### Database Setup

The module expects a ChromaDB database at `./agent_swimrules_db` with a collection named `swim_rules` containing swimming rules. You can populate this using the `agent_rule_ingestion.py` module.

## Usage

### As MCP Server

Run the module as an MCP server with stdio transport:

```bash
python3 mcp_situation_analysis.py
```

### As Python Module

```python
import asyncio
from mcp_situation_analysis import SwimRulesRAGAnalyzer

async def main():
    # Initialize analyzer
    analyzer = SwimRulesRAGAnalyzer()
    await analyzer.initialize()
    
    # Analyze a scenario
    scenario = "Swimmer did not touch wall with both hands during breaststroke turn"
    result = await analyzer.analyze_situation(scenario)
    
    print(f"Decision: {result['decision']}")
    print(f"Rationale: {result['rationale']}")
    print(f"Citations: {result['rule_citations']}")

asyncio.run(main())
```

### Demo Script

Run the demonstration script:

```bash
python3 demo_mcp_situation_analysis.py
```

## Testing

Run the comprehensive test suite:

```bash
python3 test_mcp_situation_analysis.py
```

The test suite includes:
- Analyzer initialization tests
- Basic scenario analysis validation
- Multiple scenario testing
- Empty/invalid input handling
- RAG retrieval functionality
- Response format compliance checks

## API Response Format

The `analyze_situation` tool returns a dictionary with:

```python
{
    "decision": "ALLOWED" | "DISQUALIFICATION",
    "rationale": "Detailed explanation of the decision",
    "rule_citations": ["rule_id_1", "rule_id_2", ...]
}
```

## Implementation Details

### RAG Pipeline

1. **Query Processing**: Convert scenario to embedding using OpenAI embeddings
2. **Rule Retrieval**: Search ChromaDB for semantically similar rules
3. **Context Preparation**: Format retrieved rules for LLM consumption
4. **Analysis**: Use GPT-4o with rule context to make decisions
5. **Response Formatting**: Structure output per requirements

### Error Handling

The module includes comprehensive error handling:
- Database connection failures
- OpenAI API errors
- Invalid input scenarios
- Malformed responses

### Performance Considerations

- Async/await patterns for non-blocking operations
- Connection pooling for database operations
- Embedding caching for frequently used queries
- Response time optimization (< 2 seconds target)

## Configuration

The module can be configured by modifying class initialization parameters:

```python
analyzer = SwimRulesRAGAnalyzer(
    chroma_db_path="./custom_db_path",
    collection_name="custom_collection",
    openai_model="gpt-4o"
)
```

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not set"**
   - Ensure your OpenAI API key is properly configured
   - Check that the environment variable is exported

2. **"ChromaDB collection not found"**
   - Run the rule ingestion pipeline first
   - Verify the database path is correct

3. **"No relevant rules found"**
   - Database may be empty or not properly indexed
   - Check the collection contains swimming rules

### Debug Mode

Enable verbose logging by setting environment variable:
```bash
export MCP_DEBUG=1
```

## Contributing

When modifying the module:
1. Run the test suite to ensure functionality
2. Update tests for new features
3. Follow PEP 8 style guidelines
4. Add docstrings for new functions

## License

This module is part of the Swim Rules Agent project and follows the same licensing terms.
