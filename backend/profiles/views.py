from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from .serializers import LoginSerializer, TokenSerializer, ProfileSerializer

from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    request=ProfileSerializer,
    responses={201: ProfileSerializer},
    methods=["POST"],
    description="Register a new user.",
)
@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiExample(
            name="Successful Login Example",
            description="Response with auth token for a successful login",
            value={"token": "1234567890abcdef"},
            response_only=True,
            status_codes=["200"],
        ),
        401: OpenApiExample(
            name="Unauthorized Login Example",
            description="Response for failed login due to bad credentials",
            value={"detail": "Invalid credentials"},
            response_only=True,
            status_codes=["401"],
        ),
        400: OpenApiExample(
            name="Bad Request Login Example",
            description="Response for a login attempt with bad data formatting",
            value={"username": ["This field may not be blank."]},
            response_only=True,
            status_codes=["400"],
        ),
    },
    methods=["POST"],
    description="Endpoint for user login. Returns a token upon successful authentication.",
)
@api_view(["POST"])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(TokenSerializer(token).data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={
        200: OpenApiExample(
            "Successful Logout",
            summary="Successful Logout Example",
            description="This response indicates that the user has been successfully logged out.",
            value={"message": "Successfully logged out."},
            response_only=True,
            status_codes=["200"],
        ),
        401: OpenApiExample(
            "Unauthorized",
            summary="Unauthorized Logout Attempt",
            description="This response indicates that the request was not authorized, perhaps due to an invalid or missing token.",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
            status_codes=["401"],
        ),
        500: OpenApiExample(
            "Server Error",
            summary="Internal Server Error Example",
            description="This response indicates that there was an internal server error while processing the logout request.",
            value={"error": "Internal Server Error"},
            response_only=True,
            status_codes=["500"],
        ),
    },
    request=None,
    methods=["POST"],
    description="Logs out a user by deleting their authentication token. Requires authentication.",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
