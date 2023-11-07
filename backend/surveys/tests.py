import hashlib
from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.
class SurveyPostTests(TestCase):
    def setUp(self):
        # This method will run before every test function.
        self.client = Client()
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
        url = reverse("surveys:export_js")
        response = self.client.post(url, self.payload, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response_content = b"".join(chunk for chunk in response.streaming_content)
        response_hash = hashlib.sha256(response_content).hexdigest()
        with open("survey.js", "rb") as original_file:
            original_hash = hashlib.sha256(original_file.read()).hexdigest()
        self.assertEqual(response_hash, original_hash)

    def test_export_failure(self):
        url = reverse("surveys:export_js")
        response = self.client.get(url, self.payload, content_type="application/json")
        self.assertEqual(response.status_code, 405)
