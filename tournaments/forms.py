from django import forms

from .models import Tournament, Team, Profile


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'captain', 'email']


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'description', 'team_quantity', 'team_size']


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'tournament', 'captain', 'email']

    tournament = forms.ModelChoiceField(queryset=Tournament.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TeamForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['captain'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['captain'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'country', 'city', 'faculty', 'study_group', 'speciality']
