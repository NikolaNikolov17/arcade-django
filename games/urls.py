from django.urls import path, include
from .views import GamesHomeView, SpaceInvadersView, PacManView, SaveScoreView

urlpatterns = [
    path('', include([
        path('', GamesHomeView.as_view(), name='games_hub'),
        path('space-invaders/', SpaceInvadersView.as_view(), name='space_invaders'),
        path('pac-man/', PacManView.as_view(), name='pac_man'),
    path('save-score/', SaveScoreView.as_view(), name='save_score'),
    ])),
]