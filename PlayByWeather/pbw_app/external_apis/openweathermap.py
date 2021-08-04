from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests


def openweathermap_temperature(city):
    query = {'q': city, 'units': 'metric', 'appid': settings.OPENWEATHER}
    try:
        response = requests.get('http://api.openweathermap.org/data/2.5/weather', params=query)
        json_response = response.json()
        temperature = json_response['main']['temp']
    except requests.exceptions.RequestException as e:
        error_message = 'An error occurred when retrieving the weather information: ' + str(e)
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'error': 'City not found!'}, status=status.HTTP_404_NOT_FOUND)
    return temperature
