# Generated by Django 5.1 on 2024-08-23 06:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0012_book_epub_file_book_unique_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="end_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 9, 22, 6, 47, 31, 648277, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
