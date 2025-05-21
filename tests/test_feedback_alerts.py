import pytest
from fastapi.testclient import TestClient

def test_business_alerts(client, test_db):
    """Test retrieving negative review alerts for a business"""
    business_response = client.post(
        "/business/register",
        json={
            "email": "alert@business.com",
            "business_name": "Alert Business",
            "address": "123 Alert St",
            "town_city": "Alert City",
            "type": "Restaurant"
        }
    )
    business_id = business_response.json()["id"]
    
    from business_profile.models import User
    user = User(id=1, email="alert@user.com")
    test_db.add(user)
    test_db.commit()
    
    from business_profile.models import Feedback
    feedback = Feedback(
        id=1,
        user_id=1,
        username="alert_user",
        business_id=business_id,
        title="Bad Experience",
        body="I had a terrible experience at this business.",
        star_rating=1,
        review_type="Negative",
        alert_seen=False
    )
    test_db.add(feedback)
    test_db.commit()
    
    response = client.get(f"/business/feedback/alert/{business_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["feedback_id"] == 1
    assert data[0]["username"] == "alert_user"
    assert data[0]["title"] == "Bad Experience"
    assert data[0]["star_rating"] == 1
    
    response = client.get(f"/business/feedback/alert/{business_id}")
    assert response.status_code == 200
    assert len(response.json()) == 0  # No more unseen alerts
