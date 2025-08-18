import os
import shutil

import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma

RULEBOOK_FP = "../rule_data/2025-mini-rulebook.pdf"
VECTORDB_DIR = "./swim_rules_db"
GLOSSARY_FP = "../rule_data/glossary_terms.txt"
GUIDANCE_FP = "../rule_data/interpretation_guidance.txt"


def main():

    # Load environment variables
    load_dotenv.load_dotenv()

    # Load PDF with selected pages (e.g., pages 10-15)
    loader = PyPDFLoader(RULEBOOK_FP)
    pages = loader.load()

    # Filter selected pages (0-indexed)
    selected_pages = [page for page in pages if 13 <= page.metadata["page"] <= 27]

    # Configure text splitting with overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],  # Default hierarchy
        length_function=len,
        is_separator_regex=False,
    )

    # Split selected pages into chunks
    rule_chunks = text_splitter.split_documents(selected_pages)

    # Configure text splitting glossary terms
    glossary_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        length_function=len,
    )

    with open(GLOSSARY_FP, "r", encoding="utf-8") as file:
        glossary_text = file.read()

    # configure the interpretation guidance text splitter
    glossary_chunks = glossary_text_splitter.create_documents(
        [glossary_text],
        metadatas=[{"source": GLOSSARY_FP, "page": 0}],
    )

    with open(GUIDANCE_FP, "r", encoding="utf-8") as file:
        stroke_interpretations_text = file.read()

    stroke_interpretations_chunks = glossary_text_splitter.create_documents(
        [stroke_interpretations_text],
        metadatas=[{"source": GUIDANCE_FP, "page": 0}],
    )

    # Initialize embeddings model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # remove old db
    shutil.rmtree(VECTORDB_DIR, ignore_errors=True)

    # Create vector store with chunks
    vector_store = Chroma.from_documents(
        rule_chunks + glossary_chunks + stroke_interpretations_chunks, embeddings, persist_directory=VECTORDB_DIR
    )

    # Example RAG query
    results = vector_store.similarity_search("What is breaststroke", k=3)
    for doc in results:
        print(f"Page {doc.metadata['page']}: {doc.page_content[:100]}...")


if __name__ == "__main__":
    main()
