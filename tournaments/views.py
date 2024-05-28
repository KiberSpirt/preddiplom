from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TeamForm, ProfileForm, TeamRegistrationForm, TournamentForm
from .models import Tournament, Match, Team, Profile
from .utils import generate_tournament_schedule


def login_user(request):
    if request.user.is_authenticated:
        return redirect('tournament_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tournament_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tournament/login.html', {'form': form})


@login_required
def update_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.method == 'POST':
        match.match_date = request.POST.get('match_date')
        match.result = request.POST.get('result')
        match.save()
        return redirect('tournament/tournament_schedule', tournament_id=match.tournament.id)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def profile_detail(request):
    profile = Profile.objects.get(pk=request.user.pk)
    return render(request, 'tournament/profile_detail.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'tournament/profile_form.html', {'form': form})


@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'tournament/team_list.html', {'teams': teams, 'user': request.user})


@login_required
def create_team(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if tournament.teams.count() >= tournament.team_quantity:
        return render(request, 'tournament/create_team.html', {
            'form': None,
            'error_message': 'Регистрация закрыта. Достигнуто максимальное количество команд.'
        })

    if request.method == 'POST':
        form = TeamForm(request.POST, user=request.user)
        if form.is_valid():
            team = form.save(commit=False)
            team.save()
            team.members.add(request.user)
            tournament.teams.add(team)
            generate_tournament_schedule(tournament)
            return redirect('tournament_detail', tournament_id)
    else:
        form = TeamForm(user=request.user, initial={'tournament': tournament})

    return render(request, 'tournament/create_team.html', {'form': form})


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    tournament = team.tournament
    team_size = tournament.team_size
    members_count = team.members.count()
    return render(request, 'tournament/team_detail.html', {'team': team, 'team_size': team_size,
                                                           'members_count': members_count})


@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    user = request.user
    team.members.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    user = request.user

    if team.captain == user.username:
        team.delete()
    else:
        team.members.remove(user)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_team_from_tournament(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def register_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tournament_list')
    else:
        form = TeamRegistrationForm()
    return render(request, 'tournament/register.html', {'form': form, 'tournament': tournament})


@login_required
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    matches = generate_tournament_schedule(tournament)
    teams = Team.objects.filter(tournament_id=tournament_id).order_by('-points', '-wins', 'losses')
    return render(request, 'tournament/tournament_detail.html', {'tournament': tournament, 'matches': matches, 'teams': teams})


@login_required
def open_close_register_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    tournament.toggle_registration_status()
    return redirect('tournament_detail', tournament_id=tournament_id)


@login_required
def create_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            return redirect('tournament_list')
    else:
        form = TournamentForm()
    return render(request, 'tournament/create_tournament.html', {'form': form})


@login_required
def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournament/tournament_list.html', {'tournaments': tournaments})


@login_required
def tournament_table(request, tournament_id):
    teams = Team.objects.filter(tournament_id=tournament_id).order_by('-points', '-wins', 'losses')
    return render(request, 'tournament/tournament_table.html', {'teams': teams})
