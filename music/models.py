from django.db import models
from django.conf import settings
from django.core.validators import URLValidator

# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length=100)
    youtube_url = models.URLField(validators=[URLValidator()])
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title