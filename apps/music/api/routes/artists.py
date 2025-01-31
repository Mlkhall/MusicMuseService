from http import HTTPStatus

from pydantic import PositiveInt
from django.shortcuts import get_object_or_404, get_list_or_404
from ninja import Router, UploadedFile, File, Form, Query
from loguru import logger
from django.db import transaction, IntegrityError
from ninja.errors import HttpError
from django.core.paginator import Paginator
from apps.music.api.dto.artists import AddNewArtistIn, AddNewArtistOut, UpdateArtistOut, GetFilteredArtistOut, \
    GetFilteredArtistIn, GetArtistPagesOut, GetArtistPagesItemOut
from apps.music.api.docs import Tags
from apps.music.models import Images, Artists, Labels, Genres

router_v1 = Router(tags=[Tags.artists])


@router_v1.post(
    path="/",
    summary="Добавить нового исполнителя",
    response=AddNewArtistOut,
)
def add_new_artist(
    request,
    payload: Form[AddNewArtistIn],
    avatar: UploadedFile = File(None),
):
    logger.info(request)

    label = get_object_or_404(Labels, id=payload.label_id) if payload.label_id else None
    genres = get_list_or_404(Genres, id__in=payload.genres_ids) if payload.genres_ids else None

    with transaction.atomic():
        new_avatar = None

        if avatar:
            new_avatar, was_avatar_created = Images.objects.get_or_create(
                name=avatar.name,
                defaults={"name": avatar.name, "image": avatar},
            )

            if was_avatar_created:
                logger.success(f"Изображение '{new_avatar.name}' успешно загружено")

        try:
            new_artist = Artists.objects.create(
                name=payload.name,
                description=payload.description,
                avatar=new_avatar,
                birth_date=payload.birth_date,
                country=payload.country,
                label=label,
                bio=payload.bio,
                is_verified=payload.is_verified,
            )
        except IntegrityError as exc:
            logger.warning(exc)
            raise HttpError(
                status_code=HTTPStatus.CONFLICT,
                message=f"Исполнитель с именем '{payload.name}' уже существует",
            )

        if genres:
            new_artist.genres.set(genres)

        created_new_artist = AddNewArtistOut(
            id=new_artist.id,
            name=new_artist.name,
            description=new_artist.description,
            avatar=new_avatar.image if new_avatar else None,
            birth_date=new_artist.birth_date,
            country=new_artist.country.name,
            label=label.name if label else None,
            bio=new_artist.bio,
            is_verified=new_artist.is_verified,
            genres=tuple(genre.name for genre in new_artist.genres.all()),
            gender=new_artist.gender,
        )
        logger.success(f"Исполнитель '{payload.name}' успешно создан: {created_new_artist.dict()}")

        return created_new_artist


@router_v1.get(
    path="/filter/",
    summary="Получить исполнителя по фильтру",
    response=GetFilteredArtistOut,
)
def get_filtered_artist(request, artist_filter: GetFilteredArtistIn = Query(...)):
    logger.info(request)
    if not artist_filter.name and not artist_filter.pk:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    artists = Artists.objects.all()
    filtered_artist = artist_filter.filter(artists).first()
    if not filtered_artist:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=f"Исполнитель по фильтру {artist_filter.model_dump(mode='json')} не найден",
        )

    return GetFilteredArtistOut(
        id=filtered_artist.pk,
        name=filtered_artist.name,
        description=filtered_artist.description,
        avatar=filtered_artist.avatar.image if filtered_artist.avatar else None,
        birth_date=filtered_artist.birth_date,
        country=filtered_artist.country.name,
        label=filtered_artist.label.name if filtered_artist.label else None,
        bio=filtered_artist.bio,
        is_verified=filtered_artist.is_verified,
        genres=tuple(genre.name for genre in filtered_artist.genres.all()),
        gender=filtered_artist.gender,
    )


@router_v1.get(
    path="/pages/",
    summary="Получить страницы исполнителей",
    response=GetArtistPagesOut,
)
def get_artist_pages(request, page: PositiveInt = 1, size: PositiveInt = 10):
    logger.info(request)

    artist_list = Artists.objects.all()
    paginator = Paginator(object_list=artist_list, per_page=size)

    items = tuple(
        GetArtistPagesItemOut(
            id=artist.pk,
            name=artist.name,
            description=artist.description,
            avatar=artist.avatar.image if artist.avatar else None,
            birth_date=artist.birth_date,
            country=artist.country.name,
            label=artist.label.name if artist.label else None,
            bio=artist.bio,
            is_verified=artist.is_verified,
            genres=tuple(genre.name for genre in artist.genres.all()),
            gender=artist.gender,
        )
        for artist in paginator.get_page(number=page)
    )

    return GetArtistPagesOut(
        items=items,
        total=artist_list.count(),
        per_page=len(items),
    )


@router_v1.put(
    path="/{artist_id}/",
    summary="Обновить исполнителя",
    response=UpdateArtistOut,
)
def update_artist(
    request,
    artist_id: PositiveInt,
    payload: Form[AddNewArtistIn],
    avatar: UploadedFile = File(None),
):
    logger.info(request)

    artist = get_object_or_404(Artists, id=artist_id)

    label = get_object_or_404(Labels, id=payload.label_id) if payload.label_id else None
    genres = get_list_or_404(Genres, id__in=payload.genres_ids) if payload.genres_ids else None

    with transaction.atomic():
        new_avatar = None

        if avatar:
            new_avatar, was_avatar_created = Images.objects.update_or_create(
                name=avatar.name,
                defaults={"name": avatar.name, "image": avatar},
            )

            if was_avatar_created:
                logger.success(f"Изображение '{new_avatar.name}' успешно загружено")
            else:
                logger.success(f"Изображение '{new_avatar.name}' успешно обновлено")

        for filed_name, updated_value in payload.dict(exclude={"label_id", "genres_ids"}).items():
            if updated_value:
                setattr(artist, filed_name, updated_value)
                logger.success(f"Поле '{filed_name}' -> '{updated_value}' успешно обновлено")

        if new_avatar:
            artist.avatar = new_avatar

        if label:
            artist.label = label

        artist.save()

        if genres:
            artist.genres.set(genres)

        logger.success(f"Исполнитель '{artist.name}' успешно обновлен: {artist}")
        return UpdateArtistOut(
            id=artist.pk,
            name=artist.name,
            description=artist.description,
            avatar=artist.avatar.image if artist.avatar else None,
            birth_date=artist.birth_date,
            country=artist.country.name,
            label=artist.label.name if artist.label else None,
            bio=artist.bio,
            is_verified=artist.is_verified,
            genres=tuple(genre.name for genre in artist.genres.all()),
            gender=artist.gender,
        )
