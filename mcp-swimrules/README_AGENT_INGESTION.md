# Agent Rule Ingestion for MCP Swim Rules

This directory contains the enhanced rule ingestion pipeline for the MCP Swim Rules Agent, implementing section 4.4 of the product requirements document.

## Files

### `agent_rule_ingestion.py`
Enhanced rule ingestion pipeline that creates a vector database optimized for MCP agent RAG analysis with:

- **Rule Identifier Extraction**: Automatically extracts rule identifiers like `101.1`, `101.1.1`, `101.1.2A`, `101.1.2B`, `102.2.1`, etc.
- **Enhanced Metadata**: Each chunk includes categorization by stroke type, rule category, and section
- **Optimized Chunking**: Larger chunks (800 chars) with more overlap (150 chars) for better context
- **Multiple Document Sources**: Processes rulebook, glossary terms, interpretation guidance, and practical situations

### `test_agent_db.py`
Test script to verify the enhanced vector database functionality and metadata structure.

## Database Structure

The enhanced vector database (`agent_swimrules_db/`) contains document chunks with the following metadata:

| Field | Description | Example Values |
|-------|-------------|----------------|
| `rule_id` | Unique identifier | `rule_101.1`, `rule_101.1.2A`, `glossary`, `guidance` |
| `rule_number` | Official rule number | `101.1`, `101.1.2A`, `GLOSSARY`, `SITUATIONS` |
| `rule_title` | Rule or section title | `STARTS`, `Equipment`, `Glossary Terms` |
| `category` | Rule categorization | `Starts`, `Stroke Technique`, `Turns and Finishes` |
| `stroke_type` | Stroke classification | `breaststroke`, `butterfly`, `backstroke`, `freestyle`, `none` |
| `section` | Document section | `STARTS`, `BREASTSTROKE`, `Glossary` |
| `chunk_type` | Content type | `rule`, `glossary`, `guidance`, `situation` |
| `source` | Source document path | `./rule_data/2025-mini-rulebook.pdf` |
| `page` | Page number | `"13"`, `"27"`, `"0"` |

## Usage

### Create the Vector Database

```bash
cd /path/to/mcp-swimrules
python agent_rule_ingestion.py
```

This will:
1. Process the USA Swimming 2025 Mini Rulebook (pages 14-50)
2. Extract rule identifiers and metadata
3. Process glossary terms and interpretation guidance
4. Include practical situations from stroke and turn documents
5. Create vector embeddings using OpenAI's `text-embedding-3-small`
6. Store everything in the `agent_swimrules_db/` directory

### Test the Database

```bash
python test_agent_db.py
```

This will run test scenarios to verify:
- Rule identification accuracy
- Metadata filtering capabilities
- RAG query effectiveness
- Database completeness

## Features Implemented (Section 4.4 Requirements)

✅ **Rule Identifier Extraction**: Automatically extracts hierarchical rule numbers like:
- `101.1` (main rules)
- `101.1.1` (subsections) 
- `101.1.2A`, `101.1.2B` (sub-subsections with letters)
- `102.2.1`, `102.2.2`, `102.2.3` (other rule series)

✅ **Enhanced Metadata**: Each rule chunk includes:
- Rule category (Starts, Stroke Technique, Turns and Finishes, etc.)
- Stroke type classification (breaststroke, butterfly, backstroke, freestyle)
- Source document and page information
- Content type classification

✅ **Vector Database Creation**: 
- ChromaDB with persistent storage
- OpenAI embeddings for semantic similarity
- Optimized for RAG-based rule analysis
- Support for metadata filtering

✅ **Multi-Source Processing**:
- Main USA Swimming rulebook
- Glossary definitions
- Official interpretation guidance  
- Practical stroke and turn situations

## Integration with MCP Agent

The enhanced vector database is designed to support the MCP agent's `analyze_situation` tool with:

1. **Semantic Search**: Find relevant rules based on situation descriptions
2. **Metadata Filtering**: Target specific stroke types or rule categories
3. **Context Retrieval**: Get complete rule text with proper citations
4. **Confidence Scoring**: Leverage similarity scores for decision confidence

## Database Statistics

- **Total Chunks**: ~467 processed text chunks
- **Rule Coverage**: USA Swimming technical rules and regulations
- **Metadata Fields**: 9 structured metadata fields per chunk
- **Storage**: ChromaDB with SQLite persistence
- **Embeddings**: OpenAI text-embedding-3-small model

## Dependencies

- `langchain-chroma`: Vector database integration
- `langchain-openai`: OpenAI embeddings
- `langchain-community`: PDF document loading
- `load-dotenv`: Environment variable management
- `pypdf`: PDF processing capabilities

## Environment Setup

Ensure your `.env` file contains:
```
OPENAI_API_KEY=your_openai_api_key_here
```

The script will use OpenAI's embedding API to create vector representations of the rule text for semantic search capabilities.
