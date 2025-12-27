from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('watch/<int:video_id>/', views.watch, name='watch'),
    path('shorts/<int:short_id>/', views.shorts, name='shorts'),
    path('explore/<str:category>/', views.explore, name='explore'),
]


