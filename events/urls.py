
from django.urls import path
from .views import *

urlpatterns = [
    # Home
    path('', home, name='home'),
    
    # error page
    path('no-permission/', permission_denied_view, name='no_permission'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/organizer/', organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/participant/', participant_dashboard, name='participant_dashboard'),
    
    # Event
    path('events/', event_list, name='event_list'),
    path('event/<int:id>/', event_detail, name='event_detail'),
    path('event/new/', event_create, name='event_create'),
    path('event/<int:id>/edit/', event_update, name='event_update'),
    path('event/<int:id>/delete/', event_delete, name='event_delete'),
    
    # RSVP
    path('event/<int:id>/rsvp/', event_rsvp, name='event_rsvp'),
    path('event/<int:id>/cancel-rsvp/', event_cancel_rsvp, name='event_cancel_rsvp'),
    
    # Category
    path('categories/', category_list, name='category_list'),
    path('category/new/', category_create, name='category_create'),
    path('category/<int:id>/edit/', category_update, name='category_update'),
    path('category/<int:id>/delete/', category_delete, name='category_delete'),
]