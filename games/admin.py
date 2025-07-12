from django.contrib import admin

from games.models import Game, GameScore


# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'score', 'created_at')
    list_filter = ('game',)
    ordering = ('-score',)