from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import RedirectView, TemplateView
from googleapiclient.discovery import build

from ArcadeApp_Project import settings
from chat.forms import ChatMessageForm
from chat.models import ChatMessage
from games.models import Game, GameScore
from music.forms import SongForm
from music.models import Song
from music.templatetags.youtube_extras import youtube_id


# Create your views here.
class HomeRedirectView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get_redirect_url(*args, **kwargs)
        return reverse_lazy('login')



class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Leaderboard
        games = Game.objects.all()
        leaderboard = {}
        for game in games:
            top_scores = (
                GameScore.objects
                .filter(game=game)
                .values('user__username')
                .annotate(max_score=Max('score'))
                .order_by('-max_score')[:10]
            )
            leaderboard[game.name] = list(top_scores)
        context['leaderboard'] = leaderboard

        # Chat
        context['chat_form'] = ChatMessageForm()
        context['chat_messages'] = ChatMessage.objects.order_by('-timestamp')[:50][::-1]

        # Music player
        context['song_form'] = SongForm()
        last_song = Song.objects.filter(added_by=self.request.user).order_by('-added_at').first()
        context['youtube_link'] = last_song.youtube_url if last_song else ''
        context['song_history'] = Song.objects.filter(added_by=self.request.user).order_by('-added_at')[:10]

        return context

    def post(self, request, *args, **kwargs):
        # Chat
        if 'message' in request.POST:
            form = ChatMessageForm(request.POST)
            if form.is_valid():
                ChatMessage.objects.create(
                    sender=request.user,
                    message=form.cleaned_data['message']
                )

        # Clear song history
        if 'clear_history' in request.POST:
            Song.objects.filter(added_by=request.user).delete()
            return redirect('home')

        # Music
        elif 'youtube_url' in request.POST:
            form = SongForm(request.POST)
            if form.is_valid():
                youtube_url = form.cleaned_data['youtube_url']
                clean_url = youtube_url.split('&')[0]
                title = fetch_youtube_title(clean_url)

                existing_song = Song.objects.filter(
                    youtube_url=clean_url,
                    added_by=request.user
                ).first()

                if existing_song:
                    existing_song.added_at = timezone.now()
                    existing_song.save()
                else:
                    Song.objects.create(
                        title=title,
                        youtube_url=clean_url,
                        added_by=request.user
                    )

        return redirect('home')



def fetch_youtube_title(youtube_url):
    try:
        video_id = youtube_id(youtube_url)
        if not video_id:
            return "Invalid URL"

        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        request = youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()

        if response['items']:
            return response['items'][0]['snippet']['title']
        return "Unknown Title"

    except Exception as e:
        print("YouTube API error:", e)
        return "Unknown Title"