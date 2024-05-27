from django.db import models

class Tooltip(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    markdown_file = models.FilePathField(path="../../../docs/tooltips")

    def __str__(self):
        return self.description
