from rest_framework import serializers

from music.models import (
    Albums,
    Artists,
    GeneratedImageContent,
    GeneratedVideoContent,
    Genres,
    Labels,
    Tracks,
)


class ArtistsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, default=None)

    class Meta:
        model = Artists
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "slug")


class AlbumsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, default=None)

    class Meta:
        model = Albums
        fields = "__all__"


class TracksSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, default=None)

    class Meta:
        model = Tracks
        fields = "__all__"


class LabelsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, default=None)

    class Meta:
        model = Labels
        fields = "__all__"


class GenresSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, default=None)

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
