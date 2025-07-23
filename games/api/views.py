from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from games.api.serializers import GameSerializer
from games.models import Game


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]