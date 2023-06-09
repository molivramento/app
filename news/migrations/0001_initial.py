# Generated by Django 4.1.5 on 2023-03-22 10:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="News",
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
                ("title", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=100)),
                ("content", models.TextField()),
                ("pub_date", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("politics", "Politics"),
                            ("sports", "Sports"),
                            ("entertainment", "Entertainment"),
                            ("technology", "Technology"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
    ]
