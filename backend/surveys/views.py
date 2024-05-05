from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from .helpers import _checkAttributes, _createFile, _createProfiles, _sendFileResponse
from .helpers import __CreateSurvey, __DownloadSurvey

from .serializers import ShortSurveySerializer, SurveySerializer

import random, json, csv


@extend_schema(
    request=SurveySerializer,
    responses={
        201: OpenApiResponse(
            response="application/javascript",
            description="A JavaScript file containing the exported survey data.",
            examples=[
                OpenApiExample(
                    "SurveyJSFileExample",
                    summary="Exported Survey JS File",
                    description="A JavaScript file stream named survey.js containing the exported survey data.",
                    value={
                        "content_type": "application/javascript",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="{filename}"'
                        },
                    },
                )
            ],
        ),
        400: OpenApiResponse(
            description="An error response indicating that the request was invalid.",
        ),
    },
    description="Export survey to JS. Creates a file on the server and returns it to the user",
    summary='Export Survey Data as JavaScript File',
    methods=['POST'],
)
@api_view(["POST"])
def export_js(request):
    return _sendFileResponse(_createFile(request))


@extend_schema(
    request=ShortSurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="Preview of survey generated",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewSuccess",
                    description="A successful preview of survey answers.",
                    value={
                        "attributes": ["attribute1", "attribute2"],
                        "previews": [
                            ["a1n1", "a2n1"],
                            ["a1n1", "a2n2"],
                        ],
                    },
                    response_only=True,
                    status_codes=[str(status.HTTP_201_CREATED)],
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Bad Request, no survey data or invalid data provided",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewFailEmpty",
                    description="The survey data provided is empty.",
                    value={"message": "Survey is empty."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
                OpenApiExample(
                    name="SurveyPreviewFailInvalid",
                    description="The survey data provided is invalid.",
                    value={"message": "Invalid survey data."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
            ],
        ),
    },
    description="Generates a preview of survey answers based on provided attributes",
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
            return Response({"Error": "Cannot export to JavaScript. Some attributes have no levels."}, status=status.HTTP_400_BAD_REQUEST)
        
        answer = {"attributes": [], "previews": []}
        answer["previews"] = _createProfiles(profiles, attributes, restrictions, cross_restrictions, False)
        answer["attributes"] = [attribute["name"] for attribute in attributes]
        return Response(answer, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=400)


@extend_schema(
    request=ShortSurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response="text/csv",
            description="A CSV file containing the preview of survey data.",
            examples=[
                OpenApiExample(
                    name="PreviewCSVFileExample",
                    summary="Exported Preview CSV File",
                    description="A CSV file stream containing the preview of survey data.",
                    value={
                        "content_type": "text/csv",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="preview.csv"'
                        },
                    },
                    response_only=True,
                    status_codes=[str(status.HTTP_201_CREATED)],
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Bad Request, no survey data or invalid data provided",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewFailEmpty",
                    description="The survey data provided is empty.",
                    value={"message": "Survey is empty."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
                OpenApiExample(
                    name="SurveyPreviewFailInvalid",
                    description="The survey data provided is invalid.",
                    value={"message": "Invalid survey data."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
            ],
        ),
    },
    description="Generates and sends a CSV file based on provided attributes.",
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

        #To calculate the total number of combinations
        #levels_per_attribute = [len(attribute['levels']) for attribute in attributes]
        #profiles_per_attribute = [profiles for _ in attributes]
        if any(not attribute["levels"] for attribute in attributes):
            return Response({"Error": "Cannot export to JavaScript. Some attributes have no levels."}, status=status.HTTP_400_BAD_REQUEST)

        with open("profiles.csv", "w") as file:
            writer = csv.writer(file)
                
            header = []
            for i in range(1, len(attributes) + 1):
                for j in range(1, profiles + 2):
                    if j == 1:
                        header.append(f'ATT{i}')
                    else:
                        header.append(f'ATT{i}P{j-1}')
            writer.writerow(header)
            
            for i in range(csv_lines):
                profiles_list = _createProfiles(profiles, attributes, restrictions, cross_restrictions, True)
                rearrenged_profiles = []
                for i in range(len(attributes)):
                    rearrenged_profiles.append(profiles_list[0][i * 2])
                    for j in range(profiles):
                        rearrenged_profiles.append(profiles_list[j][i * 2 + 1])
                writer.writerow(rearrenged_profiles)   
        return _sendFileResponse("profiles.csv")
    else:
        return Response(serializer.errors, status=400)


'''''''''''''''''''''''''''''''''''''''''''''
''''''''''''QUALTRICS LOGIC''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''

@extend_schema(
    request=SurveySerializer,
    responses={
        201: OpenApiResponse(
            response="application/octet-stream",
            description="Creating Qualtrics survey and exporting QSF file",
            examples=[
                OpenApiExample(
                    name="CreateQualtricsExample",
                    description="Successful creation of Qualtrics survey and export of survey QSF",
                    value={
                        "content_type": "application/octet-stream",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="{filename}"'
                        }             
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            response="application/octet-stream",
            description="Error in creating Qualtrics survey and exporting QSF file",
            examples=[
                OpenApiExample(
                    name="CreateQualtricsErrorExample",
                    summary="Bad Request Response",
                    description="This response is returned when request to create Qualtrics survey and export QSF file is invalid",
                    value={
                        "error": "Invalid data provided.",
                        "details": "Incomplete survey data"
                    },
                )
            ]
        )
}, 
    description="Creating Qualtrics survey and exporting QSF file",
)
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def create_qualtrics(request):
    attributes = request.data.get("attributes", [])
    filename = request.data.get("filename", "export survey")
    profiles = request.data.get("profiles", 2)
    tasks = request.data.get("tasks", 5)
    duplicates = request.data.get("duplicates", [2,4])
    repeatFlip = request.data.get("repeatFlip", 1)
    doubleQ = request.data.get("doubleQ", False)
    resp = _checkAttributes(attributes)
    if resp:
        return resp
    jsname = _createFile(request)
    js_py = json.dumps(request.data)
    with open(jsname, "r", encoding="utf-8") as file_js:
        js_text = file_js.read()
    js_text = "Qualtrics.SurveyEngine.addOnload(function(){" + js_text
    js_text += "\n"
    js_text += "});\nQualtrics.SurveyEngine.addOnReady(function(){\
               \n/*Place your JavaScript here to run when the page is fully displayed*/\
                });\nQualtrics.SurveyEngine.addOnUnload(function()\
                {\n/*Place your JavaScript here to run when the page is unloaded*/});"
    js_text = "//" + js_py + "\n"+ js_text
    user_token = "Vy99DuC4A57FSg4tzvoejFdE0sDgaBH8cAouYF6h"  # FIGURE OUT BETTER WAY TO STORE THIS
    created = __CreateSurvey(
        filename, user_token, tasks, len(attributes), profiles, "", js_text, duplicates, repeatFlip, doubleQ
    )
    
    __DownloadSurvey(created, user_token, doubleQ)
    return _sendFileResponse("survey.qsf")


@extend_schema(
    request=None,
    responses={
        201: OpenApiResponse(
            response="application/octet-stream",
            description="Reversing QSF File into Attribute JSON",
            examples=[
                OpenApiExample(
                    name="ReverseQualtricsExample",
                    description="Successful Reversing QSF File into Attribute JSON",
                    value={
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
                        "restrictions" : ["att1 == b || att1 == a then att2 == d"]   

                    }
                )
            ]
        ),
        400: OpenApiResponse(
            response="application/octet-stream",
            description="Error in Reversing QSF File into Attribute JSON",
            examples=[
                OpenApiExample(
                    name="ReverseQualtricsErrorExample",
                    summary="Bad Request Response",
                    description="This response is returned when request to reverse QSF File is unsuccessful",
                    value={
                        "error": "Invalid QSF provided.",
                        "details": "QSF is invalid. Make sure QSF from survey created from projoint is used."
                    },
                )
            ]
        )
}, 
    description="Reversing QSF File into Attribute JSON",
)
@api_view(["POST"])
def qsf_to_attributes(request):
    qsf_data = json.loads(request)
    questions = qsf_data.get("SurveyElements")
    flag = 1
    for i in questions:
        if i.get("PrimaryAttribute") == "QID1":
            payload = i.get("Payload", {})
            js = payload.get("QuestionJS")
            attribute_comment = js.split("\n")[0]
            if "\\" in attribute_comment:
                attribute_comment.replace("\\","")
                attribute_data = json.loads(attribute_comment)
                flag = 0
            break
    if flag: # If QSF invalid, will return empty json
        attribute_data = {}
    return attribute_data

@extend_schema(
    request=ShortSurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response="text/csv",
            description="A CSV file containing the preview of survey data.",
            examples=[
                OpenApiExample(
                    name="PreviewCSVFileExample",
                    summary="Exported Preview CSV File (No duplicates)",
                    description="A CSV file stream containing the preview of survey data of all possible combinations.",
                    value={
                        "content_type": "text/csv",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="preview.csv"'
                        },
                    },
                    response_only=True,
                    status_codes=[str(status.HTTP_201_CREATED)],
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Bad Request, no survey data or invalid data provided",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewFailEmpty",
                    description="The survey data provided is empty.",
                    value={"message": "Survey is empty."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
                OpenApiExample(
                    name="SurveyPreviewFailInvalid",
                    description="The survey data provided is invalid.",
                    value={"message": "Invalid survey data."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
            ],
        ),
    },
    description="Generates and sends a CSV file of profile combinations based on provided attributes.",
)
@api_view(["POST"])
def noDuplicate_csv(request):
    try:
        CSV_FILES_NUM = 500
        attributes = request.data.get("attributes")
        restrictions = request.data.get("restrictions", [])
        profiles = request.data.get("profiles", 2)

        #To calculate the total number of combinations
        levels_per_attribute = [len(attribute['levels']) for attribute in attributes]
        profiles_per_attribute = [profiles for _ in attributes]
        
        
        header = []
        for i in range(1, len(attributes) + 1):
            for j in range(1, profiles + 2):
                if j == 1:
                    header.append(f'ATT{i}')
                else:
                    header.append(f'ATT{i}P{j-1}')
        previews = []
        previews.append(header)

        rows = []
        while len(rows) < CSV_FILES_NUM:
            row = []
            for attribute in attributes:
                att_name = attribute['name']
                row.append(att_name)
                
                randomized_levels = [random.choice(attribute['levels'])['name'] for _ in range(profiles + 1)]
                row.extend(randomized_levels)
            rows.append(row)

        previews.extend(rows)

        with open("unique_profiles.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows(previews)
        return _sendFileResponse("profiles.csv")
        #response = HttpResponse(content_type="text/csv", status=status.HTTP_201_CREATED)
        #response["Content-Disposition"] = 'attachment; filename="survey.csv"'

    except:
        return Response(
            {"message": "Invalid survey data."},
            status=status.HTTP_400_BAD_REQUEST,
        )