from flask import Flask, request, jsonify
from inventory import store_items
from services.openfoodfacts import find_food

app = Flask(__name__)


# show all items
@app.route("/inventory", methods=["GET"])
def get_items():
    return jsonify(store_items)


# get one item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in store_items:
        if item["id"] == item_id:
            return jsonify(item)

    return {"message": "item missing"}, 404


# add new item
@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.json

    new_item = {
        "id": len(store_items) + 1,
        "name": data.get("name"),
        "price": data.get("price"),
        "stock": data.get("stock")
    }

    store_items.append(new_item)
    return jsonify(new_item), 201


# update item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.json

    for item in store_items:
        if item["id"] == item_id:
            if "price" in data:
                item["price"] = data["price"]
            if "stock" in data:
                item["stock"] = data["stock"]

            return jsonify(item)

    return {"message": "item not found"}, 404


# delete item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in store_items:
        if item["id"] == item_id:
            store_items.remove(item)
            return {"message": "deleted"}

    return {"message": "nothing there"}, 404


# check product from API
@app.route("/food/<barcode>", methods=["GET"])
def get_food_api(barcode):
    result = find_food(barcode)

    if result:
        return jsonify(result)

    return {"message": "not found in api"}, 404


# fetch + save product
@app.route("/food/<barcode>", methods=["POST"])
def save_food_api(barcode):
    result = find_food(barcode)

    if not result:
        return {"message": "api failed"}, 404

    new_item = {
        "id": len(store_items) + 1,
        "name": result["name"],
        "price": 0,
        "stock": 0
    }

    store_items.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)
