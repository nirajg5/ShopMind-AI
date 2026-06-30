from src.llm import chat

prompt = """
Recommend a gaming laptop under ₹70000.
"""

response = chat(prompt)

print(response)