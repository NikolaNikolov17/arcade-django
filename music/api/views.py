from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from music.api.serializers import SongSerializer
from music.models import Song


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]