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
- Complex scenario analysis involving multiple rules
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

#### 4.1.1 Violation Checking
- **Requirement**: Analyze described swimming scenarios for rule violations
- **Acceptance Criteria**:
  - Accept natural language scenario descriptions
  - Identify applicable rules and potential violations
  - Provide detailed explanation of violations
  - Handle multiple violation scenarios

#### 4.1.2 Complex Scenario Analysis
- **Requirement**: Analyze multi-faceted situations involving multiple rules using RAG-enhanced interpretation
- **Acceptance Criteria**:
  - Process scenarios with multiple rule interactions using vector similarity search
  - Prioritize rule applications based on semantic relevance
  - Identify conflicting regulations through context-aware analysis
  - Provide step-by-step analysis with supporting rule citations
  - Generate natural language explanations augmented by retrieved rule context

### 4.2 MCP Integration Features

#### 4.2.1 Siutaion Analysis
- **MCP Tools Required**:
  - `analyze_situation`: Analyze specified situation to determine if legal or disqualification with rationale and rule citation.
    - Transport: stdio
    - Input: Natural language description of the swimming scenario
    - Using the natural language description of the swimming scenario, use to RAG to retrieve relevant rules and context from ChromaDB vector database
    - Use OpenAI LLM `gpt-4o` with the retrieved RAG documents to arrive at a decision and rationale.
    - Extract from the retrieved RAG documents metadata the identifiers to be in the list of relevant citations.
    - Output:
      - `decision`: "ALLOWED" or "DISQUALIFICATION"
      - `rationale`: Detailed explanation of the decision
      - `rule_citations`: List of relevant rule citations (identifier)

### 4.3 User Interface Requirements

#### 4.3.1 Query Interface
- Clean, intuitive search interface with semantic search capabilities
- Support for natural language queries with intent recognition

#### 4.3.2 Web Interface for swim situation analysis

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
│  ┌─────────────────┐  ┌─────────────────┐                                   │
│  │   [Analyze]     │  │ [Clear Input]   │                                   │
│  └─────────────────┘  └─────────────────┘                                   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                            ANALYSIS RESULTS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Decision:                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🚫 DISQUALIFICATION                                                 │   │
│  │                                                                     │    │
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
│                                                                             │
└───────────────────────────────────────────────────────────────────────────-─┘
```


#### 4.3.3 Interface Component Specifications

**Scenario Input Area:**
- Multi-line text area (minimum 4 rows, expandable)
- Character limit: 2000 characters with live counter
- Placeholder text with example scenarios
- Input validation for minimum meaningful content

**Decision Display:**
- Large, prominently displayed result banner
- Color-coded status indicators:
  - 🟢 GREEN: "ALLOWED" / "NO VIOLATION"
  - 🔴 RED: "DISQUALIFICATION" / "VIOLATION"
- Visual icons for quick recognition

**Rationale Text Box:**
- Read-only formatted text area
- Supports rich text formatting for emphasis
- Expandable/collapsible for long explanations
- Word wrap enabled

**Rule Citations Box:**
- Structured list format with hierarchical display
- Clickable rule numbers for detailed rule text
- Categorized citations (Primary, Supporting, Related)

#### 4.3.4 Response Display
- Clear rule citation format
- Complete rule text with semantic highlighting
- Visual indicators for violation severity and rule relevance
- Structured analysis for complex scenarios with supporting evidence
- Print-friendly formatting with embedded context
- Source attribution for retrieved contextual information

#### 4.3.5 Web UI Styling
- Separate CSS file for styling

### 4.4 Rule Ingestion
- **Requirement**: Ingest USA swimming rules and regulations from PDF documents into a vector database for semantic search.
- **Acceptance Criteria**:
  - Create embedding vectors for all ingested rules
  - Create a metadata related to the ingested rules (e.g., stroke, rule identifier)
  - Example of rule identifiers in the following sample text are
    - `101.1`
    - `101.1.1`
    - `101.1.2A`
    - `101.1.2B`
    - `101.2`
    - `102.2.1`
    - `102.2.2`
    - `102.2.3`

```text
101.1 STARTS
.1 Equipment — A loudspeaker start system conforming to 103.18, with or without
an underwater recall device, and an electronic strobe signal visible to all manual
timers for forward and backstroke starts, shall be the preferred starting device.
.2 The Start
A Once all swimmers have removed their clothing, except for swimwear, the
Referee shall signal the commencement of an event by a short series of
whistles inviting them to get ready at the starting end, followed by a long
whistle indicating that they should take and maintain their positions on the
starting platform, the deck, or in the water. In backstroke and medley relay
events, at the Referee’s first long whistle, the swimmers shall immediately
enter the water and at the second long whistle shall return without undue
delay to the starting position.
Except as otherwise noted, all provisions in this Rulebook are effective immediately.
Rules in effect on the first day of a meet shall govern throughout that
meet.
20
101.1
B When the swimmers and officials are ready, the Referee shall signal with
an outstretched arm to the Starter that the swimmers are under the Starter’s
control.
C On the Starter’s command “take your marks,” the swimmers shall immediately
assume their starting position, in the forward start, with at least one
foot at the front of the starting platform or the deck. Swimmers starting in
the water must have at least one hand in contact with the wall or starting
platform. When all swimmers are stationary, the Starter shall give the starting
signal.
D When a swimmer does not respond promptly to the command "take your
marks," the Starter shall immediately release all swimmers with a "stand"
command upon which the swimmers may stand up or step off the blocks.
E A swimmer shall not be disqualified for an illegal starting position at the
start if the race is permitted to proceed. Enforcement of the correct starting
position is the responsibility of the Starter.
.3 False Starts
A Any swimmer initiating a start before the signal may be disqualified if the
Referee independently observes and confirms the Starter’s observation
that a violation occurred. Swimmers remaining on the starting blocks shall
be relieved from their starting positions with a "stand" command and may
step off the blocks.
B If the starting signal has been given before the disqualification is declared,
the race shall continue without recall. If the Referee independently
observes and confirms the Starter’s observation that a violation occurred,
the swimmer or swimmers who have false started shall be disqualified
upon completion of the race.
C If the recall signal is activated, no swimmer shall be charged with a false
start and the Starter shall restart the race upon signal by the Referee.
D A swimmer who would otherwise be charged with a false start may be
relieved of the charge if the false start was caused by the swimmer’s reaction
to a “stand” command.
E Declared false start: swimmers reporting to the Referee prior to the start of
their race and declaring their intent not to compete shall be disqualified
except as noted in 207.11.6D(1).
.4 Warning Signal — With the exception of relays, in events 500 yards or longer, the
Starter or a designee shall sound a warning signal over the water at the finish end
of the lane of the leading swimmer when that swimmer has two lengths plus five
yards or five meters to swim. As an alternative, a bell warning signal may be given
over each lane by a lane judge or timer for that lane.
21
1
101.1
.5 Deliberate Delay or Misconduct
A The Starter shall report a swimmer to the Referee for delaying the start, for
willfully disobeying an order or for any other misconduct taking place at the
start, but only the Referee may disqualify a swimmer for such delay, willful
disobedience or misconduct.
B The Referee shall disqualify a swimmer who fails to appear at the starting
platform ready to swim in time for the initial start of his/her heat.
C Such disqualification shall not be charged as a false start.
101.2 BREASTSTROKE
.1 Start — The forward start shall be used.
.2 Stroke — After the start and after each turn when the swimmer leaves the wall,
the body shall be kept on the breast. It is not permitted to roll onto the back at any
time except at the turn after the touch of the wall where it is permissible to turn in
any manner as long as the body is on the breast when leaving the wall. Throughout
the race the stroke cycle must be one arm stroke and one leg kick in that order.
All movements of the arms shall be simultaneous without alternating movement.
The hands shall be pushed forward together from the breast on, under, or over the
water.
The elbows shall be under water except for the final stroke before the turn, during
the turn and for the final stroke at the finish. The hands shall be brought back on or
under the surface of the water. The hands shall not be brought back beyond the
hip line, except during the first stroke after the start and each turn.
During each complete cycle, some part of the swimmer’s head shall break the surface
of the water. After the start and after each turn, the swimmer may take one
arm stroke completely back to the legs. The head must break the surface of the
water before the hands turn inward at the widest part of the second stroke.
.3 Kick — After the start and each turn, at any time prior to the first breaststroke kick,
a single butterfly kick is permitted. Following which, all movements of the legs shall
be simultaneous without alternating movement.
The feet must be turned outwards during the propulsive part of the kick. Scissors,
alternating movements or downward butterfly kicks are not permitted except as provided
herein. Breaking the surface of the water with the feet is allowed unless followed
by a downward butterfly kick.
.4 Turns and Finish — At each turn and at the finish of the race, the touch shall be
made with both hands separated and simultaneously at, above, or below the water
level. At the last stroke before the turn and at the finish, an arm stroke not followed
22
101.2
by a leg kick is permitted. The head may be submerged after the last arm pull prior
to the touch, provided it breaks the surface of the water at some point during the
last complete or incomplete cycle preceding the touch.
101.3 BUTTERFLY
.1 Start — The forward start shall be used.
.2 Stroke — After the start and after each turn, the swimmer’s body must be on the
breast. The swimmer is permitted one or more leg kicks, but only one arm pull
under water, which must bring the swimmer to the surface. It shall be permissible
for a swimmer to be completely submerged for a distance of not more than 15
meters (16.4 yards) after the start and after each turn. By that point, the head
must have broken the surface. The swimmer must remain on the surface until the
next turn or finish. From the beginning of the first arm pull, the body shall be kept
on the breast except at the turn after the touch of the wall where it is permissible
to turn in any manner as long as the body is on the breast when leaving the wall.
Both arms must be brought forward simultaneously over the water and pulled back
simultaneously under the water throughout the race.
.3 Kick — All up and down movements of the legs and feet must be simultaneous.
The position of the legs or the feet need not be on the same level, but they shall
not alternate in relation to each other. A scissors or breaststroke kicking movement
is not permitted.
.4 Turns — At each turn the body shall be on the breast. The touch shall be made
with both hands separated and simultaneously at, above, or below the water surface.
Once a touch has been made, the swimmer may turn in any manner desired
as long as the body is on the breast when leaving the wall.
.5 Finish — At the finish, the body shall be on the breast and the touch shall be
made with both hands separated and simultaneously at, above, or below the water
surface.
```   

### 4.5 Utilities

#### 4.5.1 Rule Lookup Utility
- prompt the user for a query
- Given a query, retrieve relevant rules for that query
- Integrates with the ChromaDB vector database for efficient similarity searches
- Display rule metadata (e.g., rule ID, title, description) alongside the rule text

## 5. Technical Requirements

### 5.1 Architecture
- **Programming Language**: Python 3.11+ with asyncio for concurrent operations
- **Web Framework**: FastAPI for high-performance async API endpoints
- **MCP Integration**: FastMCP Python SDK with async RAG-enhanced tools
- **Vector Database**: ChromaDB for vector embeddings and similarity search
- **Frontend**: React or Vue.js for interactive UI with async semantic search components
- **Transport**: HTTP-based MCP transport with async connection handling
- **Async Components**:
  - AsyncIO event loop for concurrent request handling
  - Background task queues (Celery/Redis or FastAPI BackgroundTasks)
  - Async context managers for resource management
  - Connection pooling for database async operations
- **RAG Components**: 
  - Async embedding model interfaces (e.g., sentence-transformers, OpenAI embeddings)
  - ChromaDB for vector embeddings and similarity search
  - Async retrieval system with concurrent similarity ranking
  - Async context augmentation pipeline with streaming responses

### 5.2 Python-Specific Requirements
- **Python Version**: Python 3.11 or higher for optimal async performance
- **Type Hints**: Complete type annotations following PEP 484 and PEP 585
- **Code Style**: PEP 8 compliance with 120-character line length limit
- **Documentation**: Google-style docstrings for all classes and functions
- **Error Handling**: Comprehensive try/except blocks with descriptive error messages
- **Async Programming**: Proper use of async/await patterns and AsyncExitStack for resource management

### 5.3 Async-Specific Requirements
- **Concurrent Request Handling**: Support 100+ simultaneous async requests with ChromaDB connection pooling
- **Non-blocking Operations**: All MCP operations must be async/await compatible using async ChromaDB client
- **Background Task Processing**: Async queue processing for rule updates and embedding generation
- **Async Resource Management**: Use AsyncExitStack for proper cleanup of async resources
- **Streaming Responses**: Support async streaming for large rule analysis results
- **Connection Pooling**: Async ChromaDB client with configurable connection limits

### 5.4 RAG-Specific Requirements
- **Async Embedding Generation**: Non-blocking embedding creation for new rules using ChromaDB async operations
- **Concurrent Vector Search**: Parallel similarity search across 10,000+ rule embeddings using ChromaDB query API
- **Async Context Retrieval**: Non-blocking retrieval of top-k (3-5) most relevant rule contexts from ChromaDB
- **Streaming Response Augmentation**: Async integration of retrieved context into streaming responses
- **Async Embedding Quality Validation**: Background validation maintaining cosine similarity > 0.8 using ChromaDB distance metrics

### 5.5 Performance Requirements
- Async rule lookup response time: < 2 seconds with concurrent handling
- Async complex analysis completion: < 10 seconds with parallel processing
- Support 100 concurrent async users without blocking (ChromaDB handles concurrent reads efficiently)
- 99.9% uptime during training periods with async health checks
- Async database update processing: < 5 minutes with background tasks

### 5.6 Deployment Requirements
- **Local Deployment**: Docker containerization with ChromaDB persistence
- **Cloud Readiness**: Environment-agnostic async configuration with ChromaDB cloud storage
- **Async Scalability**: Horizontal scaling support with ChromaDB distributed deployment
- **Async Monitoring**: Application and performance monitoring with async metrics collection
- **Async Backup**: Automated ChromaDB collection backup

### 5.7 PDF Rule Ingestion Requirements
- **PDF Processing**: Python-based automated extraction using pdfplumber library
- **Rule Parsing**: Intelligent parsing using Python regex patterns for rule structure
- **Data Validation**: Python validation functions for rule completeness and accuracy
- **Version Management**: Python-based tracking of rule document versions
- **Error Handling**: Robust Python exception handling for PDF parsing failures
- **Async Processing**: Python asyncio-based non-blocking PDF processing

## 8. Technical Specifications

### 8.1 Python Database Schema (ChromaDB Only)

```text
-- ChromaDB Configuration (handled in Python code):
-- - Collection: "swim_rules"
-- - Embedding function: SentenceTransformerEmbeddingFunction
-- - Metadata: rule_number, rule_title, stroke
-- - Documents: Combined rule_title + rule_text for embedding
-- - IDs: rule_id
```

### 8.2 Python Development Environment Requirements

- **Python Version**: 3.11+ with typing support

- **Required Packages**:
  - `fastmcp`: MCP server and client functionality
  - `fastapi`: Web framework for REST API
  - `chromadb`: Vector database for embeddings and similarity search
  - `pdfplumber`: PDF text extraction
  - `sentence-transformers`: Embedding model support
  - `asyncio`: Built-in async/await support
- **Development Tools**:
  - `pytest`: Testing framework
  - `black`: Code formatting
  - `mypy`: Static type checking
  - `ruff`: Fast Python linter

