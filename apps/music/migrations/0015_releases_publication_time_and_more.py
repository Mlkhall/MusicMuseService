# Generated by Django 5.1.5 on 2025-01-26 19:28

import django_enum.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("music", "0014_alter_genres_cover_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="releases",
            name="publication_time",
            field=models.TimeField(blank=True, null=True, verbose_name="Время публикации"),
        ),
        migrations.AlterField(
            model_name="releases",
            name="release_type",
            field=django_enum.fields.EnumCharField(
                choices=[
                    ("album", "Альбом"),
                    ("mini_album", "Мини-альбом"),
                    ("single", "Сингл"),
                    ("maxi_single", "Макси-сингл"),
                    ("podcast", "Подкаст"),
                    ("book", "Книга"),
                    ("compilation", "Сборник"),
                    ("reissue", "Переиздание"),
                    ("remix", "Ремикс"),
                    ("live", "Концерт"),
                    ("indefinite", "Неопределенный"),
                ],
                default="indefinite",
                max_length=11,
                verbose_name="Тип релиза",
            ),
        ),
    ]
