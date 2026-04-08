import requests

# get product from openfoodfacts using barcode


def find_food(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        res = requests.get(url)
        data = res.json()

        if data["status"] == 1:
            prod = data["product"]

            return {
                "name": prod.get("product_name"),
                "brand": prod.get("brands")
            }

        return None

    except Exception:
        return None
