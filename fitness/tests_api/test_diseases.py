from rest_framework.test import APITestCase
from rest_framework import status
from fitness.tests_api.utils import create_user, get_authenticated_client


class DiseaseTests(APITestCase):

    def setUp(self):
        self.user = create_user()
        self.client = get_authenticated_client(self.user)

    def test_add_disease(self):
        response = self.client.post("/api/diseases/", {
            "name": "Asthma",
            "level": "low",
            "duration": 3
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_diseases(self):
        self.client.post("/api/diseases/", {
            "name": "Diabetes",
            "level": "medium",
            "duration": 5
        })

        response = self.client.get("/api/diseases/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_disease(self):
        add_res = self.client.post("/api/diseases/", {
            "name": "BP",
            "level": "high",
            "duration": 2
        })

        disease_id = self.client.get("/api/diseases/").data[0]["id"]

        delete_res = self.client.delete("/api/diseases/", {
            "id": disease_id
        }, format="json")

        self.assertEqual(delete_res.status_code, status.HTTP_200_OK)
