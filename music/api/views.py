from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from music.api.serializers import (
    AlbumsSerializer,
    ArtistsSerializer,
    GeneratedImageContentSerializer,
    GeneratedVideoContentSerializer,
    GenresSerializer,
    LabelsSerializer,
    TracksSerializer,
)
from music.models import (
    Albums,
    Artists,
    GeneratedImageContent,
    GeneratedVideoContent,
    Genres,
    Labels,
    Tracks,
)


@extend_schema(tags=["Артисты"])
class ArtistsViewSet(viewsets.ModelViewSet):
    queryset = Artists.objects.all()
    serializer_class = ArtistsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


@extend_schema(tags=["Альбомы"])
class AlbumsViewSet(viewsets.ModelViewSet):
    queryset = Albums.objects.all()
    serializer_class = AlbumsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


@extend_schema(tags=["Треки"])
class TracksViewSet(viewsets.ModelViewSet):
    queryset = Tracks.objects.all()
    serializer_class = TracksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


@extend_schema(tags=["Лейблы"])
class LabelsViewSet(viewsets.ModelViewSet):
    queryset = Labels.objects.all()
    serializer_class = LabelsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


@extend_schema(tags=["Жанры"])
class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


@extend_schema(tags=["Контент"])
class GeneratedImageContentViewSet(viewsets.ModelViewSet):
    queryset = GeneratedImageContent.objects.all()
    serializer_class = GeneratedImageContentSerializer


@extend_schema(tags=["Контент"])
class GeneratedVideoContentViewSet(viewsets.ModelViewSet):
    queryset = GeneratedVideoContent.objects.all()
    serializer_class = GeneratedVideoContentSerializer
