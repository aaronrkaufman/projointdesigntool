'''
Unused views. No link of survey to profile yet.
'''

'''
@extend_schema(
    request=ShortSurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="Saves the survey to user's profile",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveySaveSuccess",
                    description="The survey has been successfully saved to the user's profile.",
                    value={"message": "Survey has been saved."},
                    response_only=True,
                    status_codes=[str(status.HTTP_201_CREATED)],
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Bad Request",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveySaveFail",
                    description="The survey data provided is invalid.",
                    value={"error": "Invalid data provided."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                )
            ],
        ),
    },
    description="Saves the survey to user's profile",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_user_survey(request):
    serializer = ShortSurveySerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Survey has been saved."}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="List of user's surveys",
            response=ShortSurveySerializer,
            examples=[
                OpenApiExample(
                    name="SurveyListExample",
                    description="Example of a user having multiple surveys.",
                    value=[
                        {
                            "id": 1,
                            "profile": 1,
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
                            ],
                            "constraints": [],
                        },
                    ],
                    response_only=True,
                    status_codes=[str(status.HTTP_200_OK)],
                )
            ],
        ),
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            description="No surveys found for the user",
            response=None,
            examples=[
                OpenApiExample(
                    name="NoSurveyExample",
                    description="Example of a user having no surveys.",
                    value={"message": "User has no surveys"},
                    response_only=True,
                    status_codes=[str(status.HTTP_204_NO_CONTENT)],
                )
            ],
        ),
    },
    description="Retrieves the list of surveys belonging to the user",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_user_surveys(request):
    surveys = Survey.objects.filter(profile=request.user)
    if surveys.exists():
        serializer = ShortSurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "User has no surveys"}, status=status.HTTP_204_NO_CONTENT
        )

'''