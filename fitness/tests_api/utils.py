from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(**kwargs):
    defaults = {
        "username": "testuser",
        "password": "testpass123",
        "email": "test@example.com",
        "age": 25,
        "gender": "M",
        "contact": 1234567890,
        "height": 170,
        "weight": 70,
        "diet_preference": "veg",
    }
    defaults.update(kwargs)
    user = User.objects.create_user(**defaults)
    return user


def get_authenticated_client(user):
    client = APIClient()
    response = client.post("/api/login/", {
        "username": user.username,
        "password": "testpass123"
    })
    token = response.data["access_token"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client
