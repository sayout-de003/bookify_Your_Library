# Generated by Django 5.1 on 2024-08-23 10:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0019_alter_bookissue_due_date_alter_genre_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookissue",
            name="due_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 9, 6, 10, 8, 47, 607660, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="end_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 9, 22, 10, 8, 47, 609011, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
