"""
Definition of urls for DeepDive.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.logIn.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    
        #Organizers URLs
    path('organizers/', views.organizer_list, name='organizer_list'),
    path('organizers/<int:organizer_id>/', views.organizer_detail, name='organizer_detail'),
    path('organizers/create/', views.organizer_create, name='organizer_create'),
    path('organizers/<int:organizer_id>/update/', views.organizer_update, name='organizer_update'),
    path('organizers/<int:organizer_id>/delete/', views.organizer_delete, name='organizer_delete'),

        # Gear URLs
    path('gears/', views.gear_list, name='gear_list'),
    path('gears/<int:gear_id>/', views.gear_detail, name='gear_detail'),
    path('gears/create/', views.gear_create, name='gear_create'),
    path('gears/<int:gear_id>/update/', views.gear_update, name='gear_update'),
    path('gears/<int:gear_id>/delete/', views.gear_delete, name='gear_delete'),

    # DiveComputer URLs
    path('dive_computers/', views.dive_computer_list, name='dive_computer_list'),
    path('dive_computers/<int:dive_computer_id>/', views.dive_computer_detail, name='dive_computer_detail'),
    path('dive_computers/create/', views.dive_computer_create, name='dive_computer_create'),
    path('dive_computers/<int:dive_computer_id>/update/', views.dive_computer_update, name='dive_computer_update'),
    path('dive_computers/<int:dive_computer_id>/delete/', views.dive_computer_delete, name='dive_computer_delete'),

    # Activity URLs
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/<int:activity_id>/', views.activity_detail, name='activity_detail'),
    path('activities/create/', views.activity_create, name='activity_create'),
    path('activities/<int:activity_id>/update/', views.activity_update, name='activity_update'),
    path('activities/<int:activity_id>/delete/', views.activity_delete, name='activity_delete'),

    # Participation URLs
    path('participations/', views.participation_list, name='participation_list'),
    path('participations/<int:participation_id>/', views.participation_detail, name='participation_detail'),
    path('participations/create/', views.participation_create, name='participation_create'),
    path('participations/<int:participation_id>/update/', views.participation_update, name='participation_update'),
    path('participations/<int:participation_id>/delete/', views.participation_delete, name='participation_delete'),
]
