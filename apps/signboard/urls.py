from django.urls import path

from . import views

urlpatterns = [
    path('signboards/<str:signboard_slug>/', views.signboard, name='signboard'),
    path('signboards/', views.signboards, name='signboards'),

    path('game/', views.game, name='game'),
]

