from django.urls import path

from . import views

urlpatterns = [
    path('games/', views.list_all_games_view),
]
