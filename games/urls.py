from django.urls import path
from . import views

urlpatterns = [
    path('space-invaders/', views.space_defenders_view, name='space_invaders'),
    path('pac-man/', views.pac_man_view, name='pac_man'),
]