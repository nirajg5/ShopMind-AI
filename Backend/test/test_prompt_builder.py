from src.retrival import retrieve

from src.prompt_builder import *

products = retrieve(

    "Gaming Laptop under ₹70000"

)

context = build_context(products)

print(context)