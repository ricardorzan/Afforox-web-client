from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, FormView
from .models import Usuario
from .forms import (
    LogInForm,
    SignUpUserForm,
    SignUpAddressForm
)

# Create your views here.
from django.views import View


def Homepage(request):
    return render(request, "home.html")


def About(request):
    return render(request, "about.html")

class LogInView(FormView):
    form_class = LogInForm
    template_name = "login.html"

class AccountCreateView(View):
    form_address = SignUpAddressForm
    form_user = SignUpUserForm
    template_name = "signup.html"

    def get(self, request):
        context = {}
        context['form_address'] = self.form_address(prefix='address')
        context['form_user'] = self.form_user(prefix='user')
        return render(request, AccountCreateView.template_name, context)