from rest_framework import routers

from music.api.views import (
    AlbumsViewSet,
    ArtistsViewSet,
    AudioViewSet,
    GenresViewSet,
    ImagesViewSet,
    LabelsViewSet,
    TracksViewSet,
    VideoViewSet,
)

api_router_v1 = routers.DefaultRouter()
api_router_v1.register(prefix="artists", viewset=ArtistsViewSet)
api_router_v1.register(prefix="albums", viewset=AlbumsViewSet)
api_router_v1.register(prefix="tracks", viewset=TracksViewSet)
api_router_v1.register(prefix="labels", viewset=LabelsViewSet)
api_router_v1.register(prefix="genres", viewset=GenresViewSet, basename="genres")
api_router_v1.register(prefix="images", viewset=ImagesViewSet)
api_router_v1.register(prefix="audio", viewset=AudioViewSet)
api_router_v1.register(prefix="video", viewset=VideoViewSet)
