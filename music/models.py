from django.db import models
from slugify import slugify
from django.core.files.storage import storages
from django_prometheus.models import ExportModelOperationsMixin


def _upload_videos_to(instance, filename) -> str:
    return f"videos/{instance.slug}/{filename}"


def _upload_images_to(instance, filename) -> str:
    return f"images/{instance.slug}/{filename}"


def _upload_albums_to(instance, filename) -> str:
    return f"albums/{instance.slug}/{filename}"


def _upload_labels_to(instance, filename) -> str:
    return f"labels/{instance.slug}/{filename}"


def _upload_genres_to(instance, filename) -> str:
    return f"genres/{instance.slug}/{filename}"


def _upload_tracks_to(instance, filename) -> str:
    return f"tracks/{instance.slug}/{filename}"


def _upload_artists_to(instance, filename) -> str:
    return f"artists/{instance.slug}/{filename}"


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
    name = models.CharField(
        max_length=255, verbose_name="Название", unique=True, null=False
    )
    slug = models.SlugField(
        max_length=255, blank=True, unique=True, null=False, default=""
    )
    description = models.CharField(
        verbose_name="Описание", default=None, null=True, blank=True
    )

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

        super().save(*args, **kwargs)


class GeneratedVideoContent(
    ExportModelOperationsMixin("gen_video"), _CommonDateTimeModel
):
    duration = models.DurationField(verbose_name="Длительность")
    video = models.FileField(
        null=False,
        verbose_name="Ссылка на сгенерированное видео",
        upload_to=_upload_videos_to,
        storage=_get_public_media_storage,
    )


class GeneratedImageContent(
    ExportModelOperationsMixin("gen_image"), _CommonDateTimeModel
):
    image = models.ImageField(
        null=False,
        verbose_name="Ссылка на сгенерированное изображение",
        upload_to=_upload_images_to,
        storage=_get_public_media_storage,
    )


class Genres(ExportModelOperationsMixin("genres"), _CommonItemInfoModel):
    image = models.ImageField(
        default=None,
        verbose_name="Ссылка на изображение жанра",
        upload_to=_upload_genres_to,
        storage=_get_public_media_storage,
    )


class Labels(ExportModelOperationsMixin("labels"), _CommonItemInfoModel):
    description = models.CharField(verbose_name="Описание", default=None)
    cover_image = models.ImageField(
        verbose_name="Ссылка на изображение",
        upload_to=_upload_labels_to,
        storage=_get_public_media_storage,
    )


class Artists(ExportModelOperationsMixin("artist"), _CommonItemInfoModel):
    description = models.CharField(verbose_name="Описание", default=None)
    label = models.ForeignKey(Labels, verbose_name="Лейбл", on_delete=models.CASCADE)
    bio = models.TextField(verbose_name="Биография")
    avatar_url = models.ImageField(
        verbose_name="Ссылка на аватар",
        upload_to=_upload_artists_to,
        storage=_get_public_media_storage,
    )
    birth_date = models.DateField(verbose_name="Дата рождения")
    country = models.CharField(verbose_name="Страна")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")


class Albums(ExportModelOperationsMixin("albums"), _CommonItemInfoModel):
    labels = models.ManyToManyField(Labels, verbose_name="Лейблы")
    cover_image = models.ImageField(
        verbose_name="Ссылка на изображение",
        upload_to=_upload_albums_to,
        storage=_get_public_media_storage,
    )
    release_date = models.DateField(verbose_name="Дата выхода")
    artists = models.ManyToManyField(Artists, verbose_name="Исполнители")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")


class Tracks(ExportModelOperationsMixin("tracks"), _CommonItemInfoModel):
    album = models.ForeignKey(Albums, verbose_name="Альбом", on_delete=models.CASCADE)
    label = models.OneToOneField(Labels, verbose_name="Лейбл", on_delete=models.CASCADE)
    cover_image = models.ImageField(
        verbose_name="Ссылка на изображение",
        upload_to=_upload_tracks_to,
        storage=_get_public_media_storage,
    )
    track = models.FileField(
        verbose_name="Ссылка на трек",
        upload_to=_upload_labels_to,
        storage=_get_public_media_storage,
    )
    artists = models.ManyToManyField(Artists, verbose_name="Исполнители")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")
    duration = models.DurationField(verbose_name="Длительность")
