from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}  # Adjust based on your actual response

def test_create_burger():
    response = client.post("/burgers/", json={"name": "Cheeseburger", "description": "A delicious cheeseburger", "price": 5.99})
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_burger():
    response = client.get("/burgers/1")  # Adjust the ID based on your test data
    assert response.status_code == 200
    assert response.json()["name"] == "Cheeseburger"  # Adjust based on your actual data

def test_update_burger():
    response = client.put("/burgers/1", json={"name": "Updated Cheeseburger", "description": "An updated delicious cheeseburger", "price": 6.99})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Cheeseburger"

def test_delete_burger():
    response = client.delete("/burgers/1")  # Adjust the ID based on your test data
    assert response.status_code == 204
    response = client.get("/burgers/1")
    assert response.status_code == 404  # Ensure the burger is deleted