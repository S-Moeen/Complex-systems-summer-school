from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView, RedirectView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy
from main.models import PricingGame
from django.shortcuts import redirect, render


# Create your views here.


class Login(LoginView):
    template_name = 'main/login.html'


def login_success(request):
    return redirect("/gamer_dashboard")


class Game_Details(TemplateView, UserPassesTestMixin, LoginRequiredMixin):
    template_name = "main/game_details.html"

    def get_context_data(self, **kwargs):
        self.game = PricingGame.objects.get(id=pk)
        context = super().get_context_data(**kwargs)
        context["game"] = self.game


class Gamer_Dashboard(TemplateView, UserPassesTestMixin, LoginRequiredMixin):
    template_name = "main/gamer_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = PricingGame.objects.all()
        return context

    def test_func(self):
        return not self.request.user.is_staff


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('main:login'))
