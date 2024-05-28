from .models import Match


def generate_tournament_schedule(tournament):
    teams = list(tournament.teams.all())
    matches = []
    round_number = 1

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            match = Match(
                tournament=tournament,
                round_number=round_number,
                team1=teams[i],
                team2=teams[j],
                match_date=None
            )
            match.save()
            matches.append(match)
        round_number += 1

    return matches
