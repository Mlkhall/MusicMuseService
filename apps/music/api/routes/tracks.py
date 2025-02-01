from http import HTTPStatus

from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.shortcuts import get_list_or_404, get_object_or_404
from loguru import logger
from ninja import File, Form, Query, Router, UploadedFile
from ninja.errors import HttpError
from pydantic import PositiveInt

from apps.music.api.docs import Tags
from apps.music.api.dto.tracks import (
    AddNewTrackIn,
    AddNewTrackOut,
    GetFilteredTrackIn,
    GetFilteredTrackOut,
    GetTrackPagesItemOut,
    GetTrackPagesOut,
    UpdateTrackOut,
)
from apps.music.api.validators import validate_audio_file, validate_video_file, validate_image_file
from apps.music.models import Artists, Audio, Genres, Images, Labels, Releases, Tracks, Video

router_v1 = Router(tags=[Tags.tracks])


@router_v1.post(
    path="/",
    summary="Добавить новый трек",
    response=AddNewTrackOut,
)
def add_new_track(
    request,
    payload: Form[AddNewTrackIn],
    audio: UploadedFile = File(...),
    video: UploadedFile = File(None),
    cover: UploadedFile = File(None),
):
    logger.info(request)

    label = get_object_or_404(Labels, id=payload.label_id) if payload.label_id else None
    release = get_object_or_404(Releases, id=payload.release_id)
    genres = get_list_or_404(Genres, id__in=payload.genres_ids) if payload.genres_ids else None
    artists = get_list_or_404(Artists, id__in=payload.artist_ids) if payload.artist_ids else None

    validate_audio_file(audio)

    with transaction.atomic():
        new_video = None
        new_cover = None

        new_audio, was_audio_created = Audio.objects.get_or_create(
            name=audio.name,
            defaults={"name": audio.name, "audio": audio},
        )

        if video:
            validate_video_file(video)
            new_video, was_video_created = Video.objects.get_or_create(
                name=video.name,
                defaults={"name": video.name, "video": video},
            )

        if cover:
            validate_image_file(cover)
            new_cover, was_cover_created = Images.objects.get_or_create(
                name=cover.name,
                defaults={"name": cover.name, "image": cover},
            )

        try:
            new_track = Tracks.objects.create(
                name=payload.name,
                description=payload.description,
                audio=new_audio,
                video=new_video,
                cover=new_cover,
                release=release,
                label=label,
                genres=genres,
                artists=artists,
                status=payload.status,
            )
        except IntegrityError as exc:
            logger.warning(exc)
            raise HttpError(
                status_code=HTTPStatus.CONFLICT,
                message=f"Трек с именем '{payload.name}' уже существует",
            )

        if genres:
            new_track.genres.set(genres)

        if artists:
            new_track.artists.set(artists)

        if label:
            new_track.label = label

        if new_video:
            new_track.video = new_video

        if new_cover:
            new_track.cover = new_cover

        created_new_track = AddNewTrackOut(
            pk=new_track.pk,
            name=new_track.name,
            description=new_track.description,
            cover_image=new_track.cover.image if new_cover else None,
            track=new_track.audio.audio,
            video=new_track.video.video if new_video else None,
            release_name=new_track.release.name,
            labels_names=tuple(label.name for label in new_track.label.all()),
            artists_names=tuple(artist.name for artist in new_track.artists.all()),
            genres_names=tuple(genre.name for genre in new_track.genres.all()),
            status=new_track.status,
            created=new_track.created,
            updated=new_track.updated,
        )

        logger.success(f"Трек '{payload.name}' успешно создан: {created_new_track.dict()}")

        return created_new_track


@router_v1.get(
    path="/filter/",
    summary="Получить трек по фильтру",
    response=GetFilteredTrackOut,
)
def get_filtered_track(request, track_filter: GetFilteredTrackIn = Query(...)):
    logger.info(request)

    if not track_filter.name and not track_filter.pk:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    tracks = Tracks.objects.all()
    filtered_track = track_filter.filter(tracks).first()

    if not filtered_track:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=f"Трек для {track_filter.dict()} не найден",
        )

    return GetFilteredTrackOut(
        pk=filtered_track.pk,
        name=filtered_track.name,
        description=filtered_track.description,
        cover_image=filtered_track.cover.image if filtered_track.cover else None,
        track=filtered_track.audio.audio,
        video=filtered_track.video.video if filtered_track.video else None,
        release_name=filtered_track.release.name,
        labels_names=tuple(label.name for label in filtered_track.label.all()),
        artists_names=tuple(artist.name for artist in filtered_track.artists.all()),
        genres_names=tuple(genre.name for genre in filtered_track.genres.all()),
        status=filtered_track.status,
        created=filtered_track.created,
        updated=filtered_track.updated,
    )


@router_v1.get(
    path="/pages/",
    summary="Получить страницы треков",
    response=GetTrackPagesOut,
)
def get_tracks_pages(request, page: PositiveInt = Query(1), per_page: PositiveInt = Query(10)):
    logger.info(request)

    tracks = Tracks.objects.all()
    paginator = Paginator(tracks, per_page)
    page_tracks = paginator.get_page(page)

    items = tuple(
        GetTrackPagesItemOut(
            pk=track.pk,
            name=track.name,
            description=track.description,
            cover_image=track.cover.image if track.cover else None,
            track=track.audio.audio,
            video=track.video.video if track.video else None,
            release_name=track.release.name,
            labels_names=tuple(label.name for label in track.label.all()),
            artists_names=tuple(artist.name for artist in track.artists.all()),
            genres_names=tuple(genre.name for genre in track.genres.all()),
            status=track.status,
            created=track.created,
            updated=track.updated,
        )
        for track in page_tracks
    )

    return GetTrackPagesOut(
        items=items,
        total=paginator.count,
        per_page=per_page,
    )


@router_v1.put(
    path="/{track_id}/",
    summary="Обновить трек",
    response=UpdateTrackOut,
)
def update_track(
    request,
    track_id: PositiveInt,
    payload: Form[AddNewTrackIn],
    video: UploadedFile = File(None),
    cover: UploadedFile = File(None),
    audio: UploadedFile = File(None),
):
    logger.info(request)

    track = get_object_or_404(Tracks, id=track_id)

    label = get_object_or_404(Labels, id=payload.label_id) if payload.label_id else None
    release = get_object_or_404(Releases, id=payload.release_id)
    genres = get_list_or_404(Genres, id__in=payload.genres_ids) if payload.genres_ids else None
    artists = get_list_or_404(Artists, id__in=payload.artist_ids) if payload.artist_ids else None

    with transaction.atomic():
        new_video = None
        new_cover = None
        new_audio = None

        if video:
            validate_video_file(video)
            new_video, was_video_created = Video.objects.update_or_create(
                name=video.name,
                defaults={"name": video.name, "video": video},
            )

        if cover:
            validate_image_file(cover)
            new_cover, was_cover_created = Images.objects.update_or_create(
                name=cover.name,
                defaults={"name": cover.name, "image": cover},
            )

        if audio:
            validate_audio_file(audio)
            new_audio, was_audio_created = Audio.objects.update_or_create(
                name=audio.name,
                defaults={"name": audio.name, "audio": audio},
            )

        if payload.name:
            track.name = payload.name

        if payload.description:
            track.description = payload.description

        if genres:
            track.genres.set(genres)

        if artists:
            track.artists.set(artists)

        if label:
            track.label = label

        if release:
            track.release = release

        if new_video:
            track.video = new_video

        if new_cover:
            track.cover = new_cover

        if new_audio:
            track.audio = new_audio

        track.save()

        return UpdateTrackOut(
            pk=track.pk,
            name=track.name,
            description=track.description,
            cover_image=track.cover.image if track.cover else None,
            track=new_audio.audio.path if track.audio else None,
            video=track.video.video if track.video else None,
            release_name=track.release.name,
            labels_names=tuple(label.name for label in track.label.all()),
            artists_names=tuple(artist.name for artist in track.artists.all()),
            genres_names=tuple(genre.name for genre in track.genres.all()),
            status=track.status,
            created=track.created,
            updated=track.updated,
        )
