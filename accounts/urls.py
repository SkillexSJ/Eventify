from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import *

urlpatterns = [
    path('signup/', signUp, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/',signout_view , name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_view, name='activate'),
]