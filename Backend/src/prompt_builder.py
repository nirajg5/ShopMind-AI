"""
prompt_builder.py

Prompt Engineering Module

Responsibilities
----------------
1. Define the system prompt
2. Build context from retrieved products
3. Build the final prompt for the LLM
"""

import pandas as pd


# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are ShopMind AI, an intelligent AI Shopping Assistant.

Your responsibilities:

1. Answer ONLY using the retrieved product information.
2. Never hallucinate or invent products.
3. If no suitable product exists, clearly mention it.
4. Recommend the best products based on the user's query.
5. Explain WHY each recommendation is suitable.
6. Compare products whenever appropriate.
7. Mention price, discount, rating and important features.
8. Keep responses professional, concise and helpful.
9. Do not fabricate specifications, prices or ratings.
"""


# ==========================================================
# Build Context
# ==========================================================

def build_context(products_df: pd.DataFrame) -> str:
    """
    Build context for the LLM using the
    search_document created during preprocessing.
    """

    if products_df.empty:
        return "No products found."

    context = ""

    for index, row in products_df.iterrows():

        similarity = row.get("similarity_score", "N/A")

        context += f"""
==================================================

Product {index + 1}

Similarity Score:
{similarity}

{row["search_document"]}

==================================================

"""

    return context


# ==========================================================
# Build User Prompt
# ==========================================================

def build_prompt(
    user_query: str,
    context: str
) -> str:

    return f"""
User Query:

{user_query}

--------------------------------------------------

Retrieved Product Information

{context}

--------------------------------------------------

Instructions

• Recommend the best matching products.
• Explain why each product is recommended.
• Mention important specifications.
• Mention price, discount and rating whenever available.
• If multiple products are relevant, compare them.
• If no relevant product exists, clearly mention that.
• Use ONLY the retrieved information.

Answer:
"""


# ==========================================================
# Complete Prompt
# ==========================================================

def create_prompt(
    user_query: str,
    products_df: pd.DataFrame
) -> str:
    """
    Build the complete prompt for the LLM.
    """

    context = build_context(products_df)

    return build_prompt(
        user_query=user_query,
        context=context
    )