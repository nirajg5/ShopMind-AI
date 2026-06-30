"""
embeddings.py

Generate text embeddings using Sentence Transformers.
"""

from typing import List

import numpy as np

from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL


# ==========================================================
# Load Model (Load only once)
# ==========================================================

print("Loading Embedding Model...")

model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding Model Loaded Successfully")


# ==========================================================
# Generate Embedding for One Text
# ==========================================================

def generate_embedding(text: str) -> np.ndarray:
    """
    Generate embedding for a single text.

    Parameters
    ----------
    text : str

    Returns
    -------
    numpy.ndarray
    """

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding


# ==========================================================
# Generate Batch Embeddings
# ==========================================================

def generate_embeddings(
    texts: List[str],
    batch_size: int = 32
) -> np.ndarray:
    """
    Generate embeddings for multiple texts.
    """

    embeddings = model.encode(

        texts,

        batch_size=batch_size,

        convert_to_numpy=True,

        normalize_embeddings=True,

        show_progress_bar=True

    )

    return embeddings


# ==========================================================
# Save Embeddings
# ==========================================================

def save_embeddings(
    embeddings: np.ndarray,
    path: str
):

    np.save(path, embeddings)

    print(f"Embeddings Saved -> {path}")


# ==========================================================
# Load Embeddings
# ==========================================================

def load_embeddings(path: str):

    embeddings = np.load(path)

    print(f"Embeddings Loaded <- {path}")

    return embeddings


# ==========================================================
# Embedding Dimension
# ==========================================================

def embedding_dimension():

    return model.get_sentence_embedding_dimension()