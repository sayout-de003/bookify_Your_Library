# Generated by Django 5.1 on 2024-08-21 18:52

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="creativework",
            name="category",
            field=models.CharField(
                choices=[
                    ("painting", "Painting"),
                    ("dancing", "Dancing"),
                    ("article", "Article"),
                    ("research", "Research Paper"),
                ],
                default="article",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="creativework",
            name="content",
            field=models.FileField(
                default="creative_works/placeholder.jpg", upload_to="creative_works/"
            ),
        ),
        migrations.AddField(
            model_name="subscription",
            name="subscription_date",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="creativework",
            name="created_date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="creativework",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="library.creativework",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
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
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="library.creativework",
                    ),
                ),
            ],
            options={
                "unique_together": {("work", "user")},
            },
        ),
    ]
