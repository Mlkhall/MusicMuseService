from datetime import datetime

from ninja import FilterSchema, ModelSchema, Schema
from pydantic import PositiveInt

from apps.music.api.dto._base import EmptyStrToDefault
from apps.music.models import Genres


class GenresSchema(ModelSchema):
    class Meta:
        model = Genres
        fields = "__all__"


class AddNewGenreIn(Schema):
    name: str
    description: EmptyStrToDefault[str | None] = None
    parent_genre_id: EmptyStrToDefault[PositiveInt | None] = None


class AddNewGenreOut(GenresSchema): ...


class GetFilteredGenreIn(FilterSchema):
    pk: PositiveInt | None = None
    name: str | None = None


class GetFilteredGenreInOut(Schema):
    pk: PositiveInt
    name: str
    slug: str
    description: str | None = None
    parent_genre_id: PositiveInt | None = None
    image_cover: str | None = None
    created_at: datetime
    updated_at: datetime


class GetGenrePagesOut(GenresSchema): ...


class UpdateGenreIn(Schema):
    name: str | None
    description: EmptyStrToDefault[str | None] = None
    parent_id: EmptyStrToDefault[PositiveInt | None] = None


class UpdateGenreOut(GenresSchema): ...
