"""
rag_pipeline.py

End-to-End Retrieval-Augmented Generation Pipeline

Pipeline

User Query
      ↓
Semantic Search
      ↓
Retrieve Product Details
      ↓
Prompt Construction
      ↓
LLM Response
"""

import pandas as pd

from src.retrival import retrieve

from src.prompt_builder import create_prompt

from src.llm import chat


# ==========================================================
# Retrieve Products
# ==========================================================

def retrieve_products(
    query: str,
    top_k: int = 5
) -> pd.DataFrame:
    """
    Retrieve top matching products.
    """

    return retrieve(
        query=query,
        top_k=top_k
    )


# ==========================================================
# Generate AI Answer
# ==========================================================

def generate_answer(
    query: str,
    top_k: int = 5
):
    """
    Generate AI response using RAG.
    """

    products = retrieve_products(
        query,
        top_k
    )

    prompt = create_prompt(
        query,
        products
    )

    response = chat(
        prompt
    )

    return response


# ==========================================================
# Complete RAG Search
# ==========================================================

def rag_search(
    query: str,
    top_k: int = 5
):
    """
    Returns

    response
    products
    """

    products = retrieve_products(
        query,
        top_k
    )

    prompt = create_prompt(
        query,
        products
    )

    response = chat(
        prompt
    )

    return {

        "query": query,

        "products": products,

        "response": response

    }