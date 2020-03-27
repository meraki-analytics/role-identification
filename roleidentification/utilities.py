from roleidentification.get_roles import iterative_get_roles
from roleidentification.pull_data import pull_data
from cassiopeia import Champion, Position
from cassiopeia.core.match import Team


def get_team_roles(team: Team, champion_positions=None):
    if champion_positions is None:
        champion_positions = pull_data()
    champions = [participant.champion for participant in team.participants]
    smite = None
    for participant in team.participants:
        if participant.summoner_spell_d.id == 11 or participant.summoner_spell_f.id == 11:
            if smite is None:
                smite = participant.champion.name
            else:
                smite = None
    if smite is None:
        positions = iterative_get_roles(champion_positions, champions)
    else:
        positions = iterative_get_roles(champion_positions, champions, jungle=smite)
    return positions


def _print_results(match, team, positions):
    print('Top {T:<17} Jungle {J:<17} Mid {M:<17} Bottom {A:<17} Utility {S:<17}  (Match {match})'.format(
        T='{} ({}{})'.format(positions[Position.top], team.participants[positions[Position.top]].summoner_spell_d.name[0], team.participants[positions[Position.top]].summoner_spell_f.name[0]),
        J='{} ({}{})'.format(positions[Position.jungle], team.participants[positions[Position.jungle]].summoner_spell_d.name[0], team.participants[positions[Position.jungle]].summoner_spell_f.name[0]),
        M='{} ({}{})'.format(positions[Position.middle], team.participants[positions[Position.middle]].summoner_spell_d.name[0], team.participants[positions[Position.middle]].summoner_spell_f.name[0]),
        A='{} ({}{})'.format(positions[Position.bottom], team.participants[positions[Position.bottom]].summoner_spell_d.name[0], team.participants[positions[Position.bottom]].summoner_spell_f.name[0]),
        S='{} ({}{})'.format(positions[Position.utility], team.participants[positions[Position.utility]].summoner_spell_d.name[0], team.participants[positions[Position.utility]].summoner_spell_f.name[0]),
        match=match.id,
    ))
