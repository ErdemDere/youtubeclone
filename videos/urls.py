from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.history, name='history'),
    path('', views.home, name='home'),
    path('watch/<int:video_id>/', views.watch, name='watch'),
    path('shorts/<int:short_id>/', views.shorts, name='shorts'),
    path('explore/<str:category>/', views.explore, name='explore'),
    path('liked-videos/', views.liked_videos, name='liked_videos'),
    path('toggle-like/', views.toggle_like, name='toggle_like'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('toggle-subscription/', views.toggle_subscription, name='toggle_subscription'),
    path('playlists/', views.playlists, name='playlists'),
    path('playlist/<str:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('watch-later/', views.watch_later, name='watch_later'),
    path('toggle-watch-later/', views.toggle_watch_later, name='toggle_watch_later'),
    path('profile/', views.profile, name='profile'),
]



