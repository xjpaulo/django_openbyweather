from django.test import TestCase
from ..models import History


class HistoryTest(TestCase):

    def setUp(self):
        History.objects.create(city='Limeira', temperature=23, genre='Rock', playlist_url='http://www.spotify.com')
        History.objects.create(city='Campinas', temperature=23, genre='Pop', playlist_url='http://www.spotify.com')

    def test_get_genre(self):
        history_limeira = History.objects.get(city='Limeira')
        history_campinas = History.objects.get(city='Campinas')
        self.assertEqual(
            history_limeira.get_genre(), "Genre and temperature are correct!")
        self.assertEqual(
            history_campinas.get_genre(), "Incorrect genre for given temperature.")