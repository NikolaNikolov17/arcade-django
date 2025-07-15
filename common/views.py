from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

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
        return context

