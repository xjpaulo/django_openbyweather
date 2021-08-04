from rest_framework.decorators import api_view
from rest_framework.response import Response
from .external_apis.openweathermap import openweathermap_temperature
from .external_apis.spotify import spotify_auth, spotify_playlists, spotify_tracks
from .serializers import HistorySerializer
from .models import History
from rest_framework import status, generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView


def get_genre(temperature):
    if temperature > 25:
        genre = 'pop'
    elif 10 <= temperature <= 25:
        genre = 'rock'
    else:
        genre = 'classical'
    return genre


@api_view(['GET'])
def api_root(request):
    return Response({'error': 'Please use a valid endpoint.'}, status=status.HTTP_404_NOT_FOUND)


class GetPlaylists(APIView):
    @method_decorator(cache_page(60))
    def get(self, request, city):
        temperature = openweathermap_temperature(city)
        if type(temperature) == Response:
            return temperature
        genre = get_genre(temperature)
        access_token = spotify_auth()
        if type(access_token) == Response:
            return access_token
        playlist_url = spotify_playlists(access_token, genre)
        if type(playlist_url) == Response:
            return playlist_url
        tracks = spotify_tracks(access_token, playlist_url)
        if type(tracks) == Response:
            return playlist_url
        output = {
            'results': {
                'header': {
                    'city': city,
                    'temperatureCelcius': temperature,
                    'playlistGenre': genre,
                },
                'tracks': None
            }
        }
        output['results'].update(tracks)
        data = {
            'city': city,
            'temperature': temperature,
            'genre': genre,
            'playlist_url': playlist_url
        }
        serializer = HistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(output)
        return Response(serializer.errors)


class HistoryViewSet(generics.ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def list(self, request):
        queryset = self.get_queryset()
        if queryset:
            serializer = HistorySerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "No results found."}, status=status.HTTP_404_NOT_FOUND)

