from src.embeddings import *

texts = [

    "Gaming Laptop",

    "Bluetooth Speaker",

    "Wireless Mouse",

    "Machine Learning Book"

]

embeddings = generate_embeddings(texts)

print()

print(embeddings.shape)

print()

print(embeddings[0][:10])