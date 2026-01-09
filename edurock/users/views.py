from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.shortcuts import render, redirect

from .models import User, AboutUs, StudentActivity

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "pk"
    template_name = "users/user_detail.html"

user_detail_view = UserDetailView.as_view()

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name", "image"] # Feature: Profile Image Update
    template_name = "users/user_form.html"
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user

user_update_view = UserUpdateView.as_view()

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})

user_redirect_view = UserRedirectView.as_view()

def about_view(request):
    if request.user.is_authenticated:
        StudentActivity.objects.create(user=request.user, page_visited="About Us Page")
    about_data = AboutUs.objects.first()
    return render(request, "pages/about.html", {"about": about_data})

def magazine_view(request):
    if not request.user.is_authenticated:
        return redirect('account_login')
    StudentActivity.objects.create(user=request.user, page_visited="Magazine Page")
    return render(request, "pages/magazine.html")