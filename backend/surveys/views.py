import json
import os

from dotenv import load_dotenv
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .helpers import (_create_js_file, _create_profiles, _create_survey,
                      _download_survey, _generate_unlocked_order,
                      _populate_csv, _send_file_response)
from .serializers import (QualtricsSerializer, ShortSurveySerializer,
                          SurveySerializer)

load_dotenv()


@extend_schema(
    request=SurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response=SurveySerializer,
            description="A JavaScript file containing the survey data.",
            examples=[
                OpenApiExample(
                    name="JSFileExample",
                    description="A JavaScript file containing the survey data.",
                    value={
                        "content_type": "application/javascript",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="survey_export.js"'
                        },
                    },
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="An error response indicating that the request was invalid.",
        ),
    },
    description="Generates and returns a JavaScript file based on the provided survey data if valid.",
    summary="Export a survey to JavaScript",
    tags=["Export"]
)
@api_view(["POST"])
def export_js(request):
    return _send_file_response(_create_js_file(request))


@extend_schema(
    request=ShortSurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response=ShortSurveySerializer,
            description="Preview of survey generated",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewSuccess",
                    description="A successful preview of survey answers.",
                    value={
                        "attributes": ["attribute1", "attribute2"],
                        "previews": [
                            ["profile1value1", "profile1value2"],
                            ["profile2value1", "profile2value2"],
                        ],
                    },
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ShortSurveySerializer,
            description="Bad Request, no survey data or invalid data provided",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewFailEmpty",
                    description="The survey data provided is empty.",
                    value={"message": "Survey is empty."},
                ),
                OpenApiExample(
                    name="SurveyPreviewFailInvalid",
                    description="The survey data provided is invalid.",
                    value={"message": "Invalid survey data."},
                ),
            ],
        ),
    },
    description="Generates and returns a preview of the survey based on the provided survey data if valid.",
    summary="Preview a survey",
    tags=["Preview"]
)
@api_view(["POST"])
def preview_survey(request):
    serializer = ShortSurveySerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data

        attributes = validated_data["attributes"]
        restrictions = validated_data["restrictions"]
        cross_restrictions = validated_data["cross_restrictions"]
        profiles = validated_data["profiles"]

        if any(not attribute["levels"] for attribute in attributes):
            return Response({"Error": "Cannot generate Preview. Some attributes have no levels."}, status=status.HTTP_400_BAD_REQUEST)

        attributes_list = _generate_unlocked_order(attributes)
        answer = {"attributes": [], "previews": []}
        answer["previews"] = _create_profiles(
            profiles, attributes_list, restrictions, cross_restrictions)
        answer["attributes"] = [key
                                for key in answer["previews"][0].keys()]
        return Response(answer, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=400)


@extend_schema(
    request=SurveySerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=SurveySerializer,
            description="Validated survey data",
            examples=[
                OpenApiExample(
                    name='ValidatedSurveyData',
                    description='Validated Survey Data',
                    value=SurveySerializer().data,
                )
            ]
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="An error response indicating that the request was invalid.",
        ),
    },
    description="Imports a JSON file and validates it against the Survey model. Returns the validated data if successful.",
    summary="Import a JSON formatted survey",
    tags=["Import"]
)
@api_view(["POST"])
def import_json(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        file = request.FILES['file']
    except KeyError as e:
        return Response({'error': f'Invalid file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    if file.content_type != 'application/json':
        return Response({'error': 'Invalid file type. A JSON file is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = JSONParser().parse(file)
    except Exception as e:
        return Response({'error': f'Invalid JSON data: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = SurveySerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=SurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response=ShortSurveySerializer,
            description="A JSON file containing the validated survey data.",
            examples=[
                OpenApiExample(
                    name="JSONFileExample",
                    description="A JSON file containing the validated survey data.",
                    value={
                        "content_type": "application/json",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="survey_export.json"'
                        },
                    },
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ShortSurveySerializer,
            description="Bad Request, no survey data or invalid data provided.",
            examples=[
                OpenApiExample(
                    name="SurveyExportFailEmpty",
                    description="The survey data provided is empty.",
                    value={"message": "Survey data is empty."},
                ),
                OpenApiExample(
                    name="SurveyExportFailInvalid",
                    description="The survey data provided is invalid.",
                    value={"message": "Invalid survey data."},
                ),
            ],
        ),
    },
    description="Exports the validated survey data to a JSON file.",
    summary="Export a survey to JSON",
    tags=["Export"]
)
@api_view(["POST"])
def export_json(request):
    serializer = SurveySerializer(data=request.data)
    if serializer.is_valid():
        filename = 'survey_export.json'
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(request.data, file, ensure_ascii=False, indent=4)
        return _send_file_response(filename)
    else:
        return Response(serializer.errors, status=400)


@extend_schema(
    request=ShortSurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response=ShortSurveySerializer,
            description="A CSV file containing the preview of survey data.",
            examples=[
                OpenApiExample(
                    name="PreviewCSVFileExample",
                    description="A CSV file stream containing the preview of survey data of all possible combinations.",
                    value={
                        "content_type": "text/csv",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="preview.csv"'
                        },
                    }
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ShortSurveySerializer,
            description="Bad Request, no survey data or invalid data provided",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewFailEmpty",
                    description="The survey data provided is empty.",
                    value={"message": "Survey is empty."},
                ),
                OpenApiExample(
                    name="SurveyPreviewFailInvalid",
                    description="The survey data provided is invalid.",
                    value={"message": "Invalid survey data."},
                ),
            ],
        ),
    },
    description="Generates and sends a CSV file of profile combinations based on provided attributes.",
    summary="Export a survey to CSV",
    tags=["Export"]
)
@api_view(["POST"])
def export_csv(request):
    serializer = ShortSurveySerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data

        attributes = validated_data["attributes"]
        restrictions = validated_data["restrictions"]
        cross_restrictions = validated_data["cross_restrictions"]
        profiles = validated_data["profiles"]
        csv_lines = validated_data["csv_lines"]

        if any(not attribute["levels"] for attribute in attributes):
            return Response({"Error": "Cannot export to JavaScript. Some attributes have no levels."}, status=status.HTTP_400_BAD_REQUEST)

        _populate_csv(attributes, profiles, restrictions,
                      cross_restrictions, csv_lines)
        return _send_file_response("profiles.csv")
    else:
        return Response(serializer.errors, status=400)


'''''''''''''''''''''''''''''''''''''''''''''
''''''''''''QUALTRICS LOGIC''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''


@extend_schema(
    request=QualtricsSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response=QualtricsSerializer,
            description="A QSF file containing the survey data.",
            examples=[
                OpenApiExample(
                    name="CreateQualtricsExample",
                    description="Successful creation of Qualtrics survey and export of survey QSF",
                    value={
                        "content_type": "application/json",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="{filename}"'
                        }
                    }
                )
            ]
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=SurveySerializer,
            description="Error in creating Qualtrics survey and exporting QSF file",
            examples=[
                OpenApiExample(
                    name="CreateQualtricsErrorExample",
                    description="This response is returned when request to create Qualtrics survey and export QSF file is invalid",
                    value={
                        "error": "Invalid data provided.",
                        "details": "Incomplete survey data"
                    },
                )
            ]
        )
    },
    description="Generates and exports a Qualtrics survey based on the provided survey data if valid.",
    summary="Export a survey to Qualtrics",
    tags=["Export"]
)
@api_view(["POST"])
def export_qsf(request):
    serializer = QualtricsSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        attributes = validated_data["attributes"]
        filename = validated_data["filename"]
        profiles = validated_data["profiles"]
        tasks = validated_data["tasks"]
        duplicate_first = validated_data["duplicate_first"]
        duplicate_second = validated_data["duplicate_second"]
        repeatFlip = validated_data["noFlip"]
        doubleQ = validated_data["doubleQ"]
        qType = validated_data["qType"]
        qText = validated_data["qText"]

        jsname = _create_js_file(request)
        with open(jsname, "r", encoding="utf-8") as file_js:
            js_text = file_js.read()
        js_text = "//" + json.dumps(request.data) + "\n" + \
            "Qualtrics.SurveyEngine.addOnload(function(){" + js_text + "\n"
        js_text += "});\nQualtrics.SurveyEngine.addOnReady(function(){\
                \n/*Place your JavaScript here to run when the page is fully displayed*/\
                    });\nQualtrics.SurveyEngine.addOnUnload(function()\
                    {\n/*Place your JavaScript here to run when the page is unloaded*/});"

        user_token = os.getenv("QUALTRICS_API_KEY")
        created = _create_survey(
            filename, user_token, tasks, len(
                attributes), profiles, "", js_text, duplicate_first, duplicate_second, repeatFlip, doubleQ, qText
        )

        _download_survey(created, user_token, doubleQ, qType)
        return _send_file_response("survey.qsf")
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=SurveySerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=SurveySerializer,
            description="Reversing QSF File into Survey",
            examples=[
                OpenApiExample(
                    name="ReverseQualtricsExample",
                    description="Successful Reversing QSF File into Survey",
                    value=SurveySerializer().data,)
            ]
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Error in Reversing QSF File into Survey",
        )
    },
    description="Imports a QSF file into an attribute JSON.",
    summary="Imports QSF File",
    tags=["Import"]
)
@api_view(["POST"])
def import_qsf(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        file = request.FILES['file']
    except KeyError as e:
        return Response({'error': f'Invalid file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    if file.content_type != 'application/json':
        return Response({'error': 'Invalid file type. A QSF file is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = JSONParser().parse(file)
    except Exception as e:
        return Response({'error': f'Invalid QSF data: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    survey_elements = data.get("SurveyElements")
    for elem in survey_elements:
        if elem.get("PrimaryAttribute") == "QID1":
            payload = elem.get("Payload")
            question_js = payload.get("QuestionJS")
            projoint_survey = question_js.split("\n")[0]
            if "//" in projoint_survey:
                attribute_data = json.loads(
                    projoint_survey[2:])
                serializer = SurveySerializer(data=attribute_data)
                if serializer.is_valid():
                    return Response(serializer.validated_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                break
    return Response({'error': 'Invalid QSF survey. Please use QSF file from our platform.'}, status=status.HTTP_400_BAD_REQUEST)
