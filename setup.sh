cat > app.py << 'EOL'
from flask import Flask, jsonify, request
from inventory import inventory
from external_api import fetch_product

app = Flask(__name__)

@app.route("/inventory", methods=["GET"])
def get_all():
    return jsonify(inventory)

@app.route("/inventory/<int:id>", methods=["GET"])
def get_one(id):
    item = next((i for i in inventory if i["id"] == id), None)
    return jsonify(item) if item else ("Not Found", 404)

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.json
    inventory.append(data)
    return jsonify(data), 201

@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    item = next((i for i in inventory if i["id"] == id), None)
    if item:
        item.update(request.json)
        return jsonify(item)
    return ("Not Found", 404)

@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    global inventory
    inventory = [i for i in inventory if i["id"] != id]
    return ("Deleted", 204)

@app.route("/fetch/<barcode>", methods=["GET"])
def fetch(barcode):
    product = fetch_product(barcode)
    return jsonify(product) if product else ("Not Found", 404)

if __name__ == "__main__":
    app.run(debug=True)
EOL

cat > inventory.py << 'EOL'
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 300,
        "stock": 20
    }
]
EOL

cat > external_api.py << 'EOL'
import requests

def fetch_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            return data.get("product")
    return None
EOL

cat > cli.py << 'EOL'
import requests

BASE_URL = "http://127.0.0.1:5000"

def menu():
    print("\\n1. View Inventory")
    print("2. Add Item")
    print("3. Update Item")
    print("4. Delete Item")
    print("5. Fetch from API")
    print("6. Exit")

while True:
    menu()
    choice = input("Choose: ")

    if choice == "1":
        print(requests.get(f"{BASE_URL}/inventory").json())

    elif choice == "2":
        item = {
            "id": int(input("ID: ")),
            "product_name": input("Name: "),
            "price": int(input("Price: ")),
            "stock": int(input("Stock: "))
        }
        print(requests.post(f"{BASE_URL}/inventory", json=item).json())

    elif choice == "3":
        id = input("ID: ")
        data = {"price": int(input("New price: "))}
        print(requests.patch(f"{BASE_URL}/inventory/{id}", json=data).json())

    elif choice == "4":
        id = input("ID: ")
        requests.delete(f"{BASE_URL}/inventory/{id}")
        print("Deleted")

    elif choice == "5":
        barcode = input("Barcode: ")
        print(requests.get(f"{BASE_URL}/fetch/{barcode}").json())

    elif choice == "6":
        break
EOL

cat > test_app.py << 'EOL'
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200

def test_add_item(client):
    response = client.post("/inventory", json={
        "id": 2,
        "product_name": "Test",
        "price": 100,
        "stock": 10
    })
    assert response.status_code == 201
EOL

cat > requirements.txt << 'EOL'
flask
requests
pytest
EOL

cat > README.md << 'EOL'
# Inventory Management API

## Features
- CRUD operations
- External API integration
- CLI interface
- Unit testing

## Setup
pip install -r requirements.txt
python app.py

## CLI
python cli.py
EOL
