from django.urls import path

from . import views
from .views import (
    AccountCreateView,
    LogInView,
    MainMenuView,
    AuthView
)

urlpatterns = [
    path('', views.Homepage, name='home'),
    path('about/', views.About, name='about'),
    path('login/', LogInView.as_view(), name='login'),
    path('signup/', AccountCreateView.as_view(), name='signup'),
    path('main/', MainMenuView.as_view(), name='menu'),
    path('auth/', AuthView.as_view(), name='auth')
]