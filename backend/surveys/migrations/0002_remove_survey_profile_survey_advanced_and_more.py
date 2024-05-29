# Generated by Django 4.2.7 on 2024-05-27 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="survey",
            name="profile",
        ),
        migrations.AddField(
            model_name="survey",
            name="advanced",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="survey",
            name="cross_restrictions",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="survey",
            name="csv_lines",
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name="survey",
            name="duplicate_first",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AddField(
            model_name="survey",
            name="duplicate_second",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AddField(
            model_name="survey",
            name="filename",
            field=models.CharField(default="survey.js", max_length=255),
        ),
        migrations.AddField(
            model_name="survey",
            name="noFlip",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="survey",
            name="profiles",
            field=models.IntegerField(
                default=2, validators=[django.core.validators.MinValueValidator(2)]
            ),
        ),
        migrations.AddField(
            model_name="survey",
            name="random",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="survey",
            name="randomize",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="survey",
            name="repeat_task",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="survey",
            name="restrictions",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="survey",
            name="tasks",
            field=models.IntegerField(
                default=5, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="survey",
            name="attributes",
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="survey",
            name="constraints",
            field=models.JSONField(blank=True, default=list),
        ),
    ]