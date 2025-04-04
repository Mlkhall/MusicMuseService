# Generated by Django 5.1.5 on 2025-02-03 19:42

import django_enum.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("music", "0019_alter_audio_audio_alter_images_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tracks",
            name="age_related_content",
            field=models.BooleanField(default=False, verbose_name="18+"),
        ),
        migrations.AddField(
            model_name="tracks",
            name="publication_time",
            field=models.TimeField(blank=True, null=True, verbose_name="Время публикации"),
        ),
        migrations.AddField(
            model_name="tracks",
            name="release_date",
            field=models.DateField(blank=True, null=True, verbose_name="Дата выхода"),
        ),
        migrations.AddField(
            model_name="tracks",
            name="track_type",
            field=django_enum.fields.EnumCharField(
                choices=[
                    ("non_music", "Не музыка"),
                    ("book", "Книга"),
                    ("podcast", "Подкаст"),
                    ("album", "Альбом"),
                    ("single", "Сингл"),
                    ("indefinite", "Неопределенный"),
                ],
                default="indefinite",
                max_length=10,
                null=True,
                verbose_name="Тип трека",
            ),
        ),
        migrations.AddConstraint(
            model_name="tracks",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("track_type__in", ["non_music", "book", "podcast", "album", "single", "indefinite"]),
                    ("track_type__isnull", True),
                    _connector="OR",
                ),
                name="music_Tracks_track_type_TypesOfTracks",
            ),
        ),
    ]
