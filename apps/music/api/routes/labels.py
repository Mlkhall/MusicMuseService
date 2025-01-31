from django.shortcuts import get_object_or_404
from ninja import Router, UploadedFile, File, Form, Query
from pydantic import PositiveInt

from apps.music.api.docs import Tags
from loguru import logger
from http import HTTPStatus
from ninja.errors import HttpError
from django.db import transaction, IntegrityError
from apps.music.api.dto.labels import AddNewLabelIn, AddNewLabelOut, GetFilteredLabelsOut, GetFilteredLabelsIn, \
    GetLabelsPagesOut, UpdateLabelOut, UpdateLabelIn
from apps.music.models import Labels, Images
from ninja.pagination import paginate, PageNumberPagination

router_v1 = Router(tags=[Tags.labels])


@router_v1.post(
    path="/",
    summary="Добавить новый лейбл",
    response=AddNewLabelOut,
)
def add_new_label(
    request,
    payload: Form[AddNewLabelIn],
    logo: UploadedFile = File(None),
):
    logger.info(request)

    with transaction.atomic():
        new_logo = None

        if logo:
            new_logo, was_logo_created = Images.objects.get_or_create(
                name=logo.name,
                defaults={"name": logo.name, "image": logo},
            )

            if was_logo_created:
                logger.success(f"Изображение '{new_logo.name}' успешно загружено")

        try:
            new_label = Labels.objects.create(
                name=payload.name,
                description=payload.description,
                cover_image=new_logo,
            )
        except IntegrityError as exc:
            logger.warning(exc)
            raise HttpError(
                status_code=HTTPStatus.CONFLICT,
                message=f"Лейбл с именем '{payload.name}' уже существует",
            )

    return new_label


@router_v1.get(
    path="/filter/",
    summary="Получить лейбл по фильтру",
    response=GetFilteredLabelsOut,
)
def get_filtered_labels(request, label_filter: GetFilteredLabelsIn = Query(...)):
    logger.info(request)
    if not label_filter.pk and not label_filter.name:
        raise HttpError(
            status_code=HTTPStatus.BAD_REQUEST,
            message="Необходимо указать хотя бы один фильтр, name или pk",
        )

    labels = Labels.objects.all()
    label = label_filter.filter(labels).first()
    if not label:
        logger.warning(f"Лейбл {label_filter.dict()} не найден")
        raise HttpError(
            status_code=HTTPStatus.NOT_FOUND,
            message=f"Лейбл {label_filter.dict()} не найден",
        )

    return GetFilteredLabelsOut(
        pk=label.pk,
        name=label.name,
        description=label.description,
        cover_image=label.cover_image.image if label.cover_image else None,
        updated=label.updated,
        created=label.created,
    )


@router_v1.get(
    path="/pages/",
    response=list[GetLabelsPagesOut],
    description="Получить все лейблы",
    summary="Получить все лейблы",
)
@paginate(PageNumberPagination)
def get_labels_pages(request):
    logger.info(request)
    return Labels.objects.all()


@router_v1.put(
    path="/{label_pk}/",
    summary="Обновить лейбл",
    response=UpdateLabelOut,
)
def update_label(
    request,
    label_pk: PositiveInt,
    payload: Form[UpdateLabelIn],
    logo: UploadedFile = File(None),
):
    logger.info(request)
    label = get_object_or_404(Labels, pk=label_pk)

    with transaction.atomic():
        if logo:
            new_logo, was_logo_created = Images.objects.update_or_create(
                name=logo.name,
                defaults={"name": logo.name, "image": logo},
            )

            if was_logo_created:
                logger.success(f"Изображение '{new_logo.name}' успешно загружено")
            else:
                logger.success(f"Изображение '{new_logo.name}' успешно обновлено")

            label.cover_image = new_logo

        if payload.name:
            label.name = payload.name

        if payload.description:
            label.description = payload.description

        label.save()

        return UpdateLabelOut(
            pk=label.pk,
            name=label.name,
            description=label.description,
            cover_image=label.cover_image.image if label.cover_image else None,
            updated=label.updated,
            created=label.created,
        )
