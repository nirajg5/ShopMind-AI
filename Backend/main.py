"""
main.py

FastAPI Backend for ShopMind AI

Run

uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi import HTTPException

from pydantic import BaseModel

from typing import List
from typing import Optional

from src.rag_pipelines import rag_search

app = FastAPI(

    title="ShopMind AI API",

    version="1.0.0",

    description="AI Shopping Assistant powered by RAG, Pinecone and OpenRouter"

)


# ==========================================================
# Request Model
# ==========================================================

class SearchRequest(BaseModel):

    query: str

    top_k: int = 5


# ==========================================================
# Health Check
# ==========================================================

@app.get("/")

def home():

    return {

        "message": "Welcome to ShopMind AI API",

        "status": "Running"

    }


@app.get("/health")

def health():

    return {

        "status": "Healthy"

    }


# ==========================================================
# Search API
# ==========================================================

@app.post("/search")

def search_products(request: SearchRequest):

    try:

        result = rag_search(

            query=request.query,

            top_k=request.top_k

        )

        products = []

        for _, row in result["products"].iterrows():

            products.append({

                "product_id": row["product_id"],

                "product_name": row["product_name"],

                "discounted_price": row["discounted_price"],

                "actual_price": row["actual_price"],

                "discount_percentage": row["discount_percentage"],

                "rating": row["rating"],

                "rating_count": row["rating_count"],

                "similarity_score": row["similarity_score"]

            })

        return {

            "query": result["query"],

            "response": result["response"],

            "products": products

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# ==========================================================
# Compare Products
# ==========================================================

@app.post("/compare")

def compare_products(request: SearchRequest):

    try:

        result = rag_search(

            request.query,

            request.top_k

        )

        comparison = result["products"][

            [

                "product_name",

                "discounted_price",

                "rating",

                "discount_percentage"

            ]

        ]

        return comparison.to_dict(

            orient="records"

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# ==========================================================
# Product Recommendations
# ==========================================================

@app.post("/recommend")

def recommend(request: SearchRequest):

    try:

        result = rag_search(

            request.query,

            request.top_k

        )

        return {

            "recommendation": result["response"]

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# ==========================================================
# API Information
# ==========================================================

@app.get("/info")

def info():

    return {

        "Application": "ShopMind AI",

        "Version": "1.0.0",

        "Backend": "FastAPI",

        "VectorDB": "Pinecone",

        "LLM": "OpenRouter",

        "Embedding Model": "all-MiniLM-L6-v2"

    }