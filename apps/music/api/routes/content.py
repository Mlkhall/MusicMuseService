from http import HTTPStatus

from django.db import transaction
from loguru import logger
from ninja import File, Form, Query, Router, UploadedFile
from ninja.errors import HttpError
from ninja.pagination import PageNumberPagination, paginate

from apps.music.api.docs import Tags
from apps.music.api.dto.content import (
    AddNewAudioIn,
    AddNewAudioOut,
    AddNewImageIn,
    AddNewImageOut,
    AddNewVideoIn,
    AddNewVideoOut,
    GetAudioPagesOut,
    GetFilteredAudioOut,
    GetFilteredContentIn,
    GetFilteredVideoOut,
    GetImagePagesOut,
    GetVideoPagesOut,
)
from apps.music.api.validators import validate_audio_file, validate_image_file, validate_video_file
from apps.music.models import Audio, Images, Video

router_v1 = Router(tags=[Tags.content])


@router_v1.post(
    path="/audio/",
    summary="Добавить аудиозапись в хранилище",
    response=AddNewAudioOut,
)
def add_new_audio(request, payload: Form[AddNewAudioIn], audio: UploadedFile = File(...)):
    logger.info(request)

    validate_audio_file(audio)

    with transaction.atomic():
        new_audio, _ = Audio.objects.update_or_create(
            name=payload.name or audio.name,
            defaults={
                "name": payload.name or audio.name,
                "audio": audio,
                "description": payload.description,
                "transcription": payload.transcription,
            },
        )

        return new_audio


@router_v1.get(
    path="/audio/filter/",
    summary="Получить аудиозаписи по фильтру",
    response=GetFilteredAudioOut,
)
def get_filtered_audio(request, content_filter: GetFilteredContentIn = Query(...)):
    logger.info(request)

    logger.info(request)
    if not content_filter.name and not content_filter.pk:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    audio = Audio.objects.all()
    filtered_audio = content_filter.filter(audio).first()
    if not filtered_audio:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message="Аудиозапись не найдена",
        )

    return filtered_audio


@router_v1.get(
    path="/audio/pages/",
    response=list[GetAudioPagesOut],
    description="Получение всех аудио постранично",
    summary="Получить страницы аудио",
)
@paginate(PageNumberPagination)
def get_audio_pages(request):
    logger.info(request)
    return Audio.objects.all()


@router_v1.post(
    path="/video/",
    summary="Добавить видеозапись в хранилище",
    response=AddNewVideoOut,
)
def add_new_video(request, payload: Form[AddNewVideoIn], video: UploadedFile = File(...)):
    logger.info(request)

    validate_video_file(video)

    with transaction.atomic():
        new_video, _ = Video.objects.update_or_create(
            name=payload.name or video.name,
            defaults={
                "name": payload.name or video.name,
                "video": video,
                "description": payload.description,
            },
        )

        return new_video


@router_v1.get(
    path="/video/filter/",
    summary="Получить видеозапись по фильтру",
    response=GetFilteredVideoOut,
)
def get_filtered_video(request, content_filter: GetFilteredContentIn = Query(...)):
    logger.info(request)

    logger.info(request)
    if not content_filter.name and not content_filter.pk:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    video = Video.objects.all()
    filtered_video = content_filter.filter(video).first()
    if not filtered_video:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message="Видеозапись не найдена",
        )

    return filtered_video


@router_v1.get(
    path="/video/pages/",
    response=list[GetVideoPagesOut],
    description="Получение всех видео постранично",
    summary="Получить страницы видео",
)
@paginate(PageNumberPagination)
def get_video_pages(request):
    logger.info(request)
    return Video.objects.all()


@router_v1.post(
    path="/images/",
    summary="Добавить изображение в хранилище",
    response=AddNewImageOut,
)
def add_new_image(request, payload: Form[AddNewImageIn], image: UploadedFile = File(...)):
    logger.info(request)

    validate_image_file(image)

    with transaction.atomic():
        new_image, _ = Images.objects.update_or_create(
            name=payload.name or image.name,
            defaults={
                "name": payload.name or image.name,
                "image": image,
                "description": payload.description,
            },
        )

        return new_image


@router_v1.get(
    path="/images/filter/",
    summary="Получить изображение по фильтру",
    response=GetFilteredVideoOut,
)
def get_filtered_image(request, content_filter: GetFilteredContentIn = Query(...)):
    logger.info(request)

    logger.info(request)
    if not content_filter.name and not content_filter.pk:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    images = Images.objects.all()
    filtered_image = content_filter.filter(images).first()
    if not filtered_image:
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message="Изображение не найдено",
        )

    return filtered_image


@router_v1.get(
    path="/images/pages/",
    response=list[GetImagePagesOut],
    description="Получение всех картинок постранично",
    summary="Получить страницы картинок",
)
@paginate(PageNumberPagination)
def get_images_pages(request):
    logger.info(request)
    return Images.objects.all()
