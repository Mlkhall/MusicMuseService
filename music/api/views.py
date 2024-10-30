from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from music.api.serializers import ArtistsSerializer, AlbumsSerializer, TracksSerializer, LabelsSerializer, GenresSerializer, GeneratedImageContentSerializer, GeneratedVideoContentSerializer
from music.models import Artists, Albums, Tracks, Labels, Genres, GeneratedImageContent, GeneratedVideoContent


@extend_schema(tags=["Артисты"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список артистов",
    ),
)
class ArtistsViewSet(viewsets.ModelViewSet):
    queryset = Artists.objects.all()
    serializer_class = ArtistsSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@extend_schema(tags=["Альбомы"])
class AlbumsViewSet(viewsets.ModelViewSet):
    queryset = Albums.objects.all()
    serializer_class = AlbumsSerializer


@extend_schema(tags=["Треки"])
class TracksViewSet(viewsets.ModelViewSet):
    queryset = Tracks.objects.all()
    serializer_class = TracksSerializer


@extend_schema(tags=["Лейблы"])
class LabelsViewSet(viewsets.ModelViewSet):
    queryset = Labels.objects.all()
    serializer_class = LabelsSerializer


@extend_schema(tags=["Жанры"])
class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


@extend_schema(tags=["Контент"])
class GeneratedImageContentViewSet(viewsets.ModelViewSet):
    queryset = GeneratedImageContent.objects.all()
    serializer_class = GeneratedImageContentSerializer


@extend_schema(tags=["Контент"])
class GeneratedVideoContentViewSet(viewsets.ModelViewSet):
    queryset = GeneratedVideoContent.objects.all()
    serializer_class = GeneratedVideoContentSerializer