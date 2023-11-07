from django.db import models
from django.db.models import JSONField
from profiles.models import Profile


class Survey(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    attributes = JSONField(default=dict)
    constraints = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Survey for {self.profile}"
