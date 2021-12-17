from django.urls import path

from . import views
from .views import (
    AccountCreateView,
    LogInView,
    MainMenuView,
    AuthView,
    RegisterBusiness,
    Homepage,
    GetBusiness,
    About, update_aforo
)

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('login/', LogInView.as_view(), name='login'),
    path('signup/', AccountCreateView.as_view(), name='signup'),
    path('main/', MainMenuView.as_view(), name='main'),
    path('auth/<username>/', AuthView.as_view(), name='auth'),
    path('register_business/', RegisterBusiness.as_view(), name='register_business'),
    path('negocios/<int:negocioid>', GetBusiness.as_view(), name='get_business'),
    path('negocios/<int:negocioid>/update_aforo/<str:action>', update_aforo, name='update_aforo')
]
