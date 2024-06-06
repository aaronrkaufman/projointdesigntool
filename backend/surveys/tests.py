from unittest.mock import patch
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

Profile = get_user_model()


class ExportJsTest(TestCase):
    def setUp(self):
        # This method will run before every test function.
        self.profile = Profile.objects.create_user(
            username="testprofile",
            email="testprofile@example.com",
            password="testpassword123",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.profile)
        self.url = reverse("surveys:export")

        self.payloadSuccess = {
            "attributes": [
                {
                    "name": "att1",
                    "levels": [
                        {"name": "b"},
                        {"name": "a"},
                    ],
                },
                {
                    "name": "att2",
                    "levels": [
                        {"name": "d"},
                        {"name": "e"},
                    ],
                },
                {
                    "name": "att3",
                    "levels": [
                        {"name": "f"},
                        {"name": "g"},
                    ],
                },
            ],
            "advanced": {"att1": 0, "att2": 0, "att3": 1}
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
        response = self.client.post(
            self.url, self.payloadSuccess, format="json")
        self.assertEqual(response.status_code, 201)

    def test_export_failure(self):
        response = self.client.get(
            self.url, self.payloadSuccess, format="json")
        self.assertEqual(response.status_code, 405)

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
        # Data for a successful request
        data = {
            "attributes": [{"name": "att1", "levels": [{"name": "level1"}, {"name": "another1"}]},
                           {"name": "att2", "levels": [
                               {"name": "level2"}, {"name": "another2"}]},
                           {"name": "att3", "levels": [{"name": "level3"}, {"name": "another3"}]}],
            "restrictions": [],
            "cross_restrictions": [],
            "profiles": 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_preview_survey_with_rest_success(self):
        # Data for a successful request
        data = {
            "attributes": [{"name": "att1", "levels": [{"name": "level1"}, {"name": "another1"}]},
                           {"name": "att2", "levels": [
                               {"name": "level2"}, {"name": "another2"}]},
                           {"name": "att3", "levels": [{"name": "level3"}, {"name": "another3"}]}],
            "restrictions": [{
                "condition": [{"attribute": "att1", "operation": "==", "value": "level1"},
                              {"logical": "||", "attribute": "att2", "operation": "==", "value": "level2"}],
                "result": [{"attribute": "att3", "operation": "!=", "value": "level3"}]}],
            "cross_restrictions": [],
            "profiles": 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_preview_survey_with_rest_failure(self):
        # Data with wrong operation in condition
        data = {
            "attributes": [{"name": "att1", "levels": [{"name": "level1"}, {"name": "another1"}]},
                           {"name": "att2", "levels": [
                               {"name": "level2"}, {"name": "another2"}]},
                           {"name": "att3", "levels": [{"name": "level3"}, {"name": "another3"}]}],
            "restrictions": [{
                "condition": [{"attribute": "att1", "operation": "=", "value": "level1"}],
                "result": [{"attribute": "att3", "operation": "!=", "value": "level3"}]}],
            "cross_restrictions": [],
            "profiles": 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Invalid operation in result.',
                      response.data['non_field_errors'][0])

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
        self.assertDictEqual(response.data, {
                             "Error": "Cannot export to JavaScript. Some attributes have no levels."})

    def test_preview_survey_invalid_data(self):
        # Data with no attributes
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_preview_survey_with_cross_rest_success(self):
        # Data for a successful request
        data = {
            "attributes": [
                {
                    "name": "att1",
                    "levels": [
                        {"name": "level1"},
                        {"name": "another1"},
                    ]
                },
                {
                    "name": "att2",
                    "levels": [
                        {"name": "level2"},
                        {"name": "another2"},
                    ]
                },
                {
                    "name": "att3",
                    "levels": [
                        {"name": "level3"},
                        {"name": "another3"},
                    ]
                }
            ],
            "restrictions": [],
            "cross_restrictions": [
                {
                    "condition": {"attribute": "att1", "operation": "!=", "value": "level1"},
                    "result": {"attribute": "att1", "operation": "==", "value": "another1"},
                }
            ],
            "profiles": 2
        }
        for _ in range(100):
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.json()["previews"][0]["att1"], response.json()[
                             "previews"][1]["att1"])

    def test_preview_survey_with_cross_rest_success_2(self):
        # Data for a successful request
        data = {
            "attributes": [
                {
                    "name": "att1",
                    "levels": [
                        {"name": "level1"},
                        {"name": "another1"},
                    ]
                },
                {
                    "name": "att2",
                    "levels": [
                        {"name": "level2"},
                        {"name": "another2"},
                    ]
                },
                {
                    "name": "att3",
                    "levels": [
                        {"name": "level3"},
                        {"name": "another3"},
                    ]
                }
            ],
            "restrictions": [],
            "cross_restrictions": [
                {
                    "condition": {"attribute": "att1", "operation": "==", "value": "level1"},
                    "result": {"attribute": "att1", "operation": "==", "value": "another1"},
                }
            ],
            "profiles": 2
        }
        for _ in range(100):
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn("another1", set((response.json()["previews"][0]["att1"], response.json()[
                "previews"][1]["att1"])))


class ExportCSVTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.profile = Profile.objects.create_user(
            username="testprofile",
            email="testprofile@example.com",
            password="testpassword123",
        )
        self.client.force_authenticate(user=self.profile)
        self.url = reverse('surveys:export_csv')

    def test_export_csv_success(self):
        # Data for a successful request
        data = {
            "attributes": [{"name": "att1", "levels": [{"name": "lvl1"}, {"name": "another1"}, {"name": "bruh1"}]},
                           {"name": "att2", "levels": [{"name": "lvl2"}, {
                               "name": "another2"}, {"name": "bruh2"}]},
                           {"name": "att3", "levels": [{"name": "lvl3"}, {
                               "name": "another3"}, {"name": "bruh3"}]},
                           {"name": "att4", "levels": [{"name": "lvl4"}, {
                               "name": "another4"}, {"name": "bruh4"}]},
                           {"name": "att5", "levels": [{"name": "lvl5"}, {
                               "name": "another5"}, {"name": "bruh5"}]},
                           {"name": "att6", "levels": [{"name": "lvl6"}, {"name": "another6"}, {"name": "bruh6"}]}],
            "restrictions": [],
            "cross_restrictions": [],
            "profiles": 2
        }
        with patch('surveys.views._sendFileResponse') as mock_sendFileResponse:
            mock_sendFileResponse.return_value = HttpResponse(
                status=status.HTTP_201_CREATED)
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_sendFileResponse.assert_called_once()

    def test_export_csv_with_rest_success(self):
        # Data for a successful request
        data = {
            "attributes": [{"name": "att1", "levels": [{"name": "level1"}, {"name": "another1"}]},
                           {"name": "att2", "levels": [
                               {"name": "level2"}, {"name": "another2"}]},
                           {"name": "att3", "levels": [{"name": "level3"}, {"name": "another3"}]}],
            "restrictions": [{
                "condition": [{"attribute": "att1", "operation": "==", "value": "level1"},
                              {"logical": "||", "attribute": "att2", "operation": "==", "value": "level2"}],
                "result": [{"attribute": "att3", "operation": "!=", "value": "level3"}]}],
            "cross_restrictions": [],
            "profiles": 2
        }
        with patch('surveys.views._sendFileResponse') as mock_sendFileResponse:
            mock_sendFileResponse.return_value = HttpResponse(
                status=status.HTTP_201_CREATED)
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_sendFileResponse.assert_called_once()

    def test_export_csv_no_levels(self):
        # Data where an attribute has no levels
        data = {
            "attributes": [{"name": "attr1", "levels": []}],
            "restrictions": [],
            "cross_restrictions": [],
            "profiles": 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {
                             "Error": "Cannot export to JavaScript. Some attributes have no levels."})

    def test_export_csv_invalid_data(self):
        # Example of sending invalid data
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
