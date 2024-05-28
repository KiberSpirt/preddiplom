
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Profile(AbstractUser):
    USER_ROLES = (
        ('admin', 'Administrator'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    study_group = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    team_quantity = models.PositiveIntegerField()
    team_size = models.PositiveIntegerField()
    is_close_for_register = models.BooleanField(default=False)
    teams = models.ManyToManyField('Team', blank=True, related_name='tournaments_set')

    def __str__(self):
        return self.name

    def toggle_registration_status(self):
        self.is_close_for_register = not self.is_close_for_register
        self.save()


class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='team_set')
    members = models.ManyToManyField(Profile, related_name='teams', blank=True)
    name = models.CharField(max_length=100)
    captain = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    round_number = models.IntegerField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team2')
    result = models.CharField(max_length=100, null=True, blank=True)
    match_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"

#TODO кнопки деактив если в одной команде
#TODO турнирная сетка
