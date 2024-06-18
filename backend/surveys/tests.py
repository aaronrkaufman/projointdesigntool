import json
import os
from unittest.mock import patch

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class ExportJsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("surveys:export_js")

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
            ]
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


class PreviewSurveyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('surveys:preview_survey')

    def test_preview_survey_success(self):
        # Data for a successful request
        data = {
            "attributes": [{"name": "att1", "levels": [{"name": "level1"}, {"name": "another1"}], "locked": True},
                           {"name": "att2", "levels": [{"name": "level2"}, {
                               "name": "another2"}], "locked": False},
                           {"name": "att3", "levels": [{"name": "level3"}, {"name": "another3"}], "locked": False}],
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
            "profiles": 2
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, {
                             "Error": "Cannot generate Preview. Some attributes have no levels."})

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


class ExportCsvTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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
            "profiles": 2,
            "csv_lines": 10000,
        }
        with patch('surveys.views._send_file_response') as mock_send_file_response:
            mock_send_file_response.return_value = HttpResponse(
                status=status.HTTP_201_CREATED)
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_send_file_response.assert_called_once()

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
            "profiles": 2
        }
        with patch('surveys.views._send_file_response') as mock_send_file_response:
            mock_send_file_response.return_value = HttpResponse(
                status=status.HTTP_201_CREATED)
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_send_file_response.assert_called_once()

    def test_export_csv_no_levels(self):
        # Data where an attribute has no levels
        data = {
            "attributes": [{"name": "attr1", "levels": []}],
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


class ExportJsonTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('surveys:export_json')
        self.data = {
            "attributes": [
                {
                    "name": "att1",
                    "locked": True,
                    "levels": [
                        {
                            "name": "level1",
                            "weight": 0.5
                        },
                        {
                            "name": "another1",
                            "weight": 0.5
                        }
                    ]
                },
                {
                    "name": "att2",
                    "locked": False,
                    "levels": [
                        {
                            "name": "level2",
                            "weight": 0.2
                        },
                        {
                            "name": "another2",
                            "weight": 0.8
                        }
                    ]
                },
                {
                    "name": "att3",
                    "locked": False,
                    "levels": [
                        {
                            "name": "level3",
                            "weight": 0.9
                        },
                        {
                            "name": "another3",
                            "weight": 0.1
                        }
                    ]
                }
            ],
            "restrictions": [
                {
                    "condition": [
                        {
                            "attribute": "att1",
                            "operation": "==",
                            "value": "level1"
                        },
                        {
                            "logical": "||",
                            "attribute": "att2",
                            "operation": "==",
                            "value": "level2"
                        }
                    ],
                    "result": [
                        {
                            "attribute": "att3",
                            "operation": "!=",
                            "value": "level3"
                        }
                    ]
                }
            ],
            "cross_restrictions": [],
            "profiles": 2
        }

    def test_export_json_success(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename="survey_export.json"')


class ImportJsonTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('surveys:import_json')
        self.file_path = os.path.join(
            settings.BASE_DIR, 'surveys', 'tests', 'test_data', 'valid_survey.json')

    def test_import_valid_json(self):
        with open(self.file_path, 'rb') as file:
            uploaded_file = SimpleUploadedFile(
                "valid_survey.json", file.read(), content_type="application/json")

        # Make POST request with the uploaded file
        response = self.client.post(
            self.url, {'file': uploaded_file}, format='multipart')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(json.loads(response.content.decode(
            'utf-8')), json.load(open(self.file_path, 'r')))

    def test_import_invalid_json(self):
        # Malformed JSON data as bytes
        invalid_json_data = b'{"key": "value"'  # Missing closing brace

        # Wrap the malformed data in SimpleUploadedFile
        uploaded_file = SimpleUploadedFile(
            "invalid_survey.json", invalid_json_data, content_type="application/json")

        # Make POST request with the uploaded file
        response = self.client.post(
            self.url, {'file': uploaded_file}, format='multipart')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        self.assertTrue('Invalid JSON data' in response.json()['error'])


class CreateQualtricsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("surveys:qsf_to_attribute")
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

    # def test_qsf_to_attributes_success(self):
    #     qsf_path = "./test.qf"
    #     with open(qsf_path, 'r') as qsf:
    #         qsf_content = qsf.read()
    #     payload = {'qsf_content': qsf_content}
    #     response = self.client.post(self.url, payload, format="json")
    #     self.assertEqual(response.status_code, 201)

    # def test_create_qualtrics(self):
    #     response = self.client.post(
    #         self.url, self.payloadSuccess, format="json")
    #     self.assertEqual(response.status_code, 201)
