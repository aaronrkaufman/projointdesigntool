from django.shortcuts import render
from django.http import HttpResponse
import markdown
from .models import Tooltip

def tooltip(request, identifier):
    try:
        tooltip = Tooltip.objects.get(identifier=identifier)
        with open(tooltip.markdown_file, 'r') as file:
            text = file.read()
            html = markdown.markdown(text)
        return HttpResponse(html, content_type='text/html')
    except Tooltip.DoesNotExist:
        return HttpResponse('Tooltip not found', status=404)
