from datetime import timedelta

import cv2
from django.core.files.storage import storages
from django.db import models
from django_countries.fields import CountryField
from django_prometheus.models import ExportModelOperationsMixin
from mutagen import File as MutagenFile
from pictures.models import PictureField
from slugify import slugify


def _upload_videos_to(instance, filename) -> str:
    return f"videos/{instance.slug}/{filename}"


def _upload_images_to(instance, filename) -> str:
    return f"images/{instance.slug}/{filename}"


def _upload_audio_to(instance, filename) -> str:
    return f"audio/{instance.slug}/{filename}"


def _get_public_media_storage() -> storages:
    return storages["public"]


class _CommonDateTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=("-created", "-updated")),
        ]


class _CommonItemInfoModel(_CommonDateTimeModel):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True, null=False)
    slug = models.SlugField(max_length=255, blank=True, unique=True, null=False, default="")
    description = models.CharField(verbose_name="Описание", default=None, null=True, blank=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=("name", "-created", "-updated")),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)

        if not self.description:
            self.description = None

        super().save(*args, **kwargs)


class Images(_CommonItemInfoModel):
    image = PictureField(
        default=None,
        verbose_name="Ссылка на изображение",
        upload_to=_upload_images_to,
        storage=_get_public_media_storage,
        width_field="image_width",
        height_field="image_height",
    )
    image_width = models.PositiveIntegerField(
        editable=False,
        null=True,
        blank=True,
        verbose_name="Ширина изображения",
    )
    image_height = models.PositiveIntegerField(
        editable=False,
        null=True,
        blank=True,
        verbose_name="Высота изображения",
    )


class Audio(_CommonItemInfoModel):
    transcription = models.TextField(verbose_name="Текст песни", null=True, blank=True)
    duration = models.DurationField(verbose_name="Длительность", null=True, blank=True)
    audio = models.FileField(
        null=False,
        verbose_name="Ссылка на аудио",
        upload_to=_upload_audio_to,
        storage=_get_public_media_storage,
    )

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        if self.audio:
            audio_file = MutagenFile(self.audio)
            duration_seconds = audio_file.info.length

            self.duration = timedelta(seconds=duration_seconds)
            Audio.objects.filter(pk=self.pk).update(duration=self.duration)


class Video(_CommonItemInfoModel):
    duration = models.DurationField(verbose_name="Длительность", null=True, blank=True)
    video = models.FileField(
        null=False,
        verbose_name="Ссылка на видео",
        upload_to=_upload_videos_to,
        storage=_get_public_media_storage,
    )

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        if self.video:
            video = cv2.VideoCapture(self.video.url)
            if not video.isOpened():
                raise ValueError("Could not open video")

            fps = video.get(cv2.CAP_PROP_FPS)
            frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frames / fps if fps else 0
            video.release()

            self.duration = timedelta(seconds=duration)
            Video.objects.filter(pk=self.pk).update(duration=self.duration)


class Genres(ExportModelOperationsMixin("genres"), _CommonItemInfoModel):
    cover_image = models.OneToOneField(Images, verbose_name="Изображение", on_delete=models.CASCADE, null=True)


class Labels(ExportModelOperationsMixin("labels"), _CommonItemInfoModel):
    cover_image = models.OneToOneField(Images, verbose_name="Изображение", on_delete=models.CASCADE, null=True)


class Artists(ExportModelOperationsMixin("artist"), _CommonItemInfoModel):
    label = models.ForeignKey(Labels, verbose_name="Лейбл", on_delete=models.CASCADE)
    bio = models.TextField(verbose_name="Биография")
    avatar = models.ForeignKey(Images, verbose_name="Изображение", on_delete=models.CASCADE, null=True)
    birth_date = models.DateField(verbose_name="Дата рождения")
    country = CountryField(verbose_name="Страна", default="RU")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")


class Albums(ExportModelOperationsMixin("albums"), _CommonItemInfoModel):
    labels = models.ManyToManyField(Labels, verbose_name="Лейблы")
    cover_image = models.ForeignKey(Images, verbose_name="Изображение", on_delete=models.CASCADE)
    release_date = models.DateField(verbose_name="Дата выхода")
    artists = models.ManyToManyField(Artists, verbose_name="Исполнители")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")


class Tracks(ExportModelOperationsMixin("tracks"), _CommonItemInfoModel):
    album = models.ForeignKey(Albums, verbose_name="Альбом", on_delete=models.CASCADE)
    label = models.OneToOneField(Labels, verbose_name="Лейбл", on_delete=models.CASCADE)
    cover_image = models.ForeignKey(Images, verbose_name="Изображение", on_delete=models.CASCADE)
    track = models.OneToOneField(Audio, verbose_name="Трек", on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artists, verbose_name="Исполнители")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")
