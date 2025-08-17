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

#### 4.2.2 Data Management Tools
- **MCP Tools Required**:
  - `update_rules`: Handle USA Swimming rule updates and re-generate embeddings
  - `sync_database`: Synchronize with official rule sources
  - `validate_database`: Ensure data integrity
  - `update_embeddings`: Refresh vector embeddings for rule database

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

### 8.1 PDF Rule Ingestion Pipeline (Python Implementation)

```python
# PDF Rule Ingestion Pipeline with async processing and ChromaDB integration
from fastmcp import FastMCP
from typing import List, Dict, Optional, Tuple
import asyncio
import chromadb
from chromadb.utils import embedding_functions
import pdfplumber
import re
import json
from dataclasses import dataclass
from pathlib import Path
from contextlib import AsyncExitStack

@dataclass
class RuleData:
    """Data class for parsed rule information
    
    Attributes:
        rule_id: Unique identifier for the rule
        rule_number: Official rule number (e.g., "101.2.2")
        rule_title: Title or heading of the rule
        rule_text: Complete text content of the rule
        category: Rule category (e.g., "Stroke Technique")
        section: Section number within the rule document
        subsection: Optional subsection identifier
        effective_date: Date when rule becomes effective
        version: Version number of the rule set
    """
    rule_id: str
    rule_number: str
    rule_title: str
    rule_text: str
    category: str
    section: str
    subsection: Optional[str] = None
    effective_date: Optional[str] = None
    version: int = 1

@dataclass
class IngestionStatus:
    """Status tracking for PDF ingestion process
    
    Attributes:
        total_pages: Total number of pages in PDF
        processed_pages: Number of pages successfully processed
        total_rules: Total number of rules found
        processed_rules: Number of rules successfully processed
        errors: List of error messages encountered
        warnings: List of warning messages
        start_time: Processing start time
        status: Current processing status
    """
    total_pages: int
    processed_pages: int
    total_rules: int
    processed_rules: int
    errors: List[str]
    warnings: List[str]
    start_time: float
    status: str  # 'processing', 'completed', 'failed'

class PdfRuleIngestionPipeline:
    """Async PDF rule ingestion pipeline for USA Swimming rules with ChromaDB integration
    
    This class handles the complete pipeline for extracting, parsing, validating,
    and storing USA Swimming rules from PDF documents into a SQLite database
    with vector embeddings stored in ChromaDB for semantic search.
    """
    
    def __init__(self, chroma_path: str = "./chroma_db") -> None:
        """Initialize the PDF ingestion pipeline

        Args:
            chroma_path: Path to ChromaDB persistence directory
        """
        self.chroma_path = chroma_path
        self.chroma_client = None
        self.chroma_collection = None
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.rule_patterns = {
            'rule_number': re.compile(r'^(\d+(?:\.\d+)*)\s+([A-Z][^.]*?)(?:\s*—\s*(.*))?$'),
            'section_header': re.compile(r'^ARTICLE\s+(\d+)\s*[—-]\s*(.+)$'),
            'subsection': re.compile(r'^(\d+\.\d+)\s+(.+)$'),
            'effective_date': re.compile(r'Effective\s+Date:\s*(.+)', re.IGNORECASE)
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name="swim_rules",
            embedding_function=self.embedding_function,
            metadata={"description": "USA Swimming rules and regulations"}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager cleanup"""
        # ChromaDB client automatically handles cleanup
        pass
    
    async def ingest_pdf(self, pdf_path: Path, version: int = 1) -> IngestionStatus:
        """
        Main ingestion method for processing USA Swimming rules PDF
        
        Args:
            pdf_path: Path to the USA Swimming rules PDF document
            version: Version number for this rule set
            
        Returns:
            IngestionStatus: Status object with processing results
        """
        status = IngestionStatus(
            total_pages=0, processed_pages=0, total_rules=0, processed_rules=0,
            errors=[], warnings=[], start_time=asyncio.get_event_loop().time(),
            status='processing'
        )
        
        try:
            # Extract text from PDF
            extracted_data = await self._extract_pdf_content(pdf_path, status)
            
            # Parse rules from extracted text
            parsed_rules = await self._parse_rules(extracted_data, status)
            
            # Validate parsed rules
            validated_rules = await self._validate_rules(parsed_rules, status)
            
            # Generate embeddings and store in ChromaDB
            await self._generate_and_store_embeddings(validated_rules, status)
            
            status.status = 'completed'
            
        except Exception as e:
            status.errors.append(f"Ingestion failed: {str(e)}")
            status.status = 'failed'
            raise
        
        return status
    
    async def _extract_pdf_content(self, pdf_path: Path, status: IngestionStatus) -> List[Dict]:
        """Extract structured content from PDF pages"""
        extracted_pages = []
        
        with pdfplumber.open(pdf_path) as pdf:
            status.total_pages = len(pdf.pages)
            
            for page_num, page in enumerate(pdf.pages):
                try:
                    # Extract text with layout preservation
                    text = page.extract_text(layout=True)
                    
                    # Extract tables if present
                    tables = page.extract_tables()
                    
                    # Extract metadata
                    page_data = {
                        'page_number': page_num + 1,
                        'text': text,
                        'tables': tables,
                        'bbox': page.bbox,
                        'width': page.width,
                        'height': page.height
                    }
                    
                    extracted_pages.append(page_data)
                    status.processed_pages += 1
                    
                    # Yield control for async processing
                    if page_num % 10 == 0:
                        await asyncio.sleep(0)
                        
                except Exception as e:
                    status.warnings.append(f"Error processing page {page_num + 1}: {str(e)}")
        
        return extracted_pages
    
    async def _parse_rules(self, extracted_pages: List[Dict], status: IngestionStatus) -> List[RuleData]:
        """Parse rules from extracted PDF content"""
        rules = []
        current_section = ""
        current_category = ""
        effective_date = None
        
        for page_data in extracted_pages:
            text_lines = page_data['text'].split('\n')
            
            for line_num, line in enumerate(text_lines):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Check for section headers
                    section_match = self.rule_patterns['section_header'].match(line)
                    if section_match:
                        current_section = section_match.group(1)
                        current_category = section_match.group(2).strip()
                        continue
                      
                    # Check for effective date
                    date_match = self.rule_patterns['effective_date'].search(line)
                    if date_match:
                        effective_date = date_match.group(1).strip()
                        continue
                      
                    # Check for rule number and content
                    rule_match = self.rule_patterns['rule_number'].match(line)
                    if rule_match:
                        rule_number = rule_match.group(1)
                        rule_title = rule_match.group(2).strip()
                        
                        # Extract rule text (may span multiple lines)
                        rule_text = await self._extract_rule_text(
                            text_lines, line_num, page_data['page_number']
                        )
                        
                        rule_data = RuleData(
                            rule_id=f"rule_{rule_number.replace('.', '_')}",
                            rule_number=rule_number,
                            rule_title=rule_title,
                            rule_text=rule_text,
                            category=current_category,
                            section=current_section,
                            effective_date=effective_date,
                            version=1
                        )
                        
                        rules.append(rule_data)
                        status.total_rules += 1
                        
                except Exception as e:
                    status.warnings.append(
                        f"Error parsing line {line_num} on page {page_data['page_number']}: {str(e)}"
                    )
            
            # Yield control for async processing
            await asyncio.sleep(0)
        
        return rules
    
    async def _extract_rule_text(self, text_lines: List[str], start_line: int, page_number: int) -> str:
        """Extract complete rule text that may span multiple lines"""
        rule_text_lines = []
        
        # Start from the line after the rule number
        for i in range(start_line + 1, len(text_lines)):
            line = text_lines[i].strip()
            
            # Stop if we hit another rule number or section header
            if (self.rule_patterns['rule_number'].match(line) or 
                self.rule_patterns['section_header'].match(line) or
                line.startswith('ARTICLE')):
                break
            
            # Skip empty lines at the beginning
            if not rule_text_lines and not line:
                continue
            
            rule_text_lines.append(line)
        
        return ' '.join(rule_text_lines).strip()
    
    async def _validate_rules(self, rules: List[RuleData], status: IngestionStatus) -> List[RuleData]:
        """Validate parsed rules for completeness and accuracy"""
        validated_rules = []
        
        for rule in rules:
            try:
                # Validate rule number format
                if not re.match(r'^\d+(?:\.\d+)*$', rule.rule_number):
                    status.warnings.append(f"Invalid rule number format: {rule.rule_number}")
                    continue
                
                # Validate required fields
                if not rule.rule_text or len(rule.rule_text.strip()) < 10:
                    status.warnings.append(f"Rule {rule.rule_number} has insufficient text content")
                    continue
                
                # Validate rule title
                if not rule.rule_title:
                    status.warnings.append(f"Rule {rule.rule_number} missing title")
                    continue
                
                validated_rules.append(rule)
                status.processed_rules += 1
                
            except Exception as e:
                status.errors.append(f"Validation error for rule {rule.rule_number}: {str(e)}")
        
        return validated_rules
    
    async def _generate_and_store_embeddings(self, rules: List[RuleData], status: IngestionStatus):
        """Generate embeddings and store in ChromaDB"""
        try:
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for rule in rules:
                # Combine rule title and text for embedding
                document_text = f"{rule.rule_title}\n{rule.rule_text}"
                documents.append(document_text)
                
                metadatas.append({
                    "rule_number": rule.rule_number,
                    "rule_title": rule.rule_title,
                    "category": rule.category,
                    "section": rule.section,
                    "version": rule.version,
                    "effective_date": rule.effective_date or ""
                })
                
                ids.append(rule.rule_id)
            
            # Clear existing rules for this version from ChromaDB
            existing_ids = self.chroma_collection.get(
                where={"version": rules[0].version}
            )["ids"]
            
            if existing_ids:
                self.chroma_collection.delete(ids=existing_ids)
            
            # Add new embeddings to ChromaDB in batches
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i + batch_size]
                batch_metas = metadatas[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]
                
                self.chroma_collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids
                )
                
                # Yield control for async processing
                await asyncio.sleep(0)
            
            status.processed_rules = len(rules)
            
        except Exception as e:
            status.errors.append(f"ChromaDB embedding storage error: {str(e)}")
            raise

# MCP tool for PDF ingestion
app = FastMCP("swim-rules-agent")

@app.tool("ingest_pdf_rules")
async def ingest_pdf_rules(pdf_path: str, version: int = 1) -> Dict[str, any]:
    """
    Ingest USA Swimming rules from PDF document
    
    Args:
        pdf_path: Path to the USA Swimming rules PDF file
        version: Version number for this rule set
        
    Returns:
        Dict: Ingestion status and results including processing metrics
    """
    async with PdfRuleIngestionPipeline() as pipeline:
        status = await pipeline.ingest_pdf(Path(pdf_path), version)
        
        return {
            "status": status.status,
            "total_pages": status.total_pages,
            "processed_pages": status.processed_pages,
            "total_rules": status.total_rules,
            "processed_rules": status.processed_rules,
            "errors": status.errors,
            "warnings": status.warnings,
            "processing_time": asyncio.get_event_loop().time() - status.start_time
        }

# Additional MCP tools with ChromaDB integration
@app.tool("search_rules")
async def search_rules(query: str, category: Optional[str] = None, use_semantic: bool = True) -> Dict[str, any]:
    """Search USA Swimming rules by query with optional semantic search using async ChromaDB operations

    Args:
        query: Search query string
        category: Optional category filter
        use_semantic: Whether to use semantic vector search
        
    Returns:
        Dict: Search results with rule matches
    """
    if use_semantic:
        # ChromaDB semantic search
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection("swim_rules")
        
        where_filter = {"category": category} if category else None
        
        results = collection.query(
            query_texts=[query],
            n_results=5,
            where=where_filter
        )
        
        formatted_results = []
        for i, doc in enumerate(results["documents"][0]):
            formatted_results.append({
                "rule_id": results["ids"][0][i],
                "rule_text": doc,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        
        return {"results": formatted_results, "count": len(formatted_results)}
    else:
        # Full-text search not supported without SQLite
        return {"results": [], "count": 0}

@app.tool("semantic_search")
async def semantic_search(query: str, top_k: int = 5) -> List[Dict[str, any]]:
    """Perform vector-based semantic search across rule embeddings using ChromaDB"""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("swim_rules")
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    matches = []
    for i, doc in enumerate(results["documents"][0]):
        matches.append({
            "rule_id": results["ids"][0][i],
            "text": doc,
            "metadata": results["metadatas"][0][i],
            "similarity": 1 - results["distances"][0][i]  # Convert distance to similarity
        })
    
    return matches

@app.tool("get_rule_context")
async def get_rule_context(rule_id: str) -> Dict[str, any]:
    """Retrieve contextual information and historical interpretations for a rule using ChromaDB"""
    # Get rule details from ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("swim_rules")
    rule_doc = collection.get(ids=[rule_id])
    
    if rule_doc["documents"]:
        related_results = collection.query(
            query_texts=[rule_doc["documents"][0]],
            n_results=6,  # Get 6 to exclude the original rule
            where={"rule_number": {"$ne": rule_doc["metadatas"][0]["rule_number"]}}
        )
        
        related_rules = []
        for i, doc in enumerate(related_results["documents"][0][:5]):  # Take top 5
            related_rules.append({
                "rule_id": related_results["ids"][0][i],
                "rule_number": related_results["metadatas"][0][i]["rule_number"],
                "similarity": 1 - related_results["distances"][0][i]
            })
    else:
        related_rules = []
    
    return {
        "rule_data": rule_doc,
        "related_rules": related_rules
    }

@app.tool("background_update_rules")
async def background_update_rules() -> Dict[str, any]:
    """Handle rule updates in background using async ChromaDB task processing"""
    # Schedule background task for rule updates
    task = asyncio.create_task(update_rules_async())
    return {"status": "processing", "task_id": id(task)}

# Async helper functions for ChromaDB operations
async def update_rules_async() -> None:
    """Background async rule update processing with ChromaDB
    
    This function handles the complete rule update process including
    embedding regeneration and error handling.
    """
    # Example: Clear old version embeddings
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("swim_rules")
    old_ids = collection.get(where={"version": {"$lt": 2}})["ids"]
    if old_ids:
        collection.delete(ids=old_ids)
    # Add new embeddings would go here
    # collection.add(documents=new_documents, metadatas=new_metadatas, ids=new_ids)
```

### 8.2 Python Async RAG Pipeline Architecture

```python
# Async RAG Pipeline Implementation with ChromaDB using Python
from typing import List, Optional, Dict, Any
import asyncio
import chromadb
from chromadb.utils import embedding_functions
from contextlib import AsyncExitStack

class AsyncChromaRAGPipeline:
    """Python-based async RAG pipeline for swim rules analysis with ChromaDB
    
    This class implements a Retrieval-Augmented Generation pipeline
    using ChromaDB for vector embeddings and similarity search.
    """
    
    def __init__(self, chroma_path: str = "./chroma_db") -> None:
        """Initialize the RAG pipeline

        Args:
            chroma_path: Path to ChromaDB persistence directory
        """
        self.chroma_path = chroma_path
        self.chroma_client = None
        self.chroma_collection = None
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    
    async def __aenter__(self):
        """Async context manager entry with ChromaDB connection"""
        self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name="swim_rules",
            embedding_function=self.embedding_function
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager cleanup"""
        # ChromaDB client automatically handles cleanup
        pass
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Async RAG query processing with concurrent ChromaDB operations
        
        Args:
            query: User query for rule analysis
            
        Returns:
            Dict: Enhanced response with retrieved context
        """
        # Concurrent similarity search using ChromaDB
        similarity_task = asyncio.create_task(self._similarity_search(query))
        
        similar_contexts = await similarity_task
        
        # Async response augmentation
        return await self.augment_response(query, similar_contexts)
    
    async def _similarity_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform vector similarity search using ChromaDB
        
        Args:
            query: Query text for similarity search
            
        Returns:
            List of rule contexts with similarity scores
        """
        results = self.chroma_collection.query(
            query_texts=[query],
            n_results=5
        )
        
        contexts = []
        for i, doc in enumerate(results["documents"][0]):
            contexts.append({
                "id": results["ids"][0][i],
                "text": doc,
                "metadata": results["metadatas"][0][i],
                "similarity": 1 - results["distances"][0][i]  # Convert distance to similarity
            })
        
        return contexts
    
    async def augment_response(self, query: str, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Augment response with retrieved context from ChromaDB"""
        # Combine query with retrieved contexts
        augmented_response = {
            "query": query,
            "relevant_rules": contexts,
            "confidence": self._calculate_confidence(contexts),
            "citations": [ctx["metadata"]["rule_number"] for ctx in contexts]
        }
        
        return augmented_response
    
    def _calculate_confidence(self, contexts: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on similarity scores"""
        if not contexts:
            return 0.0
        
        # Use highest similarity score as base confidence
        max_similarity = max(ctx["similarity"] for ctx in contexts)
        return min(max_similarity * 100, 95.0)  # Cap at 95%
```

### 8.3 Python Database Schema (ChromaDB Only)

```text
-- ChromaDB Configuration (handled in Python code):
-- - Collection: "swim_rules"
-- - Embedding function: SentenceTransformerEmbeddingFunction
-- - Metadata: rule_number, rule_title, category, section, version, effective_date
-- - Documents: Combined rule_title + rule_text for embedding
-- - IDs: rule_id
```

### 8.4 Python Development Environment Requirements

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

