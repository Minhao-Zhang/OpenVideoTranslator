"""
Glossary Retrieval-Augmented Generation (RAG) system for document retrieval.

This module provides functionality for managing and searching domain-specific terminology
in a glossary using a Retrieval-Augmented Generation (RAG) system.
"""

import logging
from typing import List, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import pandas as pd
import os


class GlossaryRAG:
    """Glossary Retrieval-Augmented Generation (RAG) system for document retrieval."""

    def __init__(self, collection_name: str, embedding_model_name: str):
        """
        Initialize the GlossaryRAG system.

        Args:
            collection_name: Name of the Chroma collection
            embedding_model_name: Name of the HuggingFace embedding model
        """
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model_name
        self.doc_count = 0

        try:
            model_kwargs = {"trust_remote_code": True}
            encode_kwargs = {}

            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs,
            )

            self.vectorstore = Chroma(
                collection_name,
                embedding_function=self.embedding_model
            )
            logging.info(f"Initialized GlossaryRAG system with collection '{
                         collection_name}'")
        except Exception as e:
            logging.error(f"Failed to initialize GlossaryRAG system: {str(e)}")
            raise

    def insert(self, definition: str, example_translation: str) -> None:
        """
        Insert a single document into the vector store.

        Args:
            definition: The definition text
            example_translation: Example translation text
        """
        try:
            if self.embedding_model_name[:5] == "nomic":
                definition = f"search_document: {definition}"

            self.doc_count += 1
            doc = Document(
                page_content=definition,
                metadata={
                    "id": f"id_{self.doc_count}",
                    "example_translation": example_translation
                }
            )
            self.vectorstore.add_documents([doc])
            logging.debug(f"Inserted document {self.doc_count}")
        except Exception as e:
            logging.error(f"Failed to insert document: {str(e)}")
            raise

    def insert_all(self, definitions: List[str], examples: List[str]) -> None:
        """
        Insert multiple documents into the vector store.

        Args:
            definitions: List of definition texts
            examples: List of example translation texts
        """
        try:
            documents = []
            for definition, example in zip(definitions, examples):
                content = definition
                if self.embedding_model_name[:5] == "nomic":
                    content = f"search_document: {definition}"

                self.doc_count += 1
                documents.append(Document(
                    page_content=content,
                    metadata={
                        "id": f"id_{self.doc_count}",
                        "example_translation": example
                    }
                ))

            self.vectorstore.add_documents(documents)
            logging.info(f"Inserted {len(documents)} documents")
        except Exception as e:
            logging.error(f"Failed to insert documents: {str(e)}")
            raise

    def query(self, question: str, n_results: int = 3) -> List[Document]:
        """
        Query the vector store for relevant documents.

        Args:
            question: The query text
            n_results: Number of results to return

        Returns:
            List of relevant documents
        """
        try:
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": n_results}
            )
            return retriever.invoke("Find possible definitions that relates to the sentence: " + question)
        except Exception as e:
            logging.error(f"Query failed: {str(e)}")
            raise


def load_and_insert_data(glossary_rag_instances: List[GlossaryRAG], csv_path: str) -> None:
    """
    Load data from CSV and insert into GlossaryRAG instances.

    Args:
        glossary_rag_instances: List of GlossaryRAG instances
        csv_path: Path to CSV file
    """
    try:
        data = pd.read_csv(csv_path)
        definitions = list(data["Definition"])
        examples = list(data["Example"])

        for glossary_rag in glossary_rag_instances:
            glossary_rag.insert_all(definitions, examples)

        logging.info(f"Loaded data from {csv_path}")
    except Exception as e:
        logging.error(f"Failed to load data from {csv_path}: {str(e)}")
        raise


def display_results(results: List[Document], glossary_rag_name: str) -> None:
    """
    Display query results in a formatted way.

    Args:
        results: List of documents to display
        glossary_rag_name: Name of the GlossaryRAG instance
    """
    print(f"\n{glossary_rag_name} Results:")
    for doc in results:
        print(doc.page_content)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        # Initialize GlossaryRAG instances
        glossary_rag_instances = [
            GlossaryRAG("rag1", "nomic-ai/nomic-embed-text-v1.5"),
            GlossaryRAG("rag2", "dunzhang/stella_en_400M_v5"),
            GlossaryRAG("rag3", "Snowflake/snowflake-arctic-embed-l-v2.0")
        ]

        data_folder = "data"
        csv_files = [os.path.join(data_folder, file) for file in os.listdir(
            data_folder) if file.endswith(".csv")]

        for csv_file in csv_files:
            load_and_insert_data(glossary_rag_instances, csv_file)

        # Interactive question-answering loop
        while True:
            print("=" * 80)
            question = input("Enter a question (or 'exit' to quit): ")
            if question.lower() == "exit":
                break

            for glossary_rag in glossary_rag_instances:
                results = glossary_rag.query(question)
                display_results(results, glossary_rag.collection_name)

    except Exception as e:
        logging.error(f"Application error: {str(e)}")