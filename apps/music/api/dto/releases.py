from datetime import date, datetime
from enum import StrEnum

from ninja import FilterSchema, Schema
from pydantic import PositiveInt

from apps.music.api.dto._base import EmptyStrToDefault, Statuses


class ReleaseTypes(StrEnum):
    album = "album"
    mini_album = "mini_album"
    single = "single"
    maxi_single = "maxi_single"
    podcast = "podcast"
    book = "book"
    compilation = "compilation"
    reissue = "reissue"
    remix = "remix"
    live = "live"
    indefinite = "indefinite"


class BaseReleaseOutSchema(Schema):
    pk: PositiveInt
    name: str
    description: str | None = None
    cover_image: str | None = None
    release_date: date | None = None
    labels_names: tuple[str, ...] | None = None
    artists_names: tuple[str, ...] | None = None
    genres_names: tuple[str, ...] | None = None
    release_type: ReleaseTypes
    status: Statuses
    created: datetime
    updated: datetime


class AddNewReleaseIn(Schema):
    name: str
    description: EmptyStrToDefault[str | None] = None
    label_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    artist_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    genre_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    release_type: ReleaseTypes = ReleaseTypes.indefinite
    release_date: EmptyStrToDefault[date | None] = None
    publication_time: EmptyStrToDefault[datetime | None] = None
    status: Statuses = Statuses.moderation


class AddNewReleaseOut(BaseReleaseOutSchema): ...


class GetFilteredReleaseIn(FilterSchema):
    pk: PositiveInt | None = None
    name: str | None = None


class GetFilteredReleaseOut(BaseReleaseOutSchema): ...


class GetReleasePagesItemOut(BaseReleaseOutSchema): ...


class GetReleasesPagesOut(Schema):
    items: tuple[GetReleasePagesItemOut, ...]
    total: PositiveInt
    per_page: PositiveInt


class UpdateReleaseIn(Schema):
    name: EmptyStrToDefault[str | None] = None
    description: EmptyStrToDefault[str | None] = None
    label_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    artist_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    genre_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    release_type: EmptyStrToDefault[ReleaseTypes] = None
    release_date: EmptyStrToDefault[date | None] = None
    publication_time: EmptyStrToDefault[datetime | None] = None
    status: EmptyStrToDefault[Statuses] = None


class UpdateReleaseOut(BaseReleaseOutSchema): ...
