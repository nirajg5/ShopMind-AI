"""
retrieval.py

Semantic Retrieval Module

Pipeline

User Query
      ↓
Embedding
      ↓
Pinecone
      ↓
Product IDs
      ↓
CSV Metadata
      ↓
Top Products
"""

import pandas as pd

from src.config import (
    PROCESSED_DATA_PATH,
    TOP_K
)

from src.embeddings import generate_embedding

from src.vector_store import query_vectors

# ==========================================================
# Load Dataset Once
# ==========================================================

products_df = pd.read_csv(PROCESSED_DATA_PATH)

print(f"Products Loaded : {len(products_df)}")

# ==========================================================
# Generate Query Embedding
# ==========================================================

def create_query_embedding(query: str):

    return generate_embedding(query).tolist()

# ==========================================================
# Search Pinecone
# ==========================================================

def semantic_search(

    query: str,

    top_k: int = TOP_K

):

    query_vector = create_query_embedding(query)

    results = query_vectors(

        vector=query_vector,

        top_k=top_k,

        include_metadata=True

    )

    return results

# ==========================================================
# Get Product IDs
# ==========================================================

def get_product_ids(results):

    return [

        match["id"]

        for match in results["matches"]

    ]

# ==========================================================
# Retrieve Complete Product Details
# ==========================================================

def retrieve_product_details(

    product_ids

):

    df = products_df[

        products_df["product_id"].isin(product_ids)

    ].copy()

    df["rank"] = df["product_id"].apply(

        product_ids.index

    )

    df = df.sort_values(

        "rank"

    ).drop(

        columns="rank"

    )

    return df.reset_index(drop=True)

# ==========================================================
# Complete Retrieval Pipeline
# ==========================================================

def retrieve(

    query,

    top_k=TOP_K

):

    results = semantic_search(

        query,

        top_k

    )

    ids = get_product_ids(results)

    scores = {

        match["id"]: match["score"]

        for match in results["matches"]

    }

    df = retrieve_product_details(ids)

    df["similarity_score"] = df["product_id"].map(scores)

    return df