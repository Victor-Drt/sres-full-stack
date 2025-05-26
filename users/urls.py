from django.urls import path
from .views import login, logout_view, register


urlpatterns = [
    path('', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
]