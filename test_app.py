from app import app


def test_get_inventory():
    client = app.test_client()
    res = client.get("/inventory")
    assert res.status_code == 200


def test_get_single_item():
    client = app.test_client()
    res = client.get("/inventory/1")
    assert res.status_code in [200, 404]


def test_add_item():
    client = app.test_client()
    res = client.post("/inventory", json={
        "product_name": "Test Product",
        "price": 10,
        "stock": 5
    })
    assert res.status_code == 201


def test_update_item():
    client = app.test_client()
    res = client.patch("/inventory/1", json={"price": 99})
    assert res.status_code in [200, 404]


def test_delete_item():
    client = app.test_client()
    res = client.delete("/inventory/1")
    assert res.status_code in [200, 404]


def test_fetch_external_api():
    client = app.test_client()
    res = client.get("/fetch-product/737628064502")
    assert res.status_code in [200, 404]
