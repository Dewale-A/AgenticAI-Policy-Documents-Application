"""Custom CrewAI tools for document processing."""

import os
from pathlib import Path
from typing import List, Optional, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.config.settings import POLICY_DOCS_DIR, SUPPORTED_EXTENSIONS


class DocumentReaderInput(BaseModel):
    """Input schema for DocumentReaderTool."""
    file_path: Optional[str] = Field(
        default=None,
        description="Path to a specific document to read. If not provided, lists all available documents."
    )


class DocumentReaderTool(BaseTool):
    """Tool for reading and extracting text from policy documents."""
    
    name: str = "document_reader"
    description: str = """
    Reads and extracts text content from policy documents.
    Supports PDF, DOCX, TXT, and MD files.
    If no file_path is provided, returns a list of all available documents.
    Use this tool to ingest and understand policy document contents.
    """
    args_schema: type[BaseModel] = DocumentReaderInput
    
    def _run(self, file_path: Optional[str] = None) -> str:
        """Execute the document reading."""
        if file_path is None:
            return self._list_documents()
        return self._read_document(file_path)
    
    def _list_documents(self) -> str:
        """List all available policy documents."""
        documents = []
        for ext in SUPPORTED_EXTENSIONS:
            documents.extend(POLICY_DOCS_DIR.glob(f"*{ext}"))
            documents.extend(POLICY_DOCS_DIR.glob(f"**/*{ext}"))
        
        if not documents:
            return f"No documents found in {POLICY_DOCS_DIR}. Please add policy documents to analyze."
        
        doc_list = "\n".join([f"- {doc.relative_to(POLICY_DOCS_DIR)}" for doc in documents])
        return f"Available policy documents:\n{doc_list}"
    
    def _read_document(self, file_path: str) -> str:
        """Read and extract text from a specific document."""
        # Handle relative paths
        if not os.path.isabs(file_path):
            full_path = POLICY_DOCS_DIR / file_path
        else:
            full_path = Path(file_path)
        
        if not full_path.exists():
            return f"Error: Document not found at {full_path}"
        
        ext = full_path.suffix.lower()
        
        try:
            if ext == ".pdf":
                return self._read_pdf(full_path)
            elif ext in [".docx", ".doc"]:
                return self._read_docx(full_path)
            elif ext in [".txt", ".md"]:
                return self._read_text(full_path)
            else:
                return f"Error: Unsupported file format {ext}"
        except Exception as e:
            return f"Error reading document: {str(e)}"
    
    def _read_pdf(self, path: Path) -> str:
        """Extract text from PDF."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return f"[Content from {path.name}]\n\n{text}"
        except ImportError:
            return "Error: pypdf not installed. Run: pip install pypdf"
    
    def _read_docx(self, path: Path) -> str:
        """Extract text from DOCX."""
        try:
            from docx import Document
            doc = Document(path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return f"[Content from {path.name}]\n\n{text}"
        except ImportError:
            return "Error: python-docx not installed. Run: pip install python-docx"
    
    def _read_text(self, path: Path) -> str:
        """Read plain text file."""
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return f"[Content from {path.name}]\n\n{text}"


class DocumentSearchInput(BaseModel):
    """Input schema for DocumentSearchTool."""
    query: str = Field(description="Search query to find relevant sections in documents")
    file_path: Optional[str] = Field(
        default=None,
        description="Specific document to search. If not provided, searches all documents."
    )


class DocumentSearchTool(BaseTool):
    """Tool for searching within policy documents."""
    
    name: str = "document_search"
    description: str = """
    Searches for specific terms or concepts within policy documents.
    Returns relevant sections that match the query.
    Useful for finding specific policies, rules, or requirements.
    """
    args_schema: type[BaseModel] = DocumentSearchInput
    
    def _run(self, query: str, file_path: Optional[str] = None) -> str:
        """Search documents for the query."""
        reader = DocumentReaderTool()
        
        if file_path:
            content = reader._read_document(file_path)
            return self._search_content(query, content, file_path)
        
        # Search all documents
        results = []
        for ext in SUPPORTED_EXTENSIONS:
            for doc_path in POLICY_DOCS_DIR.glob(f"*{ext}"):
                content = reader._read_document(str(doc_path))
                result = self._search_content(query, content, doc_path.name)
                if result:
                    results.append(result)
        
        if not results:
            return f"No matches found for '{query}' in any documents."
        
        return "\n\n---\n\n".join(results)
    
    def _search_content(self, query: str, content: str, source: str) -> Optional[str]:
        """Simple search within content."""
        query_lower = query.lower()
        lines = content.split("\n")
        matching_sections = []
        
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                # Get context (2 lines before and after)
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                context = "\n".join(lines[start:end])
                matching_sections.append(context)
        
        if matching_sections:
            return f"[Matches in {source}]\n\n" + "\n...\n".join(matching_sections[:5])
        return None
