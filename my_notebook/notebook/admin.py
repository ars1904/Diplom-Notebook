from django.contrib import admin

from django.contrib import admin

from .models import Tags, Note


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Note)
