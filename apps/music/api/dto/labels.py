from ninja import Schema, ModelSchema, FilterSchema
from pydantic import PositiveInt

from apps.music.api.dto._base import EmptyStrToDefault
from apps.music.models import Labels
from datetime import datetime


class LabelSchema(ModelSchema):
    class Meta:
        model = Labels
        fields = "__all__"


class BaseLabelOutSchema(Schema):
    pk: PositiveInt
    name: str
    description: str | None = None
    updated: datetime
    created: datetime
    cover_image: str | None = None


class AddNewLabelIn(Schema):
    name: str
    description: EmptyStrToDefault[str | None] = None


class AddNewLabelOut(LabelSchema):
    ...


class GetFilteredLabelsIn(FilterSchema):
    pk: PositiveInt | None = None
    name: str | None = None


class GetFilteredLabelsOut(BaseLabelOutSchema):
    ...


class GetLabelsPagesOut(LabelSchema):
    ...


class UpdateLabelIn(Schema):
    name: EmptyStrToDefault[str | None] = None
    description: EmptyStrToDefault[str | None] = None


class UpdateLabelOut(BaseLabelOutSchema):
    ...
