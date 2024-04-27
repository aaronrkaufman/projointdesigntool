from unittest.mock import patch
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

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
                        {"name": "b", "weight": 0.5},
                        {"name": "a", "weight": 0.5},
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
                    ],
                },
            ],
            "advanced" : {"att1":0, "att2":0, "att3":1}
        }

        self.payloadFailure = {
            "attributes": [
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

    # def test_save_success(self):
    #     url = reverse("surveys:save")
    #     response = self.client.post(url, self.payloadSuccess, format="json")
    #     self.assertEqual(response.status_code, 201)

    # def test_list_no_surveys_success(self):
    #     Survey.objects.filter(profile=self.profile).delete()
    #     url = reverse("surveys:list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(response.data["message"], "User has no surveys")
        
        
    # def test_qsf_to_attributes_success(self):
    #    qsf_path = "./test.qf"
    #    with open(qsf_path, 'r') as qsf:
    #        qsf_content = qsf.read()
    #    url = reverse("surveys:qsf_to_attribute")
    #    payload = {'qsf_content': qsf_content}
    #    response = self.client.post(url, payload, format="json")
    #    self.assertEqual(response.status_code, 201)

    # def test_create_qualtrics(self):
    #     url = reverse("surveys:qualtrics")
    #     response = self.client.post(url, self.payloadSuccess, format="json")
    #     self.assertEqual(response.status_code, 201)

class PreviewSurveyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.profile = Profile.objects.create_user(
            username="testprofile",
            email="testprofile@example.com",
            password="testpassword123",
        )
        self.client.force_authenticate(user=self.profile)
        self.url = reverse('surveys:preview')  

    def test_preview_survey_success(self):
        # Вata for a successful request
        data = {
            "attributes": [{"name": "attr1", "levels": [{"name": "level1"}, {"name": "level2"}]}],
            "restrictions": [],
            "cross_restrictions": [],
            "profiles": 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('attributes', response.data)
        self.assertIn('previews', response.data)

    def test_preview_survey_no_levels(self):
        # Data where an attribute has no levels
        data = {
            "attributes": [{"name": "attr1", "levels": []}],
            "restrictions": [],
            "cross_restrictions": [],
            "profiles": 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {"Error": "Cannot export to JavaScript. Some attributes have no levels."})

    def test_preview_survey_invalid_data(self):
        data = {} 
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {"Error": "Invalid survey data."})
        
class PreviewCSVTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.profile = Profile.objects.create_user(
            username="testprofile",
            email="testprofile@example.com",
            password="testpassword123",
        )
        self.client.force_authenticate(user=self.profile)
        self.url = reverse('surveys:preview_csv')  

    def test_preview_csv_success(self):
        # Data for a successful request
        data = {
            "attributes": [{"name": "attr1", "levels": [{"name": "level1"}, {"name": "level2"}]}, 
                           {"name": "attr2", "levels": [{"name": "lvl1"}, {"name": "lvl2"}]}],
            "restrictions": [],
            "cross_restrictions": [],
            "profiles": 2
        }
        with patch('surveys.views._sendFileResponse') as mock_sendFileResponse:
            mock_sendFileResponse.return_value = HttpResponse(status=status.HTTP_201_CREATED)
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_sendFileResponse.assert_called_once()

    def test_preview_csv_no_levels(self):
        # Data where an attribute has no levels
        data = {
            "attributes": [{"name": "attr1", "levels": []}],
            "restrictions": [],
            "cross_restrictions": [],
            "profiles": 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {"Error": "Cannot export to JavaScript. Some attributes have no levels."})

    def test_preview_csv_invalid_data(self):
        # Example of sending invalid data
        data = {} 
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {"message": "Invalid survey data."})