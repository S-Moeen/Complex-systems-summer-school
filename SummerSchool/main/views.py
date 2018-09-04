from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView, RedirectView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy
from main.models import Pricing_Game
from django.shortcuts import redirect, render
from main.Forms import PricingPlayForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User


# Create your views here.


class Login(LoginView):
    template_name = 'main/login.html'


def login_success(request):
    return redirect("/gamer_dashboard")


class Game_Details(LoginRequiredMixin,  UserPassesTestMixin, FormView):
    template_name = "main/game_details.html"
    form_class = PricingPlayForm
    # success_url =

    def get_context_data(self, **kwargs):
        print(self.kwargs)
        context = super().get_context_data(**kwargs)
        users = [user.username for user in User.objects.filter(is_staff=False).order_by("-id")]
        game = Pricing_Game.objects.get(id=self.kwargs["pk"])
        context["users"] = users[len(users) - game.players_number:]
        return context

    def get_success_url(self):
        return reverse_lazy('main:game', kwargs={'pk': self.kwargs["pk"]})

    def get_form_kwargs(self):
        kwargs = super(Game_Details, self).get_form_kwargs()
        # kwargs['user'] = Customer.objects.get(username=self.request.user)
        kwargs["game"] = Pricing_Game.objects.get(id=self.kwargs["pk"])
        kwargs["user"] = self.request.user
        # kwargs["round"] = PricingPlayForm.get_current_round(kwargs["game"].id)
        return kwargs

    def form_valid(self, form):
        print('form valid ast ! ')
        form.update_db()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class Gamer_Dashboard(TemplateView, UserPassesTestMixin, LoginRequiredMixin):
    template_name = "main/gamer_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Pricing_Game.objects.all()
        return context

    def test_func(self):
        return not self.request.user.is_staff


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('main:login'))
