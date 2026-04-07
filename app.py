from flask import Flask, jsonify, request
from inventory import inventory
from services.openfoodfacts import get_product_by_barcode

app = Flask(__name__)


# GET all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


# GET single item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)
    return {"error": "Item not found"}, 404


# POST add item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.json

    new_item = {
        "id": len(inventory) + 1,
        "product_name": data["product_name"],
        "brands": data.get("brands"),
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)
    return jsonify(new_item), 201


# PATCH update item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.json

    for item in inventory:
        if item["id"] == item_id:
            item.update(data)
            return jsonify(item)

    return {"error": "Item not found"}, 404


# DELETE item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return {"message": "Item deleted"}

    return {"error": "Item not found"}, 404


# 🌐 External API fetch (OpenFoodFacts only)
@app.route("/fetch-product/<barcode>", methods=["GET"])
def fetch_product(barcode):
    product = get_product_by_barcode(barcode)

    if product:
        return jsonify(product)

    return {"error": "Product not found"}, 404


# 🔥 NEW: External API → Add to inventory
@app.route("/add-from-api/<barcode>", methods=["POST"])
def add_from_api(barcode):
    product = get_product_by_barcode(barcode)

    if not product:
        return {"error": "Product not found in external API"}, 404

    new_item = {
        "id": len(inventory) + 1,
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "price": 0,
        "stock": 0
    }

    inventory.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)
