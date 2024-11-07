from rest_framework import serializers

from music.models import (
    Albums,
    Artists,
    Audio,
    Genres,
    Images,
    Labels,
    Tracks,
    Video,
)


class ArtistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        fields = "__all__"
        read_only_fields = ("slug",)


class AlbumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Albums
        fields = "__all__"
        read_only_fields = ("slug",)


class TracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = "__all__"
        read_only_fields = ("slug",)


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = "__all__"
        read_only_fields = ("slug",)


class GenresSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, default=None)

    class Meta:
        model = Genres
        fields = "__all__"


class ImagesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(initial="", default="")

    class Meta:
        model = Images
        fields = "__all__"
        read_only_fields = ("slug",)


class AudioSerializer(serializers.ModelSerializer):
    description = serializers.CharField(initial="", default="")

    class Meta:
        model = Audio
        fields = "__all__"
        read_only_fields = ("slug", "duration")


class VideoSerializer(serializers.ModelSerializer):
    description = serializers.CharField(initial="", default="")

    class Meta:
        model = Video
        fields = "__all__"
        read_only_fields = ("slug", "duration")
