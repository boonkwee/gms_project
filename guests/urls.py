from django.urls import path
from .views import GuestListView

urlpatterns = [
    path('', GuestListView.as_view(), name='guests')
]