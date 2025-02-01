from ninja import ModelSchema, Schema, FilterSchema

from apps.music.api.dto._base import EmptyStrToDefault
from apps.music.models import Audio, Video, Images


class BaseAudioOutSchema(ModelSchema):
    class Meta:
        model = Audio
        fields = "__all__"


class BaseVideoOutSchema(ModelSchema):
    class Meta:
        model = Video
        fields = "__all__"


class BaseImageOutSchema(ModelSchema):
    class Meta:
        model = Images
        fields = "__all__"


class AddNewAudioIn(Schema):
    name: EmptyStrToDefault[str | None] = None
    description: EmptyStrToDefault[str | None] = None
    transcription: EmptyStrToDefault[str | None] = None


class AddNewAudioOut(BaseAudioOutSchema): ...


class AddNewVideoIn(Schema):
    name: EmptyStrToDefault[str | None] = None
    description: EmptyStrToDefault[str | None] = None


class AddNewVideoOut(BaseVideoOutSchema): ...


class AddNewImageIn(Schema):
    name: EmptyStrToDefault[str | None] = None
    description: EmptyStrToDefault[str | None] = None


class AddNewImageOut(BaseImageOutSchema): ...


class GetFilteredContentIn(FilterSchema):
    pk: int | None = None
    name: str | None = None


class GetFilteredAudioOut(BaseAudioOutSchema): ...


class GetFilteredVideoOut(BaseVideoOutSchema): ...


class GetFilteredImageOut(BaseImageOutSchema): ...


class GetAudioPagesOut(BaseAudioOutSchema): ...


class GetVideoPagesOut(BaseVideoOutSchema): ...


class GetImagePagesOut(BaseImageOutSchema): ...
