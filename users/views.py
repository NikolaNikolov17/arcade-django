from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from users.forms import LoginForm, RegisterForm
from users.models import User


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_details.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'profile_pic']
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)