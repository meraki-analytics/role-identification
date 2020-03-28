from typing import List, Union

from roleidentification.get_roles import get_roles
from roleidentification.pull_data import pull_data
from cassiopeia import Champion, Position
from cassiopeia.core.match import Team


def get_champion_roles(composition: List[Union["Champion", str, int]], top=None, jungle=None, middle=None, bottom=None, utility=None, champion_roles=None):
    if champion_roles is None:
        champion_roles = pull_data()
    from cassiopeia import Champion

    # Shallow copy so we don't modify the list in-place
    composition = [champion for champion in composition]
    for i, champion in enumerate(composition):
        if isinstance(champion, str):
            composition[i] = Champion(name=champion, region='NA').id
        elif isinstance(champion, Champion):
            composition[i] = champion.id

    if isinstance(top, str):
        top = Champion(name=top, region='NA').id
    elif isinstance(top, Champion):
        top = top.id
    if isinstance(jungle, str):
        jungle = Champion(name=jungle, region='NA').id
    elif isinstance(jungle, Champion):
        jungle = jungle.id
    if isinstance(middle, str):
        middle = Champion(name=middle, region='NA').id
    elif isinstance(middle, Champion):
        middle = middle.id
    if isinstance(bottom, str):
        bottom = Champion(name=bottom, region='NA').id
    elif isinstance(bottom, Champion):
        bottom = bottom.id
    if isinstance(utility, str):
        utility = Champion(name=utility, region='NA').id
    elif isinstance(utility, Champion):
        utility = utility.id

    positions = get_roles(champion_roles, composition, top, jungle, middle, bottom, utility)
    positions = {Position(position): Champion(id=id_, region='NA') for position, id_ in positions.items()}
    return positions


def get_team_roles(team: Team, champion_roles=None):
    if champion_roles is None:
        champion_roles = pull_data()
    champions = [participant.champion.id for participant in team.participants]
    smite = None
    for participant in team.participants:
        if participant.summoner_spell_d.id == 11 or participant.summoner_spell_f.id == 11:
            if smite is None:
                smite = participant.champion.id
            else:
                smite = None

    if smite is None:
        positions = get_roles(champion_roles, champions)
    else:
        positions = get_roles(champion_roles, champions, jungle=smite)
    positions = {Position(position): Champion(id=id_, region='NA') for position, id_ in positions.items()}
    return positions
