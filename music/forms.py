from django import forms

from music.models import Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['youtube_url']
        widgets = {
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter YouTube link'
            })
        }
        labels = {
            'youtube_url': ''
        }