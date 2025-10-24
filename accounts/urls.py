from django.urls import path
from accounts.views import *

urlpatterns = [
    path('signup/', signUp, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', signout_view, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_view, name='activate'),
]