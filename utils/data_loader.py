import json
#products file is in data folder, load it in variable

def load_products():
    with open("data/products.json", "r") as f:
        data = json.load(f)
    return data["products"]

PRODUCTS = load_products()