from django.contrib import admin

from music import models

admin.site.register(models.Tracks)
admin.site.register(models.Artists)
admin.site.register(models.Albums)
admin.site.register(models.Labels)
admin.site.register(models.Genres)
