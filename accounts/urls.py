from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache
from . import views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('login/', views.login, name='gms_login'),
]