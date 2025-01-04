# from ninja import Router, File, Form, Query
#
# from apps.music.api.schemas import Tags
#
# router_v1 = Router(tags=[Tags.albums])
#
#
# @router_v1.post(
#     path="/",
#     summary="Добавить новый альбом",
# )
# def add_new_album(
#     request,
#     payload: Form[AlbumCreateSchema],
#     cover_image: File = File(None),
# ):
#     logger.info(request)
#     with transaction.atomic():
#         new_cover_image = None
#         if cover_image:
#             new_cover_image = Images.objects.create(
#                 name=cover_image.name,
#             )
#
#         artist = get_object_or_404(Artists, id=payload.artist_id)
#         label = get_object_or_404(Labels, id=payload.label_id)
#
#         return Albums.objects.create(
#             name=payload.name,
#             description=payload.description,
#             artist=artist,
#             label=label,
#             cover_image=new_cover_image,
#         )