# Rule Lookup Utility

## Overview

The Rule Lookup Utility implements Section 4.5.1 of the Product Requirements Document. It provides a debugging and exploration tool for the ChromaDB vector database containing USA Swimming rules and regulations.

## Features

- **Interactive Query Interface**: Prompts users for natural language queries
- **Semantic Search**: Uses ChromaDB vector similarity search to find relevant rules
- **Rich Metadata Display**: Shows rule ID, title, category, stroke, and similarity scores
- **Configurable Results**: Allows users to specify number of results (1-10)
- **Error Handling**: Graceful handling of missing database or API key issues

## Requirements

### Environment Setup

1. **OpenAI API Key**: Required for generating query embeddings
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
   Or create a `.env` file in the project directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. **ChromaDB Database**: The utility expects a populated ChromaDB database at `./agent_swimrules_db` with collection name `langchain` (created by the rule ingestion process)

### Dependencies

All required dependencies are included in the main `requirements.txt`:
- `chromadb`: Vector database for rule storage and search
- `langchain-openai`: OpenAI embeddings for semantic search
- `load_dotenv`: Environment variable management (optional)

## Usage

### Interactive Mode

Run the utility in interactive mode to perform multiple queries:

```bash
cd mcp-swimrules
python rule_lookup_utility.py
```

Example session:
```
🏊‍♀️ SWIM RULES LOOKUP UTILITY 🏊‍♂️
=====================================

🔍 Enter your rule query: breaststroke turn requirements
📊 Number of results (1-10, default=5): 3

🔍 Generating embeddings for query: 'breaststroke turn requirements'
🔍 Searching ChromaDB for 3 most relevant rules...

================================================================================
🔍 RULE LOOKUP RESULTS FOR: 'breaststroke turn requirements'
================================================================================

📖 RESULT #1
🏷️  Rule ID: 101.2.4
📝 Title: Breaststroke Turns and Finish
🏊 Stroke: Breaststroke
📂 Category: Technique
🎯 Similarity: 0.892
------------------------------------------------------------
📄 Content:
   At each turn and at the finish of the race, the touch shall be
   made with both hands separated and simultaneously at, above, or
   below the water level...
------------------------------------------------------------
```

### Testing

Run the test suite to verify functionality:

```bash
python test_rule_lookup_utility.py
```

## Implementation Details

### Architecture

The utility follows the same patterns as the main situation analysis module:

1. **Initialization**: 
   - Connects to ChromaDB persistent client
   - Initializes OpenAI embeddings model (`text-embedding-3-small`)
   - Validates database collection exists

2. **Query Processing**:
   - Generates embeddings for user queries using OpenAI
   - Performs vector similarity search in ChromaDB
   - Converts distances to similarity scores (1.0 - distance)

3. **Result Display**:
   - Formats results with metadata and content
   - Shows similarity scores for relevance assessment
   - Provides readable text wrapping for rule content

### Code Structure

```python
class RuleLookupUtility:
    def __init__(self, chroma_db_path, collection_name)
    async def initialize()                          # Setup ChromaDB and embeddings
    async def lookup_rules(query, n_results)       # Core search functionality  
    def display_results(query, results)            # Format and display results
    async def run_interactive_session()            # Interactive user interface
```

### Error Handling

The utility includes comprehensive error handling for common issues:

- **Missing API Key**: Clear error message with setup instructions
- **Database Not Found**: Informative message about running rule ingestion
- **Empty Database**: Warning about no available rules
- **Network Issues**: Graceful handling of embedding generation failures

## Integration with Main System

The Rule Lookup Utility shares the same ChromaDB database and configuration as the main MCP situation analysis tool:

- **Database Path**: `./agent_swimrules_db`
- **Collection Name**: `langchain` (created by ingestion process)
- **Embedding Model**: `text-embedding-3-small` (same as main system)
- **Metadata Schema**: Compatible with situation analysis requirements

## Query Examples

Good query examples for testing:

- **Stroke-Specific**: "breaststroke turn requirements", "butterfly stroke technique"
- **Rule Categories**: "false start rules", "disqualification procedures"
- **Event-Specific**: "relay exchange zone", "backstroke start position"  
- **Equipment**: "starting blocks", "timing systems"
- **Official Procedures**: "referee responsibilities", "protest procedures"

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY environment variable is required"**
   - Set the API key in your environment or `.env` file
   - Verify the key is valid and has sufficient credits

2. **"Collection 'swim_rules' not found"**
   - Run the rule ingestion process to populate the database
   - Check that `./agent_swimrules_db` directory exists

3. **"Collection contains 0 rule documents"**
   - The database exists but is empty
   - Run rule ingestion with proper PDF source files

4. **No results for queries**
   - Try broader or different keywords
   - Check that the database is properly populated
   - Verify embedding model is working correctly

### Debug Mode

The test utility provides detailed initialization information:

```bash
python test_rule_lookup_utility.py
```

This will show:
- Import success/failure
- Database connection status  
- Collection document count
- Sample query execution

## Future Enhancements

Potential improvements for the utility:

1. **Export Functionality**: Save search results to files
2. **Advanced Filtering**: Filter by stroke, category, or rule type
3. **Query History**: Remember and reuse previous queries
4. **Batch Processing**: Process multiple queries from a file
5. **Relevance Tuning**: Adjust similarity thresholds and ranking
