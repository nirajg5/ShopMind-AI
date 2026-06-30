from src.embeddings import *

text = """
Gaming Laptop with RTX Graphics
"""

embedding = generate_embedding(text)

print("=" * 60)

print("Embedding Shape")

print(embedding.shape)

print()

print("Embedding Dimension")

print(embedding_dimension())

print()

print("Norm")

print(np.linalg.norm(embedding))

print("=" * 60)