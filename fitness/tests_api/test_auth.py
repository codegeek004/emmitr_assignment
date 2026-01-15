from rest_framework.test import APITestCase
from rest_framework import status
from fitness.tests_api.utils import create_user


class AuthTests(APITestCase):

    def test_register_user(self):
        response = self.client.post("/api/register/", {
            "username": "newuser",
            "password": "password123",
            "email": "new@example.com",
            "age": 22,
            "gender": "M",
            "contact": 9999999999,
            "height": 175,
            "weight": 68,
            "diet_preference": "veg",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        create_user()
        response = self.client.post("/api/login/", {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertIn("access_token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
