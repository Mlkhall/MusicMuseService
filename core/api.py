from ninja import NinjaAPI

from apps.music.api.routes.genres import router_v1 as genres_router_v1
from apps.music.api.routes.artists import router_v1 as artists_router_v1

api = NinjaAPI()

api.add_router(prefix='v1/genres', router=genres_router_v1)
api.add_router(prefix='v1/artists', router=artists_router_v1)
