# Generated by Django 5.1.5 on 2025-01-25 21:54

import django.db.models.deletion
import django_enum.fields
import django_prometheus.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("music", "0011_remove_artists_music_artists_gender_artistgender_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Releases",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="Время создания")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="Время обновления")),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, default="", max_length=255, unique=True)),
                ("description", models.CharField(blank=True, default=None, null=True, verbose_name="Описание")),
                ("release_date", models.DateField(verbose_name="Дата выхода")),
                (
                    "release_type",
                    django_enum.fields.EnumCharField(
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
                        default="album",
                        max_length=11,
                        verbose_name="Тип релиза",
                    ),
                ),
                (
                    "status",
                    django_enum.fields.EnumCharField(
                        choices=[
                            ("active", "Активный"),
                            ("inactive", "Неактивный"),
                            ("deleted", "Удален"),
                            ("moderation", "На модерации"),
                        ],
                        default="moderation",
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(django_prometheus.models.ExportModelOperationsMixin("releases"), models.Model),
        ),
        migrations.RemoveField(
            model_name="albums",
            name="artists",
        ),
        migrations.RemoveField(
            model_name="albums",
            name="cover_image",
        ),
        migrations.RemoveField(
            model_name="albums",
            name="genres",
        ),
        migrations.RemoveField(
            model_name="albums",
            name="labels",
        ),
        migrations.RemoveConstraint(
            model_name="tracks",
            name="music_Tracks_status_TrackStatus",
        ),
        migrations.AlterField(
            model_name="tracks",
            name="status",
            field=django_enum.fields.EnumCharField(
                choices=[
                    ("active", "Активный"),
                    ("inactive", "Неактивный"),
                    ("deleted", "Удален"),
                    ("moderation", "На модерации"),
                ],
                default="moderation",
                max_length=10,
                verbose_name="Статус",
            ),
        ),
        migrations.AddField(
            model_name="releases",
            name="artists",
            field=models.ManyToManyField(blank=True, to="music.artists", verbose_name="Исполнители"),
        ),
        migrations.AddField(
            model_name="releases",
            name="cover_image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="music.images", verbose_name="Изображение"
            ),
        ),
        migrations.AddField(
            model_name="releases",
            name="genres",
            field=models.ManyToManyField(blank=True, to="music.genres", verbose_name="Жанры"),
        ),
        migrations.AddField(
            model_name="releases",
            name="labels",
            field=models.ManyToManyField(blank=True, to="music.labels", verbose_name="Лейблы"),
        ),
        migrations.AlterField(
            model_name="tracks",
            name="album",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="music.releases", verbose_name="Альбом"
            ),
        ),
        migrations.AddConstraint(
            model_name="tracks",
            constraint=models.CheckConstraint(
                condition=models.Q(("status__in", ["active", "inactive", "deleted", "moderation"])),
                name="music_Tracks_status_Statuses",
            ),
        ),
        migrations.AddIndex(
            model_name="releases",
            index=models.Index(fields=["name", "-created", "-updated"], name="music_relea_name_399237_idx"),
        ),
        migrations.AddConstraint(
            model_name="releases",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    (
                        "release_type__in",
                        [
                            "album",
                            "mini_album",
                            "single",
                            "maxi_single",
                            "podcast",
                            "book",
                            "compilation",
                            "reissue",
                            "remix",
                            "live",
                            "indefinite",
                        ],
                    )
                ),
                name="music_Releases_release_type_TypesOfReleases",
            ),
        ),
        migrations.AddConstraint(
            model_name="releases",
            constraint=models.CheckConstraint(
                condition=models.Q(("status__in", ["active", "inactive", "deleted", "moderation"])),
                name="music_Releases_status_Statuses",
            ),
        ),
        migrations.DeleteModel(
            name="Albums",
        ),
    ]
