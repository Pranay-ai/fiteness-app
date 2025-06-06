import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

client = TestClient(app)

# Clear and recreate tables for a clean test run
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Helper function to register users
def register_user(username, email, password, is_coach=False):
    response = client.post("/users/", json={
        "username": username,
        "email": email,
        "password": password,
        "is_coach": is_coach
    })
    assert response.status_code == 200
    return response.json()

# Helper function to login and get token
def login_user(username, password):
    response = client.post("/users/login", json={
        "username": username,
        "password": password
    })
    assert response.status_code == 200
    return response.json()["access_token"]

# Helper function to create a class
def create_class(token, name, start_time, end_time, available_slots):
    response = client.post("/classes", 
        json={
            "name": name,
            "start_time": start_time,
            "end_time": end_time,
            "available_slots": available_slots
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    return response.json()

# Helper function to book a class
def book_class(token, class_id, client_name, client_email):
    response = client.post("/bookings",
        json={
            "class_id": class_id,
            "client_name": client_name,
            "client_email": client_email
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    return response

# Test simulation
def test_full_booking_flow():
    # 1. Create 2 coaches
    register_user("coach1", "coach1@example.com", "CoachPass1", True)
    register_user("coach2", "coach2@example.com", "CoachPass2", True)

    coach1_token = login_user("coach1", "CoachPass1")
    coach2_token = login_user("coach2", "CoachPass2")

    # 2. Create 5 users
    user_tokens = []
    for i in range(1, 6):
        username = f"user{i}"
        email = f"user{i}@example.com"
        password = f"UserPass{i}"
        register_user(username, email, password, False)
        token = login_user(username, password)
        user_tokens.append((username, email, token))

    # 3. Each coach creates a class
    class1 = create_class(coach1_token, "Yoga Basics", "2025-06-06T10:00:00", "2025-06-06T11:00:00", 5)
    class2 = create_class(coach2_token, "Zumba Dance", "2025-06-07T10:00:00", "2025-06-07T11:00:00", 10)

    # 4. Users try to book classes
    # Book Class 1 (5 slots)
    for i in range(5):
        username, email, token = user_tokens[i % len(user_tokens)]
        response = book_class(token, class1["id"], username, email)
        assert response.status_code == 200

    # Try overbooking Class 1
    overbook_response = book_class(user_tokens[0][2], class1["id"], "user1", "user1@example.com")
    assert overbook_response.status_code == 400
    assert "No slots available" in overbook_response.json()["detail"]

    # Book Class 2 (10 slots)
    for i in range(10):
        username, email, token = user_tokens[i % len(user_tokens)]
        response = book_class(token, class2["id"], username, email)
        assert response.status_code == 200

    # Try overbooking Class 2
    overbook_response2 = book_class(user_tokens[0][2], class2["id"], "user1", "user1@example.com")
    assert overbook_response2.status_code == 400
    assert "No slots available" in overbook_response2.json()["detail"]

    # 5. Coaches try to book their own classes (should fail)
    coach1_selfbook = book_class(coach1_token, class1["id"], "coach1", "coach1@example.com")
    assert coach1_selfbook.status_code == 400
    assert "Instructors cannot book their own classes" in coach1_selfbook.json()["detail"]

    coach2_selfbook = book_class(coach2_token, class2["id"], "coach2", "coach2@example.com")
    assert coach2_selfbook.status_code == 400
    assert "Instructors cannot book their own classes" in coach2_selfbook.json()["detail"]

    print("✅ All test cases passed!")
