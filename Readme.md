---
# 🏋️‍♂️ Fitness Studio Booking API

A simple backend API to manage fitness classes and bookings for a fitness studio using **FastAPI**, **SQLAlchemy**, and **SQLite**.
---

## 🚀 Features

✅ User Registration & Authentication (JWT)
✅ Coaches can create classes
✅ Users can book classes (enforced slot limits)
✅ Prevents overbooking
✅ Prevents coaches from booking their own classes
✅ Tests simulate end-to-end workflows
✅ SQLite for easy local development

---

## 📦 Tech Stack

- **Python 3.13+**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **bcrypt**
- **Pytest** (for testing)
- **SQLite** (default)

---

## 🛠️ Installation & Setup

1️⃣ **Clone the repository**

```bash
git clone https://github.com/your-username/fitness-app.git
cd fitness-app
```

2️⃣ **Create a virtual environment**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## ⚡ Running the Server

Run the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

- Users login via `/users/login`
- Include the returned `access_token` in the `Authorization` header:

  ```
  Authorization: Bearer <token>
  ```

---

## 🧪 Running Tests

We provide an end-to-end simulation test using **pytest**:

```bash
pytest test_simulation.py
```

This test:

- Creates coaches and users.
- Creates classes with different slot counts.
- Books classes with users.
- Tests overbooking prevention and instructor restrictions.

---

## 📡 API Usage (cURL Examples)

### 📝 Register Users

```bash
curl -X POST "http://127.0.0.1:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "coach1", "email": "coach1@example.com", "password": "CoachPass1", "is_coach": true}'
```

### 🔑 Login

```bash
curl -X POST "http://127.0.0.1:8000/users/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "coach1", "password": "CoachPass1"}'
```

### 🏋️ Create Class (as Coach)

```bash
curl -X POST "http://127.0.0.1:8000/classes" \
     -H "Authorization: Bearer <coach_token>" \
     -H "Content-Type: application/json" \
     -d '{"name": "Yoga Basics", "start_time": "2025-06-06T10:00:00", "end_time": "2025-06-06T11:00:00", "available_slots": 5}'
```

### 🗓️ Book Class (as User)

```bash
curl -X POST "http://127.0.0.1:8000/bookings" \
     -H "Authorization: Bearer <user_token>" \
     -H "Content-Type: application/json" \
     -d '{"class_id": 1, "client_name": "user1", "client_email": "user1@example.com"}'
```

### 📖 Get Bookings by Email

```bash
curl -X GET "http://127.0.0.1:8000/bookings/by-email?email=user1@example.com"
```

---

## ⚠️ Notes

- **Python 3.13+** is recommended.
- **Pydantic V2** warnings may appear — see the [Pydantic V2 Migration Guide](https://errors.pydantic.dev/2.11/migration/) for future-proofing.
- Datetime: `datetime.utcnow()` is deprecated in Python 3.13+ — recommended to use `datetime.now(UTC)`.

---

## 🚀 Future Improvements

- Dockerfile for containerized deployment
- CI/CD integration
- Pagination on class and booking endpoints
- Email confirmations for bookings

---

Feel free to customize this README to your project’s style or add any additional notes you’d like!

Would you like me to generate a `requirements.txt` with updated libraries or help with a Dockerfile next? 🚀
