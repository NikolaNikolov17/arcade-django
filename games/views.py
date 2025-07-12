from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def space_defenders_view(request):
    return render(request, 'games/space-invaders.html')

def pac_man_view(request):
    return render(request, 'games/pac-man.html')