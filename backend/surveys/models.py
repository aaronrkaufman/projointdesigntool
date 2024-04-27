from django.db import models
from django.core.validators import MinValueValidator

class Survey(models.Model):
    attributes = models.JSONField()

    constraints = models.JSONField(blank=True, default=list)
    restrictions = models.JSONField(blank=True, default=list)
    cross_restrictions = models.JSONField(blank=True, default=list)
    advanced = models.JSONField(blank=True, default=dict)
    filename = models.CharField(max_length=255, default='survey.js')
    profiles = models.IntegerField(validators=[MinValueValidator(2)], default=2)
    tasks = models.IntegerField(validators=[MinValueValidator(1)], default=5)
    randomize = models.BooleanField(default=False)
    repeat_task = models.BooleanField(default=False)
    random = models.BooleanField(default=False)
    noFlip = models.BooleanField(default=False)

    # duplicates is a tuple of two numbers, which can be represented by two separate IntegerFields
    duplicate_first = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    duplicate_second = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

