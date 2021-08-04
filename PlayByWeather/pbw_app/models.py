from django.db import models


class History(models.Model):
    city = models.CharField(max_length=255)
    temperature = models.FloatField()
    genre = models.CharField(max_length=255)
    playlist_url = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)

    def get_genre(self):
        if self.temperature > 25:
            if self.genre != 'Pop':
                return 'Incorrect genre for given temperature.'
            else:
                return 'Genre and temperature are correct!'
        elif self.temperature >= 10 and self.temperature <= 25:
            if self.genre != 'Rock':
                return 'Incorrect genre for given temperature.'
            else:
                return 'Genre and temperature are correct!'
        else:
            if self.genre != 'Classical':
                return 'Incorrect genre for given temperature.'
            else:
                return 'Genre and temperature are correct!'

    def __repr__(self):
        return 'History is added.'
