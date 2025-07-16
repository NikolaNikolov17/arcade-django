from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from chat.forms import ChatMessageForm
from chat.models import ChatMessage
from games.models import Game, GameScore


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

        # 🎮 Leaderboard
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

        # 💬 Chat messages
        context['chat_form'] = ChatMessageForm()
        context['chat_messages'] = ChatMessage.objects.order_by('-timestamp')[:50][::-1]

        return context

    def post(self, request, *args, **kwargs):
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            ChatMessage.objects.create(
                sender=request.user,
                message=form.cleaned_data['message']
            )
        return redirect('home')

