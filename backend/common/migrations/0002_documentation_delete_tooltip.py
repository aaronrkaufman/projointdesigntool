# Generated by Django 4.2.7 on 2024-05-28 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Documentation",
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
                ("identifier", models.CharField(max_length=100, unique=True)),
                ("description", models.CharField(max_length=255)),
                ("markdown_file", models.FilePathField(path="../../../docs")),
            ],
        ),
        migrations.DeleteModel(
            name="Tooltip",
        ),
    ]