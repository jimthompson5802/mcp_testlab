# Product Requirements Document: Swim Rules Agent

## 1. Executive Summary

### 1.1 Project Overview
The Swim Rules Agent is a web-based application that provides officials with quick access to USA Swimming rules, violation checking, and meet regulation validation. The system leverages the Model Context Protocol (MCP) to access swim rule databases and provide intelligent rule analysis for training and educational purposes.

### 1.2 Business Objectives
- Provide instant access to USA Swimming rules and regulations
- Reduce rule interpretation errors during training sessions
- Support officials' education and certification processes
- Enable complex scenario analysis for rule application

### 1.3 Success Metrics
- Query response time < 2 seconds for simple rule lookups
- 95% accuracy in rule citation and interpretation
- Support for 100+ concurrent users during training sessions
- Zero downtime for rule updates

## 2. Product Scope

### 2.1 In Scope
- Web-based user interface for rule queries
- MCP integration for accessing USA Swimming rule databases
- Rule lookup functionality with citation references
- Swimming violation checking and validation
- Meet regulation compliance verification
- Complex scenario analysis involving multiple rules
- Rule update management system
- Local deployment with cloud migration readiness

### 2.2 Out of Scope
- Mobile-specific applications
- Real-time meet officiating integration
- User authentication system (Phase 1)
- Multi-organization rule support (Phase 1)
- Automated rule enforcement during live meets

## 3. Target Users

### 3.1 Primary Users
- **Swimming Officials**: Referees, starters, stroke & turn judges
- **Official Trainers**: Instructors conducting certification programs
- **Meet Directors**: Personnel managing swimming competitions

### 3.2 User Personas
- **Experienced Official**: Needs quick rule clarification and complex scenario analysis
- **Training Official**: Requires detailed explanations and educational context
- **Meet Director**: Needs regulation validation and compliance checking

## 4. Functional Requirements

### 4.1 Core Features

#### 4.1.1 Rule Lookup System
- **Requirement**: Users can search for specific USA Swimming rules
- **Acceptance Criteria**:
  - Full-text search across rule database
  - Search by rule number, keyword, or category
  - Return rule citation with complete text
  - Display related rules and cross-references
  - Search response time < 2 seconds

#### 4.1.2 Violation Checking
- **Requirement**: Analyze described swimming scenarios for rule violations
- **Acceptance Criteria**:
  - Accept natural language scenario descriptions
  - Identify applicable rules and potential violations
  - Provide detailed explanation of violations
  - Suggest corrective actions or penalties
  - Handle multiple violation scenarios

#### 4.1.3 Meet Regulation Validation
- **Requirement**: Validate meet procedures against USA Swimming regulations
- **Acceptance Criteria**:
  - Check meet format compliance
  - Validate timing and scoring procedures
  - Verify equipment and facility requirements
  - Provide compliance checklists
  - Generate regulation summary reports

#### 4.1.4 Complex Scenario Analysis
- **Requirement**: Analyze multi-faceted situations involving multiple rules using RAG-enhanced interpretation
- **Acceptance Criteria**:
  - Process scenarios with multiple rule interactions using vector similarity search
  - Prioritize rule applications based on semantic relevance
  - Identify conflicting regulations through context-aware analysis
  - Provide step-by-step analysis with supporting rule citations
  - Support "what-if" scenario modeling with historical precedent lookup
  - Generate natural language explanations augmented by retrieved rule context

### 4.2 MCP Integration Features

#### 4.2.1 Rule Database Access
- **MCP Tools Required**:
  - `search_rules`: Full-text and semantic rule search functionality
  - `get_rule_by_number`: Retrieve specific rule by reference number
  - `get_related_rules`: Find related and cross-referenced rules using vector similarity
  - `validate_scenario`: Analyze scenarios for rule compliance with RAG-enhanced interpretation
  - `semantic_search`: Vector-based semantic search across rule embeddings
  - `get_rule_context`: Retrieve contextual information and historical interpretations

#### 4.2.2 Data Management Tools
- **MCP Tools Required**:
  - `update_rules`: Handle USA Swimming rule updates and re-generate embeddings
  - `sync_database`: Synchronize with official rule sources
  - `validate_database`: Ensure data integrity
  - `get_rule_history`: Track rule changes and versions
  - `update_embeddings`: Refresh vector embeddings for rule database
  - `index_scenarios`: Index analyzed scenarios for future retrieval

#### 4.2.3 RAG Enhancement Tools
- **MCP Tools Required**:
  - `generate_embeddings`: Create vector embeddings for rules and scenarios
  - `similarity_search`: Find semantically similar rules and precedents
  - `context_retrieval`: Retrieve relevant context for rule interpretation
  - `augment_response`: Enhance responses with retrieved contextual information

### 4.3 User Interface Requirements

#### 4.3.1 Query Interface
- Clean, intuitive search interface with semantic search capabilities
- Support for natural language queries with intent recognition
- Advanced search filters (category, rule type, date, similarity threshold)
- Query history and saved searches with semantic clustering
- Export functionality for results including retrieved context
- Visual similarity indicators for related rules and scenarios

#### 4.3.2 Web Interface Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Swim Rules Agent                                    │
│                    Official Scenario Analysis                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Scenario Input:                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Enter swimming scenario description...                              │    │
│  │                                                                     │    │
│  │ Example: "Swimmer did not touch the wall with both hands            │    │
│  │ simultaneously during breaststroke turn"                            │    │
│  │                                                                     │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   [Analyze]     │  │ [Clear Input]   │  │ [Load Example]  │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                            ANALYSIS RESULTS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Decision:                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🚫 DISQUALIFICATION                                                 │   │
│  │     Confidence: 95%                                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             |
│  Rationale:                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ The described scenario constitutes a violation of breaststroke      │    │
│  │ technique requirements. USA Swimming rules mandate that swimmers    │    │
│  │ must touch the wall with both hands simultaneously during turns     │    │
│  │ and finishes in breaststroke events. Failure to do so results in    │    │
│  │ immediate disqualification as it provides an unfair competitive     │    │
│  │ advantage and violates stroke technique standards.                  │    │
│  │                                                                     │    │
│  │ The violation is clear and unambiguous, requiring no official       │    │
│  │ discretion in application.                                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  Rule Citations:                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Primary Rules:                                                      │    │
│  │ • 101.2.2 - Breaststroke Turn Requirements                          │    │
│  │ • 101.2.3 - Breaststroke Finish Requirements                        │    │
│  │                                                                     │    │
│  │ Supporting Rules:                                                   │    │
│  │ • 102.5.1 - Disqualification Procedures                             │    │
│  │ • 103.1.4 - Stroke Technique Violations                             │    │
│  │                                                                     │    │
│  │ Related Interpretations:                                            │    │
│  │ • Official Interpretation 2023-BR-15: Simultaneous Touch Definition │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │ [Export Report] │  │ [Save Scenario] │  │ [Print Results] │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                             │
└───────────────────────────────────────────────────────────────────────────-─┘
```

#### 4.3.3 Interface Component Specifications

**Scenario Input Area:**
- Multi-line text area (minimum 4 rows, expandable)
- Character limit: 2000 characters with live counter
- Placeholder text with example scenarios
- Auto-save draft functionality
- Input validation for minimum meaningful content

**Decision Display:**
- Large, prominently displayed result banner
- Color-coded status indicators:
  - 🟢 GREEN: "ALLOWED" / "NO VIOLATION"
  - 🔴 RED: "DISQUALIFICATION" / "VIOLATION"
- Confidence percentage display (RAG-generated confidence score)
- Visual icons for quick recognition

**Rationale Text Box:**
- Read-only formatted text area
- Supports rich text formatting for emphasis
- Expandable/collapsible for long explanations
- Word wrap enabled
- Copy-to-clipboard functionality

**Rule Citations Box:**
- Structured list format with hierarchical display
- Clickable rule numbers for detailed rule text
- Categorized citations (Primary, Supporting, Related)
- Link to official USA Swimming rule database
- Export citations in standard format

#### 4.3.4 Response Display
- Clear rule citation format with confidence scores
- Complete rule text with semantic highlighting
- Visual indicators for violation severity and rule relevance
- Structured analysis for complex scenarios with supporting evidence
- Print-friendly formatting with embedded context
- Source attribution for retrieved contextual information

### 4.4 Rule Update Management
- **Requirement**: Automatically handle USA Swimming rule updates with RAG pipeline refresh using async operations
- **Acceptance Criteria**:
  - Detect new rule publications and trigger embedding updates asynchronously
  - Update database without service interruption using background tasks
  - Maintain rule version history with embedding versioning via async workers
  - Notify users of significant changes affecting semantic relationships through async notifications
  - Validate update integrity including embedding quality using async validation pipelines
  - Re-index historical scenarios against updated rule base with async batch processing

## 5. Technical Requirements

### 5.1 Architecture
- **Web Framework**: FastAPI for high-performance async API endpoints
- **MCP Integration**: FastMCP Python SDK with async RAG-enhanced tools
- **Database**: SQLite3 with aiosqlite for async operations + sqlite-vss extension for vector similarity search
- **Frontend**: React or Vue.js for interactive UI with async semantic search components
- **Transport**: HTTP-based MCP transport with async connection handling
- **Async Components**:
  - AsyncIO event loop for concurrent request handling
  - Background task queues (Celery/Redis or FastAPI BackgroundTasks)
  - Async context managers for resource management
  - Connection pooling for database async operations
- **RAG Components**: 
  - Async embedding model interfaces (e.g., sentence-transformers, OpenAI embeddings)
  - SQLite-vss for vector embeddings and similarity search
  - Async retrieval system with concurrent similarity ranking
  - Async context augmentation pipeline with streaming responses

### 5.2 Async-Specific Requirements
- **Concurrent Request Handling**: Support 100+ simultaneous async requests with SQLite connection pooling
- **Non-blocking Operations**: All database and MCP operations must be async/await compatible using aiosqlite
- **Background Task Processing**: Async queue processing for rule updates and embedding generation
- **Async Resource Management**: Use AsyncExitStack for proper cleanup of async resources
- **Streaming Responses**: Support async streaming for large rule analysis results
- **Connection Pooling**: Async SQLite connection pools with configurable limits

### 5.3 RAG-Specific Requirements
- **Async Embedding Generation**: Non-blocking embedding creation for new rules using SQLite transactions
- **Concurrent Vector Search**: Parallel similarity search across 10,000+ rule embeddings using sqlite-vss
- **Async Context Retrieval**: Non-blocking retrieval of top-k (3-5) most relevant rule contexts
- **Streaming Response Augmentation**: Async integration of retrieved context into streaming responses
- **Async Embedding Quality Validation**: Background validation maintaining cosine similarity > 0.8

### 5.4 Performance Requirements
- Async rule lookup response time: < 2 seconds with concurrent handling
- Async complex analysis completion: < 10 seconds with parallel processing
- Support 100 concurrent async users without blocking (SQLite handles multiple readers efficiently)
- 99.9% uptime during training periods with async health checks
- Async database update processing: < 5 minutes with background tasks

### 5.5 Deployment Requirements
- **Local Deployment**: Docker containerization with SQLite database file mounting
- **Cloud Readiness**: Environment-agnostic async configuration with SQLite file backup to cloud storage
- **Async Scalability**: Horizontal scaling support with SQLite file replication
- **Async Monitoring**: Application and performance monitoring with async metrics collection
- **Async Backup**: Automated SQLite database backup system with non-blocking file operations

### 5.6 Data Requirements
- USA Swimming Official Rules and Regulations stored in SQLite tables
- Technical Rules for competitive swimming with full-text search indexes
- Administrative regulations with vector embeddings in sqlite-vss tables
- Historical rule versions and change logs in versioned SQLite tables
- Rule interpretation guidelines with semantic search capabilities

## 8. Technical Specifications

### 8.1 MCP Server Architecture
```python
# Example MCP tools structure with async SQLite and RAG integration
from fastmcp import FastMCP
from typing import List
import asyncio
import aiosqlite
import sqlite3

app = FastMCP("swim-rules-agent")

# SQLite database configuration
DATABASE_PATH = "swim_rules.db"

@app.tool("search_rules")
async def search_rules(query: str, category: str = None, use_semantic: bool = True) -> SearchResults:
    """Search USA Swimming rules by query with optional semantic search using async SQLite operations"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Enable sqlite-vss extension for vector search
        await db.enable_load_extension(True)
        await db.load_extension("vss0")
        
        if use_semantic:
            # Vector similarity search using sqlite-vss
            cursor = await db.execute("""
                SELECT rule_id, rule_text, distance 
                FROM vss_rules 
                WHERE vss_search(embedding, vss_search_params(?, 5))
                ORDER BY distance ASC
            """, (query,))
        else:
            # Traditional full-text search
            cursor = await db.execute("""
                SELECT rule_id, rule_text 
                FROM rules_fts 
                WHERE rules_fts MATCH ? 
                ORDER BY rank
            """, (query,))
        
        results = await cursor.fetchall()
        return SearchResults(results=results)

@app.tool("validate_scenario")
async def validate_scenario(scenario: str, use_rag: bool = True) -> ViolationAnalysis:
    """Analyze swimming scenario for rule violations with RAG-enhanced interpretation using async SQLite processing"""
    async with AsyncExitStack() as stack:
        # Async resource management with SQLite connections
        db = await stack.enter_async_context(aiosqlite.connect(DATABASE_PATH))
        await db.enable_load_extension(True)
        await db.load_extension("vss0")
        
        # Concurrent processing of multiple rule checks
        tasks = [
            check_stroke_violations(db, scenario),
            check_timing_violations(db, scenario), 
            check_equipment_violations(db, scenario)
        ]
        results = await asyncio.gather(*tasks)
        return aggregate_analysis(results)

@app.tool("get_regulation_compliance") 
async def get_regulation_compliance(meet_type: str) -> ComplianceChecklist:
    """Get compliance requirements for specific meet types using async SQLite queries"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            SELECT requirement_id, requirement_text, category
            FROM compliance_requirements 
            WHERE meet_type = ? OR meet_type = 'all'
            ORDER BY priority DESC
        """, (meet_type,))
        
        requirements = await cursor.fetchall()
        return ComplianceChecklist(requirements=requirements)

@app.tool("semantic_search")
async def semantic_search(query: str, top_k: int = 5) -> List[RuleMatch]:
    """Perform vector-based semantic search across rule embeddings with async SQLite operations"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.enable_load_extension(True)
        await db.load_extension("vss0")
        
        cursor = await db.execute("""
            SELECT rule_id, rule_text, rule_number, distance 
            FROM vss_rules 
            WHERE vss_search(embedding, vss_search_params(?, ?))
            ORDER BY distance ASC
        """, (query, top_k))
        
        matches = await cursor.fetchall()
        return [RuleMatch(rule_id=m[0], text=m[1], number=m[2], similarity=1-m[3]) for m in matches]

@app.tool("get_rule_context")
async def get_rule_context(rule_id: str) -> RuleContext:
    """Retrieve contextual information and historical interpretations for a rule using async SQLite operations"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Get rule details and related context
        cursor = await db.execute("""
            SELECT r.rule_text, r.rule_number, r.category,
                   GROUP_CONCAT(ri.interpretation_text) as interpretations,
                   GROUP_CONCAT(rr.related_rule_id) as related_rules
            FROM rules r
            LEFT JOIN rule_interpretations ri ON r.rule_id = ri.rule_id
            LEFT JOIN rule_relationships rr ON r.rule_id = rr.rule_id
            WHERE r.rule_id = ?
            GROUP BY r.rule_id
        """, (rule_id,))
        
        context = await cursor.fetchone()
        return RuleContext.from_tuple(context)

@app.tool("background_update_rules")
async def background_update_rules() -> UpdateStatus:
    """Handle rule updates in background using async SQLite task processing"""
    # Schedule background task for rule updates
    task = asyncio.create_task(update_rules_async())
    return {"status": "processing", "task_id": id(task)}

# Async helper functions for SQLite operations
async def check_stroke_violations(db: aiosqlite.Connection, scenario: str) -> List[Violation]:
    """Async stroke violation checking using SQLite"""
    cursor = await db.execute("""
        SELECT violation_id, violation_text, severity
        FROM stroke_violations sv
        JOIN rules r ON sv.rule_id = r.rule_id
        WHERE ? LIKE '%' || sv.trigger_pattern || '%'
    """, (scenario,))
    
    violations = await cursor.fetchall()
    return [Violation(id=v[0], text=v[1], severity=v[2]) for v in violations]

async def check_timing_violations(db: aiosqlite.Connection, scenario: str) -> List[Violation]:
    """Async timing violation checking using SQLite"""
    cursor = await db.execute("""
        SELECT violation_id, violation_text, severity
        FROM timing_violations tv
        JOIN rules r ON tv.rule_id = r.rule_id
        WHERE ? LIKE '%' || tv.trigger_pattern || '%'
    """, (scenario,))
    
    violations = await cursor.fetchall()
    return [Violation(id=v[0], text=v[1], severity=v[2]) for v in violations]

async def check_equipment_violations(db: aiosqlite.Connection, scenario: str) -> List[Violation]:
    """Async equipment violation checking using SQLite"""
    cursor = await db.execute("""
        SELECT violation_id, violation_text, severity
        FROM equipment_violations ev
        JOIN rules r ON ev.rule_id = r.rule_id
        WHERE ? LIKE '%' || ev.trigger_pattern || '%'
    """, (scenario,))
    
    violations = await cursor.fetchall()
    return [Violation(id=v[0], text=v[1], severity=v[2]) for v in violations]

async def update_rules_async() -> None:
    """Background async rule update processing with SQLite"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Begin transaction for atomic updates
        await db.execute("BEGIN TRANSACTION")
        try:
            # Update rules and regenerate embeddings
            await db.execute("DELETE FROM rules WHERE version < ?", (new_version,))
            await db.executemany("INSERT INTO rules VALUES (?, ?, ?, ?)", new_rules)
            
            # Update vector embeddings
            await db.enable_load_extension(True)
            await db.load_extension("vss0")
            await db.execute("DELETE FROM vss_rules")
            await db.executemany("INSERT INTO vss_rules VALUES (?, ?)", rule_embeddings)
            
            await db.execute("COMMIT")
        except Exception as e:
            await db.execute("ROLLBACK")
            raise e
```

### 8.2 Async SQLite Database Schema Operations
- **Async Connection Management**: Connection pooling with aiosqlite for SQLite operations
- **Non-blocking Queries**: All database operations use async/await patterns with aiosqlite
- **Concurrent Transactions**: SQLite WAL mode for concurrent readers with single writer
- **Async Vector Indexing**: Background async indexing for vector embeddings using sqlite-vss
- **Streaming Results**: Async generators for large result sets from SQLite queries

### 8.3 Async RAG Pipeline Architecture
```python
# Async RAG Pipeline Implementation with SQLite
class AsyncSQLiteRAGPipeline:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.embedding_service = None
        self.db_connection = None
    
    async def __aenter__(self):
        """Async context manager entry with SQLite connection"""
        self.db_connection = await aiosqlite.connect(self.db_path)
        await self.db_connection.enable_load_extension(True)
        await self.db_connection.load_extension("vss0")
        
        # Configure SQLite for optimal performance
        await self.db_connection.execute("PRAGMA journal_mode=WAL")
        await self.db_connection.execute("PRAGMA synchronous=NORMAL")
        await self.db_connection.execute("PRAGMA cache_size=10000")
        
        self.embedding_service = await AsyncEmbeddingService().connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager cleanup"""
        if self.embedding_service:
            await self.embedding_service.close()
        if self.db_connection:
            await self.db_connection.close()
    
    async def process_query(self, query: str) -> EnhancedResponse:
        """Async RAG query processing with concurrent SQLite operations"""
        # Concurrent embedding generation and similarity search
        embedding_task = asyncio.create_task(self.embedding_service.embed(query))
        
        embedding = await embedding_task
        
        # Concurrent context retrieval using SQLite
        similarity_task = asyncio.create_task(self._similarity_search(embedding))
        rule_task = asyncio.create_task(self._get_related_rules(query))
        
        similar_contexts, related_rules = await asyncio.gather(similarity_task, rule_task)
        
        # Async response augmentation
        return await self.augment_response(query, similar_contexts, related_rules)
    
    async def _similarity_search(self, embedding: List[float]) -> List[RuleContext]:
        """Perform vector similarity search using sqlite-vss"""
        cursor = await self.db_connection.execute("""
            SELECT rule_id, rule_text, distance 
            FROM vss_rules 
            WHERE vss_search(embedding, vss_search_params(?, 5))
            ORDER BY distance ASC
        """, (embedding,))
        
        results = await cursor.fetchall()
        return [RuleContext(id=r[0], text=r[1], similarity=1-r[2]) for r in results]
    
    async def _get_related_rules(self, query: str) -> List[Rule]:
        """Get related rules using full-text search"""
        cursor = await self.db_connection.execute("""
            SELECT rule_id, rule_text, rule_number 
            FROM rules_fts 
            WHERE rules_fts MATCH ? 
            ORDER BY rank 
            LIMIT 10
        """, (query,))
        
        results = await cursor.fetchall()
        return [Rule(id=r[0], text=r[1], number=r[2]) for r in results]
```

### 8.4 Async Client Architecture
```python
# Example async client implementation with SQLite awareness
class AsyncSwimRulesClient:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.session: Optional[ClientSession] = None
        self.transport: Optional[Transport] = None
        self.exit_stack = AsyncExitStack()
    
    async def __aenter__(self):
        """Async context manager for resource management"""
        self.transport = await self.exit_stack.enter_async_context(
            get_http_transport("http://localhost:8000")
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.transport)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup async resources"""
        await self.exit_stack.aclose()
    
    async def analyze_scenario(self, scenario: str) -> ViolationAnalysis:
        """Async scenario analysis with streaming response"""
        result = await self.session.call_tool("validate_scenario", {"scenario": scenario})
        return ViolationAnalysis.from_dict(result.content[0].text)
    
    async def search_rules_concurrent(self, queries: List[str]) -> List[SearchResults]:
        """Concurrent rule searches leveraging SQLite's concurrent read capability"""
        tasks = [self.session.call_tool("search_rules", {"query": q}) for q in queries]
        results = await asyncio.gather(*tasks)
        return [SearchResults.from_dict(r.content[0].text) for r in results]
    
    async def backup_database(self, backup_path: str) -> bool:
        """Create async backup of SQLite database"""
        async with aiosqlite.connect(self.db_path) as source:
            async with aiosqlite.connect(backup_path) as backup:
                await source.backup(backup)
                return True
```

### 8.5 SQLite Database Schema
```sql
-- Core rules table with full-text search
CREATE TABLE rules (
    rule_id TEXT PRIMARY KEY,
    rule_number TEXT NOT NULL,
    rule_text TEXT NOT NULL,
    category TEXT NOT NULL,
    effective_date DATE,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-text search virtual table
CREATE VIRTUAL TABLE rules_fts USING fts5(
    rule_id UNINDEXED,
    rule_number,
    rule_text,
    category,
    content='rules',
    content_rowid='rowid'
);

-- Vector embeddings table using sqlite-vss
CREATE VIRTUAL TABLE vss_rules USING vss0(
    embedding(1536),  -- Dimension for OpenAI embeddings
    rule_id TEXT PRIMARY KEY
);

-- Rule relationships and cross-references
CREATE TABLE rule_relationships (
    relationship_id INTEGER PRIMARY KEY,
    rule_id TEXT REFERENCES rules(rule_id),
    related_rule_id TEXT REFERENCES rules(rule_id),
    relationship_type TEXT NOT NULL,
    strength REAL DEFAULT 1.0
);

-- Historical rule versions
CREATE TABLE rule_history (
    history_id INTEGER PRIMARY KEY,
    rule_id TEXT REFERENCES rules(rule_id),
    previous_text TEXT,
    change_description TEXT,
    changed_date DATE,
    version INTEGER
);

-- Violation patterns and triggers
CREATE TABLE violations (
    violation_id TEXT PRIMARY KEY,
    rule_id TEXT REFERENCES rules(rule_id),
    violation_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    penalty_description TEXT,
    trigger_patterns TEXT  -- JSON array of pattern strings
);

-- Analyzed scenarios for learning
CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_text TEXT NOT NULL,
    analysis_result TEXT,  -- JSON result
    applicable_rules TEXT, -- JSON array of rule_ids
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    embedding BLOB  -- Serialized embedding vector
);

-- Performance indexes
CREATE INDEX idx_rules_category ON rules(category);
CREATE INDEX idx_rules_version ON rules(version);
CREATE INDEX idx_violations_type ON violations(violation_type);
CREATE INDEX idx_scenarios_created ON scenarios(created_at);
```
