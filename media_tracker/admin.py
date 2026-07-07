from django.contrib import admin
from media_tracker.models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "current_season", "current_episode", "status", "updated_at")
    search_fields = ("title",)
    list_filter = ("status",)
    ordering = ("-updated_at",)
