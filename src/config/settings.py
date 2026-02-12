"""Configuration settings for the Policy Documents Application."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
POLICY_DOCS_DIR = Path(os.getenv("POLICY_DOCS_DIR", BASE_DIR / "policy_documents"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "output"))

# Ensure directories exist
POLICY_DOCS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# LLM Configuration
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Document processing settings
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".doc", ".txt", ".md"]
MAX_CHUNK_SIZE = 4000  # tokens
CHUNK_OVERLAP = 200  # tokens
