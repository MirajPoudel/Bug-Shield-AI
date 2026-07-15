import json
import hashlib
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")

def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        # Seed a demo user
        demo = {
            "faroukmabrouk": {
                "email": "faroukmabrouk999@gmail.com",
                "username": "faroukmabrouk",
                "password": _hash("password123"),
                "created_at": datetime.now().isoformat()
            },
            "demo": {
                "email": "demo@bugshield.ai",
                "username": "demo",
                "password": _hash("demo123"),
                "created_at": datetime.now().isoformat()
            }
        }
        with open(USERS_FILE, "w") as f:
            json.dump(demo, f, indent=2)
    if not os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, "w") as f:
            json.dump({}, f)

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def _load_users():
    _ensure_data_dir()
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def _save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def _load_reviews():
    _ensure_data_dir()
    with open(REVIEWS_FILE, "r") as f:
        return json.load(f)

def _save_reviews(reviews: dict):
    with open(REVIEWS_FILE, "w") as f:
        json.dump(reviews, f, indent=2)

def login(email_or_username: str, password: str):
    """Returns (success, username_or_error)"""
    users = _load_users()
    hashed = _hash(password)
    for uname, data in users.items():
        if (data["email"] == email_or_username or uname == email_or_username) and data["password"] == hashed:
            return True, uname
    return False, "Invalid email or password."

def signup(username: str, email: str, password: str):
    """Returns (success, message)"""
    users = _load_users()
    if username in users:
        return False, "Username already taken."
    for u in users.values():
        if u["email"] == email:
            return False, "Email already registered."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    users[username] = {
        "email": email,
        "username": username,
        "password": _hash(password),
        "created_at": datetime.now().isoformat()
    }
    _save_users(users)
    return True, "Account created! You can now sign in."

def save_review(username: str, review: dict):
    """Save a review result for a user."""
    reviews = _load_reviews()
    if username not in reviews:
        reviews[username] = []
    review["timestamp"] = datetime.now().isoformat()
    reviews[username].insert(0, review)  # newest first
    _save_reviews(reviews)

def get_reviews(username: str) -> list:
    """Get all reviews for a user."""
    reviews = _load_reviews()
    return reviews.get(username, [])

def get_user_stats(username: str) -> dict:
    reviews = get_reviews(username)
    if not reviews:
        return {"total": 0, "avg_score": 0, "best_score": 0}
    scores = [r.get("score", 0) for r in reviews]
    return {
        "total": len(reviews),
        "avg_score": round(sum(scores) / len(scores)),
        "best_score": max(scores)
    }
