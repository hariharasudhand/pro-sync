from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_view


urlpatterns = [

    path('register/', user_view.register, name='register'),
    path('profile/', user_view.profile, name='profile'),
    path('activate/', user_view.activate, name='activate'),


    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('success/', auth_views.LoginView.as_view(template_name='app/main.html'), name='success'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/index.html'), name='logout'),

    # organization links
    path('org-onboard/', user_view.orgOnboard, name='org-onboard'),
    path('org-registered/', user_view.orgRegistered, name='org-registered'),
    path('org-update/', user_view.org_update, name='org-update'),
    path('org-approve/<int:id>', user_view.org_approve, name='org-approve'),
    path('org-approved/', user_view.org_approved, name='org-approved'),

    # Roles links
    path('roles/', user_view.roles_add, name='roles'),
    path('roles/<int:id>/update', user_view.roles_update, name='roles-update'),
    path('roles/<int:id>/delete/', user_view.roles_cancel, name='roles-delete'),

    # Groups links
    path('groups/', user_view.group_add, name='groups'),
    path('groups/<int:id>/update', user_view.group_update, name='groups-update'),
    path('groups/<int:id>/delete/', user_view.groups_cancel, name='groups-delete'),


]