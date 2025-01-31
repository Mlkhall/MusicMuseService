from ninja import Schema, ModelSchema, FilterSchema
from pydantic import PositiveInt, AnyHttpUrl
from datetime import date
from enum import StrEnum
from apps.music.models import Artists
from pydantic_extra_types.country import CountryAlpha3
from apps.music.api.dto._base import EmptyStrToDefault


class ArtistGender(StrEnum):
    male = "male"
    female = "female"
    not_specified = "not_specified"
    other = "other"


class ArtistSchema(ModelSchema):
    class Meta:
        model = Artists
        fields = "__all__"


class BaseArtistOutSchema(Schema):
    id: PositiveInt
    name: str
    description: str | None = None
    birth_date: date | None = None
    country: str
    genres: tuple[str, ...] | None = None
    label: str | None = None
    bio: str | None = None
    is_verified: bool
    gender: ArtistGender
    avatar: AnyHttpUrl | None = None


class AddNewArtistIn(Schema):
    name: str
    description: EmptyStrToDefault[str | None] = None
    birth_date: EmptyStrToDefault[date | None] = None
    country: CountryAlpha3 = 'RUS'
    genres_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = ()
    label_id: EmptyStrToDefault[PositiveInt | None] = None
    bio: EmptyStrToDefault[str | None] = None
    is_verified: bool = False
    gender: ArtistGender


class AddNewArtistOut(BaseArtistOutSchema):
    ...


class UpdateArtistIn(Schema):
    name: EmptyStrToDefault[str | None] = None
    description: EmptyStrToDefault[str | None] = None
    birth_date: EmptyStrToDefault[date | None] = None
    country: CountryAlpha3 = 'RUS'
    genres_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = ()
    label_id: EmptyStrToDefault[PositiveInt | None] = None
    bio: EmptyStrToDefault[str | None] = None
    is_verified: bool = False
    gender: ArtistGender


class UpdateArtistOut(BaseArtistOutSchema):
    ...


class GetFilteredArtistIn(FilterSchema):
    pk: PositiveInt | None = None
    name: str | None = None


class GetFilteredArtistOut(BaseArtistOutSchema):
    ...


class GetArtistPagesItemOut(BaseArtistOutSchema):
    ...


class GetArtistPagesOut(Schema):
    items: tuple[GetArtistPagesItemOut, ...]
    total: PositiveInt
    per_page: PositiveInt
