import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product/"


def get_product_by_barcode(barcode):
    response = requests.get(f"{BASE_URL}{barcode}.json")

    if response.status_code != 200:
        return None

    data = response.json()

    if data["status"] == 1:
        product = data["product"]
        return {
            "product_name": product.get("product_name"),
            "brands": product.get("brands"),
            "ingredients": product.get("ingredients_text")
        }

    return None
