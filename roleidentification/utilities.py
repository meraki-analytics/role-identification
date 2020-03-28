from roleidentification.get_roles import iterative_get_roles
from roleidentification.pull_data import pull_data
from cassiopeia import Champion, Position
from cassiopeia.core.match import Team


def get_team_roles(team: Team, champion_positions=None):
    if champion_positions is None:
        champion_positions = pull_data()
    champions = [participant.champion.id for participant in team.participants]
    smite = None
    for participant in team.participants:
        if participant.summoner_spell_d.id == 11 or participant.summoner_spell_f.id == 11:
            if smite is None:
                smite = participant.champion.id
            else:
                smite = None

    if smite is None:
        positions = iterative_get_roles(champion_positions, champions)
    else:
        positions = iterative_get_roles(champion_positions, champions, jungle=smite)
    positions = {Position(position): Champion(id=id_, region='NA') for position, id_ in positions.items()}
    return positions
