from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_view


urlpatterns = [

    path('register/', user_view.register, name='register'),
    path('profile/', user_view.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('success/', auth_views.LoginView.as_view(template_name='app/main.html'), name='success'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/index.html'), name='logout'),

    # organization links
    path('org-onboard/', user_view.orgOnboard, name='org-onboard'),
    path('org-registered/', user_view.orgRegistered, name='org-registered'),

]