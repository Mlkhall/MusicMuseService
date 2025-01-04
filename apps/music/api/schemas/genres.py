from ninja import ModelSchema, Schema, FilterSchema
from datetime import datetime
from apps.music.models import Genres


class GenresSchema(ModelSchema):
    class Meta:
        model = Genres
        fields = "__all__"


class GenreUpdateSchema(Schema):
    name: str | None
    description: str | None
    parent_id: int | None


class GenreCreateSchema(Schema):
    name: str
    description: str | None = None
    parent_genre_id: int | None = None


class GenreFilterSchema(FilterSchema):
    pk: int | None = None
    name: str | None = None


class FilteredGenreSchema(Schema):
    pk: int
    name: str
    slug: str
    description: str | None = None
    parent_genre_id: int | None = None
    image_cover: str | None = None
    created_at: datetime
    updated_at: datetime


class AlbumCreateSchema(Schema):
    name: str
    description: str | None = None
    artists_id: int
    labels_id: int
