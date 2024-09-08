from django.db import models
from slugify import slugify


class _CommonDateTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=('-created', '-updated')),
        ]


class _CommonItemInfoModel(_CommonDateTimeModel):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True, null=False)
    slug = models.SlugField(max_length=255, blank=True, unique=True, null=False)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=('name', '-created', '-updated')),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Genres(_CommonItemInfoModel):
    description = models.CharField(verbose_name="Описание")


class Labels(_CommonItemInfoModel):
    description = models.CharField(verbose_name="Описание")
    cover_image = models.ImageField(verbose_name="Ссылка на изображение")


class Artists(_CommonItemInfoModel):
    description = models.CharField(verbose_name="Описание")
    label = models.ForeignKey(Labels, verbose_name="Лейбл", on_delete=models.CASCADE)
    bio = models.TextField(verbose_name="Биография")
    avatar_url = models.ImageField(verbose_name="Ссылка на аватар")
    birth_date = models.DateField(verbose_name="Дата рождения")
    country = models.CharField(verbose_name="Страна")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")


class Albums(_CommonItemInfoModel):
    labels = models.ManyToManyField(Labels, verbose_name="Лейблы")
    cover_image = models.ImageField(verbose_name="Ссылка на изображение")
    release_date = models.DateField(verbose_name="Дата выхода")
    artists = models.ManyToManyField(Artists, verbose_name="Исполнители")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")


class Tracks(_CommonItemInfoModel):
    album = models.ForeignKey(Albums, verbose_name="Альбом", on_delete=models.CASCADE)
    label = models.OneToOneField(Labels, verbose_name="Лейбл", on_delete=models.CASCADE)
    cover_image = models.ImageField(verbose_name="Ссылка на изображение")
    track = models.FileField(verbose_name="Ссылка на трек")
    artists = models.ManyToManyField(Artists, verbose_name="Исполнители")
    genres = models.ManyToManyField(Genres, verbose_name="Жанры")
    duration = models.DurationField(verbose_name="Длительность")
