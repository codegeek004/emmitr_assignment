from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from fitness.tests_api.utils import create_user, get_authenticated_client


class DietPlanTests(APITestCase):

    def setUp(self):
        self.user = create_user()
        self.client = get_authenticated_client(self.user)

    @patch("fitness.views.requests.post")
    def test_generate_diet_plan(self, mock_llm):
        mock_llm.return_value.status_code = 200
        mock_llm.return_value.json.return_value = {
            "choices": [{
                "message": {
                    "content": """
                    {
                      "overview": "Test diet",
                      "weekly_plan": {
                        "day_1": "Veg",
                        "day_2": "Veg",
                        "day_3": "Veg",
                        "day_4": "Veg",
                        "day_5": "Veg",
                        "day_6": "Veg",
                        "day_7": "Veg"
                      },
                      "safety_notes": "Test safety"
                    }
                    """
                }
            }]
        }

        response = self.client.post("/api/diet_plan/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("diet_plan", response.data)
