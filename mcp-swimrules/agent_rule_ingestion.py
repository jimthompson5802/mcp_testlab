"""
Agent Rule Ingestion Pipeline for MCP Swim Rules

This module implements section 4.4 of the product requirements document,
providing enhanced rule ingestion with metadata extraction for rule identifiers,
categorization, and vector database creation optimized for RAG-based analysis.

Based on the existing rule_ingestion.py but enhanced with:
- Rule identifier extraction (e.g., 101.1, 101.1.1, 101.1.2A, etc.)
- Enhanced metadata with stroke categorization
- Optimized chunking for MCP agent analysis
- Vector database creation under agent_swimrules_db
"""

import os
import shutil
import re
from typing import List, Optional
from dataclasses import dataclass

import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain.schema import Document

# Configuration constants
RULEBOOK_FP = "./rule_data/2025-mini-rulebook.pdf"
VECTORDB_DIR = "./agent_swimrules_db"
GLOSSARY_FP = "./rule_data/glossary_terms.txt"
GUIDANCE_FP = "./rule_data/interpretation_guidance.txt"


@dataclass
class RuleMetadata:
    """Enhanced metadata for swim rules with identifier extraction"""

    rule_id: str
    rule_number: str
    rule_title: str
    category: str
    stroke_type: Optional[str] = None
    section: Optional[str] = None
    page: int = 0
    source: str = ""
    chunk_type: str = "rule"  # rule, glossary, guidance, situation


class AgentRuleIngestionPipeline:
    """
    Enhanced rule ingestion pipeline for MCP agent RAG analysis

    Implements section 4.4 requirements:
    - Rule identifier extraction (101.1, 101.1.1, 101.1.2A, etc.)
    - Enhanced metadata with stroke and category information
    - Optimized chunking for agent analysis
    - Vector database creation for semantic search
    """

    def __init__(self):
        """Initialize the agent rule ingestion pipeline"""
        self.rule_patterns = {
            # Pattern for rule numbers like 101.1, 101.1.1, 101.1.2A, 102.2.1, etc.
            "rule_number": re.compile(r"^(\d+(?:\.\d+)*[A-Z]?)\s+([A-Z][^.\n]*?)(?:\s*—\s*(.*))?$", re.MULTILINE),
            "subsection": re.compile(r"^\.(\d+[A-Z]?)\s+(.+?)(?:\s*—\s*(.*))?$", re.MULTILINE),
            "sub_subsection": re.compile(r"^([A-Z])\s+(.+)$", re.MULTILINE),
            "section_header": re.compile(r"^(\d+)\s+([A-Z][A-Z\s]+)$", re.MULTILINE),
        }

        # Stroke and category mappings
        self.stroke_categories = {
            "breaststroke": ["breaststroke", "breast"],
            "butterfly": ["butterfly", "fly"],
            "backstroke": ["backstroke", "back"],
            "freestyle": ["freestyle", "free"],
            "medley": ["medley", "individual medley", "im"],
            "relay": ["relay"],
            "starts": ["start", "starting"],
            "turns": ["turn", "turning"],
            "general": ["general", "equipment", "officials"],
        }

    def extract_rule_identifiers(self, text: str, page_num: int) -> List[RuleMetadata]:
        """
        Extract rule identifiers and metadata from rule text

        Args:
            text: Raw text from PDF page
            page_num: Page number for metadata

        Returns:
            List of RuleMetadata objects with extracted identifiers
        """
        rules = []
        lines = text.split("\n")
        current_section = None
        current_rule_base = None

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Check for main rule number (e.g., "101.1 STARTS")
            rule_match = self.rule_patterns["rule_number"].match(line)
            if rule_match:
                rule_number = rule_match.group(1)
                rule_title = rule_match.group(2).strip()
                description = rule_match.group(3) if rule_match.group(3) else ""

                current_rule_base = rule_number.split(".")[0]  # e.g., "101" from "101.1"
                current_section = rule_title

                category = self._categorize_rule(rule_title, description)
                stroke_type = self._identify_stroke_type(rule_title, description)

                rules.append(
                    RuleMetadata(
                        rule_id=f"rule_{rule_number}",
                        rule_number=rule_number,
                        rule_title=rule_title,
                        category=category,
                        stroke_type=stroke_type,
                        section=current_section,
                        page=page_num,
                        source=RULEBOOK_FP,
                        chunk_type="rule",
                    )
                )
                continue

            # Check for subsections (e.g., ".1 Equipment", ".2 The Start")
            subsection_match = self.rule_patterns["subsection"].match(line)
            if subsection_match and current_rule_base:
                subsection_num = subsection_match.group(1)
                subsection_title = subsection_match.group(2).strip()
                description = subsection_match.group(3) if subsection_match.group(3) else ""

                full_rule_number = f"{current_rule_base}.{subsection_num}"
                category = self._categorize_rule(subsection_title, description)
                stroke_type = self._identify_stroke_type(subsection_title, description)

                rules.append(
                    RuleMetadata(
                        rule_id=f"rule_{full_rule_number}",
                        rule_number=full_rule_number,
                        rule_title=subsection_title,
                        category=category,
                        stroke_type=stroke_type,
                        section=current_section,
                        page=page_num,
                        source=RULEBOOK_FP,
                        chunk_type="rule",
                    )
                )
                continue

            # Check for sub-subsections (e.g., "A Once all swimmers...")
            sub_subsection_match = self.rule_patterns["sub_subsection"].match(line)
            if sub_subsection_match and current_rule_base and len(rules) > 0:
                letter = sub_subsection_match.group(1)
                content = sub_subsection_match.group(2).strip()

                # Get the last rule number and append the letter
                last_rule = rules[-1]
                if "." in last_rule.rule_number:
                    base_rule = last_rule.rule_number
                    full_rule_number = f"{base_rule}{letter}"

                    category = self._categorize_rule(content)
                    stroke_type = self._identify_stroke_type(content)

                    rules.append(
                        RuleMetadata(
                            rule_id=f"rule_{full_rule_number}",
                            rule_number=full_rule_number,
                            rule_title=content[:50] + "..." if len(content) > 50 else content,
                            category=category,
                            stroke_type=stroke_type,
                            section=current_section,
                            page=page_num,
                            source=RULEBOOK_FP,
                            chunk_type="rule",
                        )
                    )

        return rules

    def _categorize_rule(self, title: str, description: str = "") -> str:
        """Categorize rule based on title and description"""
        text = (title + " " + description).lower()

        if any(keyword in text for keyword in ["start", "starting"]):
            return "Starts"
        elif any(keyword in text for keyword in ["turn", "finish"]):
            return "Turns and Finishes"
        elif any(keyword in text for keyword in ["stroke", "breaststroke", "butterfly", "backstroke", "freestyle"]):
            return "Stroke Technique"
        elif any(keyword in text for keyword in ["relay"]):
            return "Relays"
        elif any(keyword in text for keyword in ["equipment", "pool"]):
            return "Equipment and Facilities"
        elif any(keyword in text for keyword in ["official", "referee", "judge"]):
            return "Officials"
        elif any(keyword in text for keyword in ["disqualif", "violation"]):
            return "Violations and Penalties"
        else:
            return "General Rules"

    def _identify_stroke_type(self, title: str, description: str = "") -> Optional[str]:
        """Identify stroke type from rule text"""
        text = (title + " " + description).lower()

        for stroke, keywords in self.stroke_categories.items():
            if any(keyword in text for keyword in keywords):
                return stroke

        return None

    def create_enhanced_chunks(self, documents: List[Document]) -> List[Document]:
        """
        Create enhanced document chunks with rule metadata

        Args:
            documents: Raw documents from PDF loader

        Returns:
            Enhanced document chunks with extracted metadata
        """
        enhanced_chunks = []

        # Configure text splitter optimized for rule analysis
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # Larger chunks for better context
            chunk_overlap=150,  # More overlap for rule continuity
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
            is_separator_regex=False,
        )

        for doc in documents:
            page_num = doc.metadata.get("page", 0)

            # Extract rule identifiers from the page
            rule_metadata_list = self.extract_rule_identifiers(doc.page_content, page_num)

            # Split the document into chunks
            chunks = text_splitter.split_documents([doc])

            # Enhance each chunk with rule metadata
            for chunk in chunks:
                # Find the most relevant rule metadata for this chunk
                relevant_rule = self._find_relevant_rule_metadata(chunk.page_content, rule_metadata_list)

                if relevant_rule:
                    # Add enhanced metadata - ensure all values are strings for ChromaDB compatibility
                    chunk.metadata = {
                        "rule_id": str(relevant_rule.rule_id),
                        "rule_number": str(relevant_rule.rule_number),
                        "rule_title": str(relevant_rule.rule_title),
                        "category": str(relevant_rule.category),
                        "stroke_type": str(relevant_rule.stroke_type) if relevant_rule.stroke_type else "none",
                        "section": str(relevant_rule.section) if relevant_rule.section else "unknown",
                        "chunk_type": str(relevant_rule.chunk_type),
                        "source": str(relevant_rule.source),
                        "page": str(page_num),
                    }
                else:
                    # Default metadata for chunks without specific rule identifiers
                    chunk.metadata = {
                        "rule_id": f"page_{page_num}_chunk_{len(enhanced_chunks)}",
                        "rule_number": "unknown",
                        "rule_title": "General Content",
                        "category": "General Rules",
                        "stroke_type": "none",
                        "section": "General",
                        "chunk_type": "rule",
                        "source": RULEBOOK_FP,
                        "page": str(page_num),
                    }

                enhanced_chunks.append(chunk)

        return enhanced_chunks

    def _find_relevant_rule_metadata(
        self, chunk_text: str, rule_metadata_list: List[RuleMetadata]
    ) -> Optional[RuleMetadata]:
        """Find the most relevant rule metadata for a text chunk"""
        chunk_lower = chunk_text.lower()

        # Look for exact rule number matches in the chunk
        for rule_meta in rule_metadata_list:
            if rule_meta.rule_number in chunk_text:
                return rule_meta

        # Look for rule title matches
        for rule_meta in rule_metadata_list:
            if rule_meta.rule_title.lower() in chunk_lower:
                return rule_meta

        # Return the first rule from the same page if no specific match
        if rule_metadata_list:
            return rule_metadata_list[0]

        return None

    def load_and_process_documents(self) -> List[Document]:
        """
        Load and process all rule documents with enhanced metadata

        Returns:
            List of processed document chunks ready for vector storage
        """
        all_chunks = []

        # Load main rulebook
        print("Loading main rulebook...")
        loader = PyPDFLoader(RULEBOOK_FP)
        pages = loader.load()

        # Filter relevant pages (rules sections)
        selected_pages = [page for page in pages if 13 <= page.metadata["page"] <= 50]

        # Create enhanced chunks with rule metadata
        rule_chunks = self.create_enhanced_chunks(selected_pages)
        all_chunks.extend(rule_chunks)

        # Process glossary terms
        print("Processing glossary terms...")
        if os.path.exists(GLOSSARY_FP):
            with open(GLOSSARY_FP, "r", encoding="utf-8") as file:
                glossary_text = file.read()

            glossary_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=30,
                length_function=len,
            )

            glossary_chunks = glossary_splitter.create_documents(
                [glossary_text],
                metadatas=[
                    {
                        "rule_id": "glossary",
                        "rule_number": "GLOSSARY",
                        "rule_title": "Glossary Terms",
                        "category": "Definitions",
                        "stroke_type": "none",
                        "section": "Glossary",
                        "chunk_type": "glossary",
                        "source": GLOSSARY_FP,
                        "page": "0",
                    }
                ],
            )
            all_chunks.extend(glossary_chunks)

        # Process interpretation guidance
        print("Processing interpretation guidance...")
        if os.path.exists(GUIDANCE_FP):
            with open(GUIDANCE_FP, "r", encoding="utf-8") as file:
                guidance_text = file.read()

            guidance_splitter = RecursiveCharacterTextSplitter(
                chunk_size=400,
                chunk_overlap=50,
                length_function=len,
            )

            guidance_chunks = guidance_splitter.create_documents(
                [guidance_text],
                metadatas=[
                    {
                        "rule_id": "guidance",
                        "rule_number": "GUIDANCE",
                        "rule_title": "Interpretation Guidance",
                        "category": "Interpretations",
                        "stroke_type": "none",
                        "section": "Guidance",
                        "chunk_type": "guidance",
                        "source": GUIDANCE_FP,
                        "page": "0",
                    }
                ],
            )
            all_chunks.extend(guidance_chunks)

        return all_chunks

    def create_vector_database(self) -> Chroma:
        """
        Create the enhanced vector database for MCP agent RAG analysis

        Returns:
            Configured Chroma vector store
        """
        print("Creating enhanced vector database for MCP agent...")

        # Load environment variables
        load_dotenv.load_dotenv()

        # Load and process all documents
        all_chunks = self.load_and_process_documents()

        print(f"Total processed chunks: {len(all_chunks)}")

        # Print sample metadata for verification
        if all_chunks:
            print("\nSample chunk metadata:")
            sample_chunk = all_chunks[0]
            for key, value in sample_chunk.metadata.items():
                print(f"  {key}: {value}")
            print(f"  Content preview: {sample_chunk.page_content[:100]}...")

        # Initialize embeddings model
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Remove old database
        if os.path.exists(VECTORDB_DIR):
            shutil.rmtree(VECTORDB_DIR, ignore_errors=True)
            print(f"Removed existing database at {VECTORDB_DIR}")

        # Create enhanced vector store
        vector_store = Chroma.from_documents(all_chunks, embeddings, persist_directory=VECTORDB_DIR)

        print(f"Created vector database at {VECTORDB_DIR}")

        # Test the enhanced database
        self._test_enhanced_database(vector_store)

        return vector_store

    def _test_enhanced_database(self, vector_store: Chroma) -> None:
        """Test the enhanced database with sample queries"""
        print("\nTesting enhanced database...")

        test_queries = [
            "What is breaststroke technique?",
            "Rules about false starts",
            "Butterfly turn requirements",
            "Disqualification for stroke violations",
        ]

        for query in test_queries:
            print(f"\nQuery: {query}")
            results = vector_store.similarity_search(query, k=2)

            for i, doc in enumerate(results, 1):
                metadata = doc.metadata
                print(f"  Result {i}:")
                print(f"    Rule ID: {metadata.get('rule_id', 'N/A')}")
                print(f"    Rule Number: {metadata.get('rule_number', 'N/A')}")
                print(f"    Category: {metadata.get('category', 'N/A')}")
                print(f"    Stroke Type: {metadata.get('stroke_type', 'N/A')}")
                print(f"    Content: {doc.page_content[:100]}...")


def main():
    """Main function to create the enhanced vector database for MCP agent"""
    print("Starting Agent Rule Ingestion Pipeline")
    print("Implementing section 4.4 of product requirements document")
    print("=" * 60)

    try:
        pipeline = AgentRuleIngestionPipeline()
        pipeline.create_vector_database()

        print("\n" + "=" * 60)
        print("Agent rule ingestion completed successfully!")
        print(f"Vector database created at: {VECTORDB_DIR}")
        print("Enhanced features implemented:")
        print("  ✓ Rule identifier extraction (101.1, 101.1.1, 101.1.2A, etc.)")
        print("  ✓ Enhanced metadata with stroke categorization")
        print("  ✓ Optimized chunking for agent analysis")
        print("  ✓ Vector database ready for RAG operations")

    except Exception as e:
        print(f"Error during ingestion: {e}")
        raise


if __name__ == "__main__":
    main()
