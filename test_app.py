from app import app


def test_inventory_route():
    client = app.test_client()
    res = client.get("/inventory")
    assert res.status_code == 200


def test_create_item():
    client = app.test_client()
    res = client.post("/inventory", json={
        "name": "soda",
        "price": 120,
        "stock": 4
    })
    assert res.status_code == 201
