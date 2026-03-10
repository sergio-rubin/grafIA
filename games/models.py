from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


class LearnScore(models.Model):
    """Score for grafIA Learn game"""
    player_name = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='El nombre solo puede contener letras, números y guiones bajos'
            )
        ]
    )
    score = models.IntegerField()
    error = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', 'created_at']

    def __str__(self):
        return f"{self.player_name}: {self.score}"


class GuessScore(models.Model):
    """Score for grafIA Guess game"""
    player_name = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='El nombre solo puede contener letras, números y guiones bajos'
            )
        ]
    )
    score = models.IntegerField()
    time_seconds = models.FloatField()
    precision = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', 'created_at']

    def __str__(self):
        return f"{self.player_name}: {self.score}"
