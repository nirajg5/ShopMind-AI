from src.rag_pipelines import rag_search

result = rag_search(

    "Best Gaming Laptop for ML"

)

print(result["response"])