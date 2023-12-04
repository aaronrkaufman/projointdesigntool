import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from .models import Survey


# Create your tests here.

Profile = get_user_model()


class SurveyPostTests(TestCase):
    def setUp(self):
        # This method will run before every test function.
        self.profile = Profile.objects.create_user(
            username="testprofile",
            email="testprofile@example.com",
            password="testpassword123",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.profile)

        self.payloadSuccess = {
            "attributes": [
                {
                    "name": "att1",
                    "levels": [
                        {"name": "a", "weight": 0.5},
                        {"name": "b", "weight": 0.5},
                        {"name": "c", "weight": 0.5},
                    ],
                },
                {
                    "name": "att2",
                    "levels": [
                        {"name": "d", "weight": 0.5},
                        {"name": "e", "weight": 0.5},
                    ],
                },
                {
                    "name": "att3",
                    "levels": [
                        {"name": "f", "weight": 0.5},
                        {"name": "g", "weight": 0.5},
                        {"name": "h", "weight": 0.5},
                        {"name": "i", "weight": 0.5},
                    ],
                },
            ]
        }

        self.payloadFailure = {
            "error": [
                {
                    "name": "asfasf",
                },
                {
                    "levels": [
                        {"name": "3", "weight": 0.5},
                        {"name": "4", "weight": 0.5},
                    ],
                },
            ]
        }

    def test_export_success(self):
        url = reverse("surveys:export")
        response = self.client.post(url, self.payloadSuccess, format="json")
        self.assertEqual(response.status_code, 201)

    def test_export_failure(self):
        url = reverse("surveys:export")
        response = self.client.get(url, self.payloadSuccess, format="json")
        self.assertEqual(response.status_code, 405)

    def test_save_success(self):
        url = reverse("surveys:save")
        response = self.client.post(url, self.payloadSuccess, format="json")
        self.assertEqual(response.status_code, 201)

    def test_list_no_surveys_success(self):
        Survey.objects.filter(profile=self.profile).delete()
        url = reverse("surveys:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data["message"], "User has no surveys")

    def test_preview_survey_success(self):
        url = reverse("surveys:preview")
        response = self.client.post(url, self.payloadSuccess, format="json")
        self.assertEqual(response.status_code, 201)

        questions = []
        for question in self.payloadSuccess["attributes"]:
            for answer in question["levels"]:
                questions.append(answer["name"])

        # How to assertEquality?
        # self.assertContains(response.content, 201)

    def test_preview_survey_failure(self):
        url = reverse("surveys:preview")
        response = self.client.post(url, self.payloadFailure, format="json")
        self.assertEqual(response.status_code, 400)

    # def test_preview_csv_success(self):
    #     url = reverse("surveys:preview_csv")
    #     response = self.client.post(url, self.payloadSuccess, format="json")
    #     self.assertEqual(response.status_code, 201)

    def test_preview_csv_failure(self):
        payload = {
            "attributes": [
                {
                    "name": "asfasf",
                    "levels": [],
                },
            ]
        }
        url = reverse("surveys:preview_csv")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"message": "Survey is empty."},
        )

    def test_create_qualtrics(self):
        url = reverse("surveys:qualtrics")
        response = self.client.post(url, self.payloadSuccess, format="json")
        self.assertEqual(response.status_code, 201)
