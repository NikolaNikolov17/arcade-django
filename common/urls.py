from django.urls import path

from common.views import HomeRedirectView, HomeView

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='root'),
    path('home/', HomeView.as_view(), name='home'),
]