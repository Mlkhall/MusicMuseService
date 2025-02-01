from http import HTTPStatus

from ninja import UploadedFile
from ninja.errors import HttpError


def validate_video_file(video: UploadedFile) -> UploadedFile:
    # MIME-тип должен начинаться с "video/"
    if not video.content_type.startswith("video/"):
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST, message=f"Неверный тип файла {video.content_type}. Ожидается видео."
        )
    return video


def validate_audio_file(audio: UploadedFile) -> UploadedFile:
    # MIME-тип должен начинаться с "audio/"
    if not audio.content_type.startswith("audio/"):
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST, message=f"Неверный тип файла {audio.content_type}. Ожидается аудио."
        )
    return audio


def validate_image_file(image: UploadedFile) -> UploadedFile:
    # MIME-тип должен начинаться с "image/"
    if not image.content_type.startswith("image/"):
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message=f"Неверный тип файла {image.content_type}. Ожидается изображение.",
        )
    return image
