"""
vector_store.py

Pinecone Vector Database Operations

This module handles

• Connect Pinecone
• Create Index
• Connect to Index
• Upload Vectors
• Search Vectors
• Fetch Vectors
• Delete Vectors
"""

from pinecone import Pinecone, ServerlessSpec

from src.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_CLOUD,
    PINECONE_REGION,
    PINECONE_METRIC,
    EMBEDDING_DIMENSION
)

# ==========================================================
# Initialize Pinecone
# ==========================================================

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

# ==========================================================
# Create Index
# ==========================================================

def create_index():

    existing_indexes = pc.list_indexes().names()

    if PINECONE_INDEX_NAME not in existing_indexes:

        pc.create_index(

            name=PINECONE_INDEX_NAME,

            dimension=EMBEDDING_DIMENSION,

            metric=PINECONE_METRIC,

            spec=ServerlessSpec(

                cloud=PINECONE_CLOUD,

                region=PINECONE_REGION

            )

        )

        print(f"Index Created : {PINECONE_INDEX_NAME}")

    else:

        print("Index Already Exists")

# ==========================================================
# Connect to Index
# ==========================================================

def get_index():

    return pc.Index(PINECONE_INDEX_NAME)

# ==========================================================
# Index Statistics
# ==========================================================

def describe_index():

    index = get_index()

    return index.describe_index_stats()

# ==========================================================
# Upload Vectors
# ==========================================================

def upload_vectors(

    records,

    batch_size=100

):

    index = get_index()

    for i in range(0, len(records), batch_size):

        batch = records[i:i + batch_size]

        index.upsert(
            vectors=batch
        )

    print("Vectors Uploaded Successfully")

# ==========================================================
# Query Vectors
# ==========================================================

def query_vectors(

    vector,

    top_k=5,

    include_metadata=True

):

    index = get_index()

    results = index.query(

        vector=vector,

        top_k=top_k,

        include_metadata=include_metadata

    )

    return results

# ==========================================================
# Fetch Vector
# ==========================================================

def fetch_vector(

    vector_id

):

    index = get_index()

    return index.fetch(
        ids=[vector_id]
    )

# ==========================================================
# Delete Vector
# ==========================================================

def delete_vector(

    vector_id

):

    index = get_index()

    index.delete(
        ids=[vector_id]
    )

    print("Vector Deleted")

# ==========================================================
# Delete All Vectors
# ==========================================================

def delete_all_vectors():

    index = get_index()

    index.delete(delete_all=True)

    print("All Vectors Deleted")