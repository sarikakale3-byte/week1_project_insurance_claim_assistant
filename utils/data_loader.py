import json

def load_products():
    with open("data/products.json", "r") as f:
        data = json.load(f)
    return data["products"]

PRODUCTS = load_products()