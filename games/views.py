import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from games.models import Game, GameScore


# Create your views here.
class SpaceInvadersView(LoginRequiredMixin, TemplateView):
    template_name = 'games/space-invaders.html'


class PacManView(LoginRequiredMixin, TemplateView):
    template_name = 'games/pac-man.html'

class GamesHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'games/game-hub.html'

class SaveScoreView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        game_name = data.get('game')
        score = data.get('score')

        if not game_name or not isinstance(score, int):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

        game, _ = Game.objects.get_or_create(name=game_name)


        existing_score = GameScore.objects.filter(user=request.user, game=game).order_by('-score').first()

        if existing_score:
            if score > existing_score.score:
                existing_score.score = score
                existing_score.save()
            else:
                return JsonResponse({'status': 'ignored', 'message': 'Lower score'})
        else:
            GameScore.objects.create(user=request.user, game=game, score=score)

        return JsonResponse({'status': 'ok'})