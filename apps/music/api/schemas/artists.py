from ninja import Schema
from pydantic import PositiveInt
from datetime import date
from enum import StrEnum
from pydantic_extra_types.country import CountryAlpha3


class _ArtistGender(StrEnum):
    male = "male"
    female = "female"
    not_specified = "not_specified"
    other = "other"


class ArtistCreateSchema(Schema):
    name: str
    description: str | None = None
    birth_date: date | None = None
    country: CountryAlpha3 = 'RUS'
    genres_ids: list[PositiveInt] | None = None
    label_id: PositiveInt | None = None
    bio: str | None = None
    is_verified: bool = False
    gender: _ArtistGender
