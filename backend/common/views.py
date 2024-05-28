import os
from django.http import HttpResponse
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import api_view
import markdown
from .models import Documentation

@api_view(['GET'])
def get_docs(request, identifier):
    try:
        tooltip = Documentation.objects.get(identifier=identifier)
        with open(tooltip.markdown_file, 'r') as file:
            text = file.read()
            html = markdown.markdown(text)
        return HttpResponse(html, content_type='text/html')
    except Documentation.DoesNotExist:
        return HttpResponse('Tooltip not found', status=404)


@api_view(['GET'])
def list_docs(request):
    docs_path = os.path.join(settings.BASE_DIR, '../docs')
    markdown_files = [f for f in os.listdir(docs_path) if f.endswith('.md')]
    return Response(markdown_files)