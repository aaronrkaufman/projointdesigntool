import hashlib
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

        self.payload = {
            "attributes": [
                {
                    "name": "asfasf",
                    "levels": [
                        {"name": "1", "weight": 0.5},
                        {"name": "2", "weight": 0.5},
                    ],
                },
                {
                    "name": "asf",
                    "levels": [
                        {"name": "3", "weight": 0.5},
                        {"name": "4", "weight": 0.5},
                    ],
                },
            ]
        }

    def test_export_success(self):
        url = reverse("surveys:export")
        response = self.client.post(url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)

        response_content = b"".join(chunk for chunk in response.streaming_content)
        response_hash = hashlib.sha256(response_content).hexdigest()
        with open("survey.js", "rb") as original_file:
            original_hash = hashlib.sha256(original_file.read()).hexdigest()
        self.assertEqual(response_hash, original_hash)

    def test_export_failure(self):
        url = reverse("surveys:export")
        response = self.client.get(url, self.payload, format="json")
        self.assertEqual(response.status_code, 405)

    def test_save_success(self):
        url = reverse("surveys:save")
        response = self.client.post(url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)

    def test_list_no_surveys_success(self):
        Survey.objects.filter(profile=self.profile).delete()
        url = reverse("surveys:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data["message"], "User has no surveys")
