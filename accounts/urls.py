from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', next_page='/', redirect_authenticated_user=True)),
    path('logout/', auth_views.LogoutView.as_view(next_page='/')),
    path('registration/', views.registration, name='registration')
]