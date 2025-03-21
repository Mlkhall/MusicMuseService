# Generated by Django 5.1.3 on 2024-11-10 18:47

import pictures.models
from django.db import migrations, models

import apps.music.models


class Migration(migrations.Migration):
    dependencies = [
        ("music", "0002_remove_artists_avatar_url_remove_tracks_duration_and_more_squashed_0004_alter_video_duration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="audio",
            name="audio",
            field=models.FileField(
                max_length=255,
                storage=apps.music.models._get_public_media_storage,
                upload_to=apps.music.models._upload_audio_to,
                verbose_name="Ссылка на аудио",
            ),
        ),
        migrations.AlterField(
            model_name="images",
            name="image",
            field=pictures.models.PictureField(
                aspect_ratios=[None],
                breakpoints={"l": 1200, "m": 992, "s": 768, "xl": 1400, "xs": 576},
                container_width=1200,
                default=None,
                file_types=["WEBP"],
                grid_columns=12,
                height_field="image_height",
                max_length=255,
                pixel_densities=[1, 2],
                storage=apps.music.models._get_public_media_storage,
                upload_to=apps.music.models._upload_images_to,
                verbose_name="Ссылка на изображение",
                width_field="image_width",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="video",
            field=models.FileField(
                max_length=255,
                storage=apps.music.models._get_public_media_storage,
                upload_to=apps.music.models._upload_videos_to,
                verbose_name="Ссылка на видео",
            ),
        ),
    ]
