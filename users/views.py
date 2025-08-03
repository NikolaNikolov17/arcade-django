from asgiref.sync import sync_to_async
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from ArcadeApp_Project import settings
from users.forms import LoginForm, RegisterForm, CustomPasswordChangeForm
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

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile')
    success_message = "The password has been changed successfully."

    async def form_valid(self, form):
        response = await sync_to_async(super().form_valid)(form)
        update_session_auth_hash(self.request, form.user)
        await self.send_email_notification()
        return response

    async def send_email_notification(self):
        user_email = self.request.user.email
        if user_email:
            await sync_to_async(send_mail)(
                subject='Your password has been changed.',
                message='Hello! Your password has been changed successfully.',
                from_email=settings.COMPANY_EMAIL,
                recipient_list=[user_email],
                fail_silently=True,
            )