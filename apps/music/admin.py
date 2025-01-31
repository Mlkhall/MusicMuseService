from django.contrib import admin

from apps.music import models

admin.site.register(models.Tracks)
admin.site.register(models.Artists)
admin.site.register(models.Releases)
admin.site.register(models.Labels)
admin.site.register(models.Genres)
