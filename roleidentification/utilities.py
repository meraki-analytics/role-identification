from roleidentification.get_roles import iterative_get_roles, get_data, Role
from cassiopeia import Champion
from cassiopeia.core.match import Team


def _get_team_roles(team: Team, champion_roles=None):
    if champion_roles is None:
        champion_roles = get_data()
    champions = [participant.champion for participant in team.participants]
    smite = None
    for participant in team.participants:
        if participant.summoner_spell_d.id == 11 or participant.summoner_spell_f.id == 11:
            if smite is None:
                smite = participant.champion.name
            else:
                smite = None
    if smite is None:
        roles, prob, confidence, second_best_roles = iterative_get_roles(champion_roles, champions)
    else:
        roles, prob, confidence, second_best_roles = iterative_get_roles(champion_roles, champions, jungle=smite)
    prob = round(prob * 100, 1)
    prob = str(prob)
    while len(prob) < 4:
        prob += '0'
    confidence = round(confidence * 100, 1)
    confidence = str(confidence)
    while len(confidence) < 5:
        confidence += '0'
    return roles, prob, confidence, second_best_roles


def get_team_roles(team: Team, champion_roles=None):
    roles = _get_team_roles(team, champion_roles)[0]
    return roles


def _print_results(match, team, roles, prob, confidence, second_best_roles=None):
    if second_best_roles is not None:
        string = []
        for role in Role:
            if roles[role] != second_best_roles[role]:
                string.append("{}: {}".format(role, second_best_roles[role]))
        alternative = ', '.join(string)
    else:
        alternative = None
    print('Probability: {prob}%  Confidence: {conf}%;  Top {T:<17} Jungle {J:<17} Mid {M:<17} ADC {A:<17} Support {S:<17}  (Match {match}) ({alt})'.format(
        prob=prob, conf=confidence,
        T='{} ({}{})'.format(roles[Role.top], team.participants[roles[Role.top]].summoner_spell_d.name[0], team.participants[roles[Role.top]].summoner_spell_f.name[0]),
        J='{} ({}{})'.format(roles[Role.jungle], team.participants[roles[Role.jungle]].summoner_spell_d.name[0], team.participants[roles[Role.jungle]].summoner_spell_f.name[0]),
        M='{} ({}{})'.format(roles[Role.middle], team.participants[roles[Role.middle]].summoner_spell_d.name[0], team.participants[roles[Role.middle]].summoner_spell_f.name[0]),
        A='{} ({}{})'.format(roles[Role.adc], team.participants[roles[Role.adc]].summoner_spell_d.name[0], team.participants[roles[Role.adc]].summoner_spell_f.name[0]),
        S='{} ({}{})'.format(roles[Role.support], team.participants[roles[Role.support]].summoner_spell_d.name[0], team.participants[roles[Role.support]].summoner_spell_f.name[0]),
        match=match.id,
        alt=alternative,
    ))
