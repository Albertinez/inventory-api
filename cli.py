import requests


BASE_URL = "http://127.0.0.1:5000"


def menu():
    print("\n1. View Inventory")
    print("2. Add Item")
    print("3. Update Item")
    print("4. Delete Item")
    print("5. Fetch from API")
    print("6. Exit")


def view_inventory():
    res = requests.get(f"{BASE_URL}/inventory")
    print(res.json())


def add_item():
    name = input("Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))

    data = {
        "product_name": name,
        "price": price,
        "stock": stock
    }

    res = requests.post(f"{BASE_URL}/inventory", json=data)
    print(res.json())


def update_item():
    item_id = input("ID: ")
    price = input("New price: ")

    res = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json={"price": float(price)}
    )
    print(res.json())


def delete_item():
    item_id = input("ID: ")
    res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    print(res.json())


def fetch_api():
    barcode = input("Enter barcode: ")
    res = requests.get(f"{BASE_URL}/fetch-product/{barcode}")
    print(res.json())


while True:
    menu()
    choice = input("Choose: ")

    if choice == "1":
        view_inventory()
    elif choice == "2":
        add_item()
    elif choice == "3":
        update_item()
    elif choice == "4":
        delete_item()
    elif choice == "5":
        fetch_api()
    elif choice == "6":
        break
