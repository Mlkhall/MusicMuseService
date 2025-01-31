from http import HTTPStatus
from django.shortcuts import get_object_or_404
from ninja import Router, File, Form, Query
from ninja.pagination import paginate, PageNumberPagination
from loguru import logger
from ninja.files import UploadedFile
from pydantic import PositiveInt
from django.db import transaction, IntegrityError
from ninja.errors import HttpError
from apps.music.api.dto.genres import AddNewGenreIn, GetFilteredGenreIn, \
    GetFilteredGenreInOut, AddNewGenreOut, GetGenrePagesOut, UpdateGenreIn, UpdateGenreOut
from apps.music.api.docs import Tags
from apps.music.models import Genres, Images

router_v1 = Router(tags=[Tags.genres])


@router_v1.post(
    path="/",
    response=AddNewGenreOut,
    summary="Добавить новый жанр",
)
def add_new_genre(
    request,
    payload: Form[AddNewGenreIn],
    cover_image: UploadedFile = File(None),
):
    logger.info(request)
    with transaction.atomic():
        new_cover_image = None

        if cover_image:
            new_cover_image, was_cover_image_created = Images.objects.get_or_create(
                name=cover_image.name,
                defaults={"name": cover_image.name, "image": cover_image},
            )

            if was_cover_image_created:
                logger.success(f"Изображение '{new_cover_image.name}' успешно загружено")

        parent_genre = None
        if payload.parent_genre_id:
            parent_genre = get_object_or_404(Genres, id=payload.parent_genre_id)

        try:
            new_genre = Genres.objects.create(
                name=payload.name,
                description=payload.description,
                parent=parent_genre,
                cover_image=new_cover_image,
            )
        except IntegrityError as exc:
            logger.warning(exc)
            raise HttpError(
                status_code=HTTPStatus.CONFLICT,
                message=f"Жанр с именем '{payload.name}' уже существует",
            )

    return new_genre

@router_v1.get(
    path="/filter/",
    response=GetFilteredGenreInOut,
    summary="Получить жанр по фильтру",
)
def get_filtered_genre(request, genre_filter: GetFilteredGenreIn = Query(...)):
    logger.info(request)
    if not genre_filter.name and not genre_filter.pk:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    genres = Genres.objects.all()
    genre = genre_filter.filter(genres).first()
    if not genre:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=f"Жанр для {genre_filter.dict()} не найден",
        )

    return GetFilteredGenreInOut(
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
    response=list[GetGenrePagesOut],
    description="Получение всех музыкальных жанров постранично",
    summary="Получить страницы жанров"
)
@paginate(PageNumberPagination)
def get_genre_pages(request):
    logger.info(request)
    return Genres.objects.all()


@router_v1.put(
    path="/{genre_id}/",
    response=UpdateGenreOut,
    description="Обновление музыкального жанра",
    summary="Обновить жанр",
)
def update_genre(
    request,
    genre_id: PositiveInt,
    payload: Form[UpdateGenreIn],
    cover_image: UploadedFile = File(None),
):
    logger.info(request)

    genre = get_object_or_404(Genres, id=genre_id)
    with transaction.atomic():
        for filed_name, updated_value in payload.dict().items():
            if updated_value:
                setattr(genre, filed_name, updated_value)

        if cover_image:
            updated_image, was_image_created = Images.objects.update_or_create(
                name=cover_image.name,
                defaults={"name": cover_image.name, "image": cover_image},
            )

            if was_image_created:
                logger.success(f"Изображение '{updated_image.name}' успешно загружено")
            else:
                logger.success(f"Изображение '{updated_image.name}' успешно обновлено")

            genre.cover_image = updated_image

        genre.save()
    return genre
