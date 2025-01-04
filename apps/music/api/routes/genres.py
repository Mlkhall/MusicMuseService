from http import HTTPStatus
from django.shortcuts import get_object_or_404
from ninja import Router, File, Form, Query
from ninja.pagination import paginate, PageNumberPagination
from loguru import logger
from ninja.files import UploadedFile
from django.db import transaction
from ninja.errors import HttpError
from apps.music.api.schemas.genres import GenresSchema, GenreUpdateSchema, GenreCreateSchema, GenreFilterSchema, \
    FilteredGenreSchema
from apps.music.api.types import Tags
from apps.music.models import Genres, Images

router_v1 = Router(tags=[Tags.genres])


@router_v1.post(
    path="/",
    response=GenresSchema,
    summary="Добавить новый жанр",
)
def add_new_genre(
    request,
    payload: Form[GenreCreateSchema],
    cover_image: UploadedFile = File(None),
):
    logger.info(request)
    with transaction.atomic():
        new_cover_image = None
        if cover_image:
            new_cover_image = Images.objects.create(
                name=cover_image.name,
            )

        parent_genre = None
        if payload.parent_genre_id:
            parent_genre = get_object_or_404(Genres, id=payload.parent_genre_id)

        return Genres.objects.create(
            name=payload.name,
            description=payload.description,
            parent=parent_genre,
            cover_image=new_cover_image,
        )


@router_v1.get(
    path="/filter/",
    response=FilteredGenreSchema,
    summary="Получить жанр по фильтру",
)
def get_filtered_genre(request, genre_filter: GenreFilterSchema = Query(...)):
    logger.info(request)
    if not genre_filter.name and not genre_filter.pk:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    genres = Genres.objects.all()
    genre = genre_filter.filter(genres).first()
    return FilteredGenreSchema(
        pk=genre.pk,
        name=genre.name,
        slug=genre.slug,
        description=genre.description,
        parent_genre_id=genre.parent_id,
        image_cover=genre.cover_image.image if genre.cover_image else None,
        created_at=genre.created,
        updated_at=genre.updated,
    )


@router_v1.get(
    path="/pages/",
    response=list[GenresSchema],
    description="Получение всех музыкальных жанров постранично",
    summary="Получить страницы жанров"
)
@paginate(PageNumberPagination)
def get_genre_pages(request):
    logger.info(request)
    return Genres.objects.all()


@router_v1.put(
    path="/{genre_id}/",
    response=GenresSchema,
    description="Обновление музыкального жанра",
    summary="Обновить жанр",
)
def update_genre(request, genre_id: int, payload: GenreUpdateSchema):
    logger.info(request)

    genre = get_object_or_404(Genres, id=genre_id)
    for filed_name, updated_value in payload.dict().items():
        if updated_value:
            setattr(genre, filed_name, updated_value)

    genre.save()
    return genre
