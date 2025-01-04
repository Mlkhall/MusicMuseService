from django.shortcuts import get_object_or_404, get_list_or_404
from ninja import Router, UploadedFile, File, Form
from loguru import logger
from django.db import transaction
from apps.music.api.schemas.artists import ArtistCreateSchema
from apps.music.api.types import Tags
from apps.music.models import Images, Artists, Labels, Genres

router_v1 = Router(tags=[Tags.artists])


@router_v1.post(
    path="/",
    summary="Добавить нового исполнителя",
)
def add_new_artist(
    request,
    payload: Form[ArtistCreateSchema],
    avatar: UploadedFile = File(None),
):
    logger.info(request)

    label = get_object_or_404(Labels, id=payload.label_id) if payload.label_id else None
    genres = get_list_or_404(Genres, id__in=payload.genres_ids) if payload.genres_ids else None

    with transaction.atomic():
        new_avatar = None
        if avatar:
            new_avatar = Images.objects.create(
                name=avatar.name,
            )

        new_artist_kwargs = dict(
            name=payload.name,
            description=payload.description,
            avatar=new_avatar,
            birth_date=payload.birth_date,
            country=payload.country,
            genres=genres,
            label=label,
            bio=payload.bio,
            is_verified=payload.is_verified,
        )
        if genres:
            new_artist_kwargs["genres"] = genres

        return Artists.objects.create(**new_artist_kwargs)
