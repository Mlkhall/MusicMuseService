from http import HTTPStatus

from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.shortcuts import get_list_or_404, get_object_or_404
from loguru import logger
from ninja import File, Form, Query, Router, UploadedFile
from ninja.errors import HttpError
from pydantic import PositiveInt

from apps.music.api.docs import Tags
from apps.music.api.dto.releases import (
    AddNewReleaseIn,
    AddNewReleaseOut,
    GetFilteredReleaseIn,
    GetFilteredReleaseOut,
    GetReleasePagesItemOut,
    GetReleasesPagesOut,
    UpdateReleaseIn,
    UpdateReleaseOut,
)
from apps.music.api.validators import validate_image_file
from apps.music.models import Artists, Genres, Images, Labels, Releases

router_v1 = Router(tags=[Tags.releases])


@router_v1.post(
    path="/",
    summary="Добавить новый релиз",
    response=AddNewReleaseOut,
)
def add_new_release(
    request,
    payload: Form[AddNewReleaseIn],
    cover_image: UploadedFile = File(None),
):
    logger.info(request)

    labels = get_list_or_404(Labels, id__in=payload.label_ids) if payload.label_ids else None
    artists = get_list_or_404(Artists, id__in=payload.artist_ids) if payload.artist_ids else None
    genres = get_list_or_404(Genres, id__in=payload.genre_ids) if payload.genre_ids else None

    with transaction.atomic():
        new_cover_image = None

        if cover_image:
            validate_image_file(cover_image)
            new_cover_image, was_cover_image_created = Images.objects.get_or_create(
                name=cover_image.name,
                defaults={"name": cover_image.name, "image": cover_image},
            )

            if was_cover_image_created:
                logger.success(f"Изображение '{new_cover_image.name}' успешно загружено")

        try:
            new_release = Releases.objects.create(
                name=payload.name,
                description=payload.description,
                release_date=payload.release_date,
                publication_time=payload.publication_time,
                status=payload.status,
                release_type=payload.release_type,
                cover_image=new_cover_image,
            )
        except IntegrityError as exc:
            logger.warning(exc)
            raise HttpError(
                status_code=HTTPStatus.CONFLICT,
                message=f"Релиз с именем '{payload.name}' уже существует",
            )

        if genres:
            new_release.genres.set(genres)

        if labels:
            new_release.labels.set(labels)

        if artists:
            new_release.artists.set(artists)

        return AddNewReleaseOut(
            pk=new_release.pk,
            name=new_release.name,
            description=new_release.description,
            cover_image=new_cover_image.image if new_cover_image else None,
            release_date=new_release.release_date,
            labels_names=tuple(new_release.labels.values_list("name", flat=True)),
            artists_names=tuple(new_release.artists.values_list("name", flat=True)),
            genres_names=tuple(new_release.genres.values_list("name", flat=True)),
            release_type=new_release.release_type,
            status=new_release.status,
            created=new_release.created,
            updated=new_release.updated,
        )


@router_v1.get(
    path="/filter/",
    summary="Получить релиз по фильтру",
    response=GetFilteredReleaseOut,
)
def get_filtered_release(request, release_filter: GetFilteredReleaseIn = Query(...)):
    logger.info(request)

    if not release_filter.name and not release_filter.pk:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    releases = Releases.objects.all()
    release = release_filter.filter(releases).first()
    if not release:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=f"Релиз для {release_filter.dict()} не найден",
        )

    return GetFilteredReleaseOut(
        pk=release.pk,
        name=release.name,
        description=release.description,
        cover_image=release.cover_image.image if release.cover_image else None,
        release_date=release.release_date,
        labels_names=tuple(release.labels.values_list("name", flat=True)),
        artists_names=tuple(release.artists.values_list("name", flat=True)),
        genres_names=tuple(release.genres.values_list("name", flat=True)),
        release_type=release.release_type,
        status=release.status,
        created=release.created,
        updated=release.updated,
    )


@router_v1.get(
    path="/pages/",
    response=GetReleasesPagesOut,
    description="Получение всех релизов постранично",
    summary="Получить страницы релизов",
)
def get_release_pages(request, page: PositiveInt = 1, size: PositiveInt = 10):
    logger.info(request)

    release_list = Releases.objects.all()
    paginator = Paginator(object_list=release_list, per_page=size)

    items = tuple(
        GetReleasePagesItemOut(
            pk=release.pk,
            name=release.name,
            description=release.description,
            cover_image=release.cover_image.image if release.cover_image else None,
            release_date=release.release_date,
            labels_names=tuple(release.labels.values_list("name", flat=True)),
            artists_names=tuple(release.artists.values_list("name", flat=True)),
            genres_names=tuple(release.genres.values_list("name", flat=True)),
            release_type=release.release_type,
            status=release.status,
            created=release.created,
            updated=release.updated,
        )
        for release in paginator.get_page(page)
    )

    return GetReleasesPagesOut(
        items=items,
        total=paginator.count,
        per_page=size,
    )


@router_v1.put(
    path="/{release_id}/",
    summary="Обновление релиза",
    description="Обновить релиз",
    response=UpdateReleaseOut,
)
def update_release(
    request,
    release_id: PositiveInt,
    payload: Form[UpdateReleaseIn],
    cover_image: UploadedFile = File(None),
):
    logger.info(request)

    release = get_object_or_404(Releases, id=release_id)

    labels = get_list_or_404(Labels, id__in=payload.label_ids) if payload.label_ids else None
    artists = get_list_or_404(Artists, id__in=payload.artist_ids) if payload.artist_ids else None
    genres = get_list_or_404(Genres, id__in=payload.genre_ids) if payload.genre_ids else None

    with transaction.atomic():
        for field_name, updated_value in payload.dict(exclude={"label_ids", "artist_ids", "genre_ids"}).items():
            if updated_value:
                setattr(release, field_name, updated_value)

        if cover_image:
            validate_image_file(cover_image)
            new_cover_image, was_cover_image_created = Images.objects.update_or_create(
                name=cover_image.name,
                defaults={"name": cover_image.name, "image": cover_image},
            )

            if was_cover_image_created:
                logger.success(f"Изображение '{new_cover_image.name}' успешно загружено")
            else:
                logger.success(f"Изображение '{new_cover_image.name}' успешно обновлено")

            release.cover_image = new_cover_image

        release.save()

        if genres:
            release.genres.set(genres)

        if labels:
            release.labels.set(labels)

        if artists:
            release.artists.set(artists)

        return UpdateReleaseOut(
            pk=release.pk,
            name=release.name,
            description=release.description,
            cover_image=release.cover_image.image if release.cover_image else None,
            release_date=release.release_date,
            labels_names=tuple(release.labels.values_list("name", flat=True)),
            artists_names=tuple(release.artists.values_list("name", flat=True)),
            genres_names=tuple(release.genres.values_list("name", flat=True)),
            release_type=release.release_type,
            status=release.status,
            created=release.created,
            updated=release.updated,
        )
