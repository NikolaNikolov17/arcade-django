from django.contrib.auth.views import LogoutView
from django.urls import path, include

from users.views import CustomLoginView, RegisterView, ProfileDetailView, ProfileUpdateView, ProfileDeleteView, \
    CustomPasswordChangeView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', include([
        path('', ProfileDetailView.as_view(), name='profile'),
        path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
        path('profile/delete/', ProfileDeleteView.as_view(), name='delete_profile'),
        path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    ])),
]