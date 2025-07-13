from django.urls import path, include

from users.views import CustomLoginView, RegisterView, ProfileDetailView, ProfileUpdateView, ProfileDeleteView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', include([
        path('', ProfileDetailView.as_view(), name='profile'),
        path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
        path('profile/delete/', ProfileDeleteView.as_view(), name='delete_profile'),
    ])),
]