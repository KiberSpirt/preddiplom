from django.contrib import admin
from .models import Team, Tournament, Match, Profile

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Profile)
