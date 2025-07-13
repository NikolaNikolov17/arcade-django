from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView


# Create your views here.
class HomeRedirectView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get_redirect_url(*args, **kwargs)
        return reverse_lazy('login')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'