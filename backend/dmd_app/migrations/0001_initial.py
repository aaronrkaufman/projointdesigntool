# Generated by Django 4.2.7 on 2024-03-27 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MarkdownContent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("content", models.TextField()),
                ("slug", models.SlugField(blank=True)),
            ],
            options={
                "verbose_name_plural": "Pages",
            },
        ),
    ]
