from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import random


def spotify_auth():
    url = 'https://accounts.spotify.com/api/token'
    spotify_client_id = settings.SPOTIFY_CLIENT_ID
    spotify_client_secret = settings.SPOTIFY_SECRET_ID
    data = {
        'grant_type': 'client_credentials'
    }

    try:
        response_spotify = requests.post(url, auth=(spotify_client_id, spotify_client_secret), data=data)
    except requests.exceptions.RequestException as e:
        error_message = 'An error occurred when authenticating to Spotify: ' + str(e)
        return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)
    if response_spotify.status_code != 200:
        return Response({'error': 'An error occurred when authenticating to Spotify, check your credentials.'}, response_spotify.status_code)
    json_response_spotify = response_spotify.json()
    access_token = json_response_spotify.get('access_token')
    if access_token:
        return access_token
    return Response({'error': 'An error occurred when authenticating to Spotify.'}, status=status.HTTP_401_UNAUTHORIZED)


def spotify_playlists(access_token, genre):
    url = 'https://api.spotify.com/v1/browse/categories/' + genre + '/playlists'
    random_offset = random.randint(0, 19)
    payload = {
        'country': 'BR',
        'limit': '1',
        'offset': random_offset
    }
    headers = {
        'Authorization': "Bearer " + access_token
    }

    try:
        response_spotify = requests.get(url, params=payload, headers=headers)
    except requests.exceptions.RequestException as e:
        error_message = 'An error occurred when retrieving the playlists: ' + str(e)
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    if response_spotify.status_code != 200:
        return Response({'error': 'An error occurred when retrieving the playlists.'}, response_spotify.status_code)
    json_response_spotify = response_spotify.json()
    playlist_url = json_response_spotify['playlists']['items'][0]['tracks']['href']
    if playlist_url:
        return playlist_url
    return Response({'error': 'An error occurred when retrieving the playlists.'}, status=status.HTTP_400_BAD_REQUEST)


def spotify_tracks(access_token, playlist_url):
    headers = {
        'Authorization': "Bearer " + access_token
    }

    try:
        response_spotify = requests.get(playlist_url, headers=headers)
    except requests.exceptions.RequestException as e:
        error_message = 'An error occurred when retrieving the tracks from the playlist: ' + str(e)
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    if response_spotify.status_code != 200:
        return Response({'error': 'An error occurred when retrieving the tracks from the playlist.'}, response_spotify.status_code)
    json_response_spotify = response_spotify.json()
    tracks_json = json_response_spotify["items"]
    tracks = {'tracks': []}
    x = 0
    for item in tracks_json:
        artists_json = json_response_spotify['items'][x]['track']['artists']
        track_artists = []
        for artist in artists_json:
            track_artists.append(artist['name'])
        track_name = json_response_spotify['items'][x]['track']['name']
        track_artists_final = ', '.join(track_artists)
        tracks['tracks'].append({
            'trackArtist': track_artists_final,
            'trackName': track_name
        })
        x += 1
    return tracks
