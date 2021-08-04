from django.urls import include, path
from . import views
from .views import HistoryViewSet, GetPlaylists


urlpatterns = [
    path('api/v1/playlists/cities/<city>/', GetPlaylists.as_view(), name='Get Playlists'),
    path('api/v1/playlists/history/', HistoryViewSet.as_view(), name='History'),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.api_root)
]