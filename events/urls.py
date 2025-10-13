# events/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Home
    path('', home, name='home'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # Event URLs
    path('events/', event_list, name='event_list'),
    path('event/<int:id>/', event_detail, name='event_detail'),
    path('event/new/', event_create, name='event_create'),
    path('event/<int:id>/edit/', event_update, name='event_update'),
    path('event/<int:id>/delete/', event_delete, name='event_delete'),
    
    # Category URLs
    path('categories/', category_list, name='category_list'),
    path('category/new/', category_create, name='category_create'),
    path('category/<int:id>/edit/', category_update, name='category_update'),
    path('category/<int:id>/delete/', category_delete, name='category_delete'),
    
    # Participant URLs
    path('participants/', participant_list, name='participant_list'),
    path('participant/new/', participant_create, name='participant_create'),
    path('participant/<int:id>/edit/', participant_update, name='participant_update'),
    path('participant/<int:id>/delete/', participant_delete, name='participant_delete'),
]