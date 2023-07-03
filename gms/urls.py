from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('', views.index, name='login'),
    # path('reservations', views.reservations, name='reservations'),
    path('reservations/', views.ReservationListView.as_view(), name='reservations'),
    path('check-in/', views.process_checkin, name='check-in'),
    path('upload/', views.upload, name='upload'),
    path('upload_details/', views.manual_ingest, name='upload_details'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_checkin, name='search'),
]

