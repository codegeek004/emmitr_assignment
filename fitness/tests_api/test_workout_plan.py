from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from fitness.tests_api.utils import create_user, get_authenticated_client


class WorkoutPlanTests(APITestCase):

    def setUp(self):
        self.user = create_user()
        self.client = get_authenticated_client(self.user)

    @patch("fitness.views.requests.post")
    def test_generate_workout_plan(self, mock_llm):
        mock_llm.return_value.status_code = 200
        mock_llm.return_value.json.return_value = {
            "choices": [{
                "message": {
                    "content": """
                    {
                      "overview": "Test workout",
                      "weekly_plan": {
                        "day_1": "Rest",
                        "day_2": "Rest",
                        "day_3": "Rest",
                        "day_4": "Rest",
                        "day_5": "Rest",
                        "day_6": "Rest",
                        "day_7": "Rest"
                      },
                      "safety_notes": "Test safety"
                    }
                    """
                }
            }]
        }

        response = self.client.post("/api/workout_plan/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("workout_plan", response.data)
