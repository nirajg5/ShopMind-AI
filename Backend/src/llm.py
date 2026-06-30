"""
llm.py

OpenRouter LLM Module

Responsibilities
----------------
1. Initialize OpenRouter Client
2. Generate LLM Responses
3. Handle Errors
"""

from openai import OpenAI

from src.config import (
    OPENROUTER_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)

from src.prompt_builder import SYSTEM_PROMPT


# ==========================================================
# Initialize OpenRouter Client
# ==========================================================

client = OpenAI(

    api_key=OPENROUTER_API_KEY,

    base_url="https://openrouter.ai/api/v1"

)


# ==========================================================
# Generate Response
# ==========================================================

def generate_response(
    prompt: str,
    stream: bool = False
):

    try:

        response = client.chat.completions.create(

            model=LLM_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=TEMPERATURE,

            max_tokens=MAX_TOKENS,

            stream=stream

        )

        if stream:

            return response

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"


# ==========================================================
# Chat Function
# ==========================================================

def chat(
    user_prompt: str
):

    return generate_response(user_prompt)