from rest_framework import routers

from music.api.views import ArtistsViewSet, AlbumsViewSet, TracksViewSet, LabelsViewSet, GenresViewSet, GeneratedImageContentViewSet, GeneratedVideoContentViewSet


api_router_v1 = routers.DefaultRouter()
api_router_v1.register(prefix='artists', viewset=ArtistsViewSet)
api_router_v1.register(prefix='albums', viewset=AlbumsViewSet)
api_router_v1.register(prefix='tracks', viewset=TracksViewSet)
api_router_v1.register(prefix='labels', viewset=LabelsViewSet)
api_router_v1.register(prefix='genres', viewset=GenresViewSet, basename='genres')
api_router_v1.register(prefix='image_content', viewset=GeneratedImageContentViewSet)
api_router_v1.register(prefix=r'video_content', viewset=GeneratedVideoContentViewSet)
