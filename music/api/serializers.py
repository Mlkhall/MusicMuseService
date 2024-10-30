from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from music.models import Artists, Albums, Tracks, Labels, Genres, GeneratedImageContent, GeneratedVideoContent


@extend_schema_field(OpenApiTypes.BINARY)
class ImageField(serializers.ImageField):
    ...


class ArtistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        fields = "__all__"


class AlbumsSerializer(serializers.ModelSerializer):

    cover_image = ImageField()

    class Meta:
        model = Albums
        fields = "__all__"


class TracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = "__all__"


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = "__all__"


class GenresSerializer(serializers.ModelSerializer):

    image = ImageField()

    class Meta:
        model = Genres
        fields = "__all__"


class GeneratedImageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImageContent
        fields = "__all__"


class GeneratedVideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedVideoContent
        fields = "__all__"
