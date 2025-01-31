from ninja import Schema, FilterSchema
from pydantic import PositiveInt
from datetime import datetime
from apps.music.api.dto._base import Statuses, EmptyStrToDefault


class BaseTrackOut(Schema):
    pk: PositiveInt
    name: str
    description: str | None = None
    cover_image: str | None = None
    track: str
    video: str | None = None
    release_name: str
    labels_names: tuple[str, ...] | None = None
    artists_names: tuple[str, ...] | None = None
    genres_names: tuple[str, ...] | None = None
    status: Statuses
    created: datetime
    updated: datetime


class AddNewTrackIn(Schema):
    name: str
    description: EmptyStrToDefault[str | None] = None
    release_id: PositiveInt
    label_id: EmptyStrToDefault[PositiveInt | None] = None
    artist_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    genre_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    status: Statuses = Statuses.moderation


class AddNewTrackOut(BaseTrackOut):
    ...


class GetFilteredTrackIn(FilterSchema):
    pk: PositiveInt | None = None
    name: str | None = None


class GetFilteredTrackOut(BaseTrackOut):
    ...


class GetTrackPagesItemOut(BaseTrackOut):
    ...


class GetTrackPagesOut(Schema):
    items: tuple[GetTrackPagesItemOut, ...]
    total: PositiveInt
    per_page: PositiveInt


class UpdateTrackIn(Schema):
    name: EmptyStrToDefault[str | None] = None
    description: EmptyStrToDefault[str | None] = None
    release_id: EmptyStrToDefault[PositiveInt | None] = None
    label_id: EmptyStrToDefault[PositiveInt | None] = None
    artist_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    genre_ids: tuple[EmptyStrToDefault[PositiveInt], ...] = tuple()
    status: EmptyStrToDefault[Statuses] = None


class UpdateTrackOut(BaseTrackOut):
    ...
