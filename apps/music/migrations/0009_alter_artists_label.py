# Generated by Django 5.1.4 on 2024-12-30 01:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("music", "0008_artists_gender_artists_is_verified_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artists",
            name="label",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="music.labels", verbose_name="Лейбл"
            ),
        ),
    ]
