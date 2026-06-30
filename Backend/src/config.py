"""
config.py

Central configuration file for ShopMind AI.

This module contains:

• API Keys
• Model Names
• Pinecone Settings
• File Paths
• LLM Parameters
"""

import os

from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# API Keys
# ==========================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# ==========================================================
# Embedding Model
# ==========================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

EMBEDDING_DIMENSION = 384

# ==========================================================
# OpenRouter Model
# ==========================================================

LLM_MODEL = "meta-llama/llama-3.1-8b-instruct"

# Examples

# LLM_MODEL = "google/gemma-3-27b-it"

# LLM_MODEL = "deepseek/deepseek-chat"

# ==========================================================
# Pinecone
# ==========================================================

PINECONE_INDEX_NAME = "shopmind"

PINECONE_CLOUD = "aws"

PINECONE_REGION = "us-east-1"

PINECONE_METRIC = "cosine"

# ==========================================================
# LLM Parameters
# ==========================================================

TEMPERATURE = 0.3

MAX_TOKENS = 700

TOP_P = 1.0

# ==========================================================
# Retrieval
# ==========================================================

TOP_K = 5

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DATA_PATH = os.path.join(
    BASE_DIR,
    "processed",
    "amazon_products_unique.csv"
)

EMBEDDINGS_PATH = os.path.join(
    BASE_DIR,
    "embeddings",
    "product_embeddings.npy"
)

METADATA_PATH = os.path.join(
    BASE_DIR,
    "embeddings",
    "product_metadata.csv"
)

# ==========================================================
# Streamlit
# ==========================================================

PAGE_TITLE = "ShopMind AI"

PAGE_ICON = "🛒"

LAYOUT = "wide"