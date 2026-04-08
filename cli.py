import requests

base_url = "http://127.0.0.1:5000"

while True:
    print("\nMENU")
    print("1. view items")
    print("2. add item")
    print("3. update price")
    print("4. delete item")
    print("5. check product")
    print("6. exit")

    choice = input("enter option: ")

    if choice == "1":
        r = requests.get(f"{base_url}/inventory")
        print(r.json())

    elif choice == "2":
        name = input("name: ")
        price = int(input("price: "))
        stock = int(input("stock: "))

        r = requests.post(f"{base_url}/inventory", json={
            "name": name,
            "price": price,
            "stock": stock
        })
        print(r.json())

    elif choice == "3":
        item_id = input("id: ")
        new_price = int(input("new price: "))

        r = requests.patch(f"{base_url}/inventory/{item_id}", json={
            "price": new_price
        })
        print(r.json())

    elif choice == "4":
        item_id = input("id: ")
        r = requests.delete(f"{base_url}/inventory/{item_id}")
        print(r.json())

    elif choice == "5":
        code = input("barcode: ")
        r = requests.get(f"{base_url}/food/{code}")
        print(r.json())

    elif choice == "6":
        break
