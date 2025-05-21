from django.contrib import admin
from django.urls import path, include
from transactions.views import login, auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('auth/', auth, name='auth'),
    path('transactions/', include('transactions.urls'))
]
