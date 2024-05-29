import os

import markdown
from django.conf import settings
from django.http import HttpResponse
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Documentation
from .serializer import DocumentationSerializer

# def _save_docs():
#     Documentation.objects.create(
#             identifier='example',
#             description='Example Document',
#             markdown_file=os.path.join(settings.BASE_DIR, '../docs', 'example.md')
#         )
#     Documentation.objects.create(
#             identifier='tutorial',
#             description='Tutorial Document',
#             markdown_file=os.path.join(settings.BASE_DIR, '../docs', '00_tutorial.md')
#         )
#     Documentation.objects.create(
#             identifier='settings',
#             description='Settings Document',
#             markdown_file=os.path.join(settings.BASE_DIR, '../docs', '01_settings.md')
#         )


@extend_schema(
    summary="Get a documentation file",
    request=DocumentationSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="HTML content of the requested document file.",
            response="text/html",
            examples=[
                OpenApiExample(
                    name="Example Document",
                    description="An example document",
                    value="<h1>Example Document</h1>\n<p>This is an example document content.</p>\n",
                    status_codes=[status.HTTP_201_CREATED],
                )
            ]
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description="Document not found."
        ),
    },
    description="Returns a markdown page of the requested identifier",
    tags=['Documentation']
)
@api_view(['GET'])
def get_docs(request, identifier):
    try:
        document = Documentation.objects.get(identifier=identifier)
        with open(document.markdown_file, 'r') as file:
            text = file.read()
            html = markdown.markdown(text)
        return HttpResponse(html, content_type='text/html')
    except Documentation.DoesNotExist:
        return HttpResponse('Document not found', status=404)


@extend_schema(
    summary="List all documentation files",
    description="Returns a list of all Markdown files available in the documentation directory.",
    request=None,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="List of all Markdown files in the documentation directory.",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="List of Markdown files",
                    description="List of all Markdown files in the documentation directory.",
                    value=["example.md", "tutorial.md", "settings.md"],
                    status_codes=[status.HTTP_200_OK],
                )
            ]
        ),
    },
    tags=['Documentation']
)
@api_view(['GET'])
def list_docs(request):
    docs_path = os.path.join(settings.BASE_DIR, '../docs')
    markdown_files = [f for f in os.listdir(docs_path) if f.endswith('.md')]
    return Response(markdown_files)
