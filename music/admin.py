from django.contrib import admin

from music.models import Song


# Register your models here.
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'added_by', 'added_at')
    search_fields = ('title', 'youtube_url')
    list_filter = ('added_by',)