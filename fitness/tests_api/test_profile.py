from rest_framework.test import APITestCase
from rest_framework import status
from fitness.tests_api.utils import create_user, get_authenticated_client


class ProfileTests(APITestCase):

    def setUp(self):
        self.user = create_user()
        self.client = get_authenticated_client(self.user)

    def test_create_fitness_info(self):
        response = self.client.put("/api/fitness_info/", {
            "fitness_goal": "weight_loss",
            "current_fitness_level": "beginner",
            "workout_location": "home"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_info(self):
        response = self.client.put("/api/user_info/", {
            "smoking": False,
            "drinking": False,
            "stress_level": "medium",
            "injuries": "knee pain"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
