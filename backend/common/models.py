from django.db import models

class Documentation(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    markdown_file = models.FilePathField(path="../../../docs")

    def __str__(self):
        return self.description
