import pytest
from fastapi.testclient import TestClient

def test_register_business_user(client):
    """Test registering a new business user"""
    response = client.post(
        "/business/register",
        json={
            "email": "test@business.com",
            "business_name": "Test Business",
            "address": "123 Test St",
            "town_city": "Test City",
            "type": "Restaurant"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@business.com"
    assert data["business_name"] == "Test Business"

def test_get_business_user(client):
    """Test getting a business user by ID"""
    register_response = client.post(
        "/business/register",
        json={
            "email": "get@business.com",
            "business_name": "Get Business",
            "address": "456 Get St",
            "town_city": "Get City",
            "type": "Retail"
        }
    )
    business_id = register_response.json()["id"]
    
    response = client.get(f"/business/{business_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == business_id
    assert data["email"] == "get@business.com"
    assert data["business_name"] == "Get Business"

def test_delete_business_user(client):
    """Test deleting a business user"""
    register_response = client.post(
        "/business/register",
        json={
            "email": "delete@business.com",
            "business_name": "Delete Business",
            "address": "789 Delete St",
            "town_city": "Delete City",
            "type": "Service"
        }
    )
    business_id = register_response.json()["id"]
    
    response = client.delete(f"/business/{business_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Business user deleted"}
    
    get_response = client.get(f"/business/{business_id}")
    assert get_response.status_code == 404
