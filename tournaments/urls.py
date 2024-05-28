from django.urls import path
from . import views
from .views import (tournament_table, team_list, login_user, logout_user,
                    tournament_detail, update_match, remove_team_from_tournament,
                    create_team, team_detail, join_team, profile_detail, edit_profile,
                    leave_team, open_close_register_tournament)


urlpatterns = [
    path('', login_user, name='login'),
    path('profile/', profile_detail, name='profile_detail'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/', logout_user, name='logout'),
    path('team_list/', team_list, name='team_list'),
    path('team_detail/<int:team_id>/', team_detail, name='team_detail'),
    path('join_team/<int:team_id>/', join_team, name='join_team'),
    path('leave_team/<int:team_id>/', leave_team, name='leave_team'),
    path('remove_team/<int:team_id>/', remove_team_from_tournament, name='remove_team_from_tournament'),
    path('tournament/', views.tournament_list, name='tournament_list'),
    path('tournament/<int:tournament_id>/register/', create_team, name='register_tournament'),
    path('tournament/<int:tournament_id>/detail/', tournament_detail, name='tournament_detail'),
    path('tournament/<int:tournament_id>/close_register/', open_close_register_tournament,
         name='open_close_register_tournament'),
    path('tournament/create/', views.create_tournament, name='create_tournament'),
    path('tournament/<int:tournament_id>/tournament_table/', tournament_table, name='tournament_table'),
    path('match/<int:match_id>/update/', update_match, name='update_match'),
]
