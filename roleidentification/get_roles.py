import sys
import itertools
import copy
from typing import List, Union

from .data import Role
from cassiopeia import Champion

from .pull_data import get_data


def get_roles(champion_roles, composition: List[Union[Champion, str, int]], top=None, jungle=None, middle=None, adc=None, support=None, verbose=False):
    """ Returns a dictionary with keys Top, Jungle, Middle, ADC, Support and values as names of the input champions. """
    if isinstance(composition[0], Champion):
        region = composition[0].region
    else:
        region = 'NA'
    if isinstance(composition[0], str):
        composition = [Champion(name=name, region='NA').id for name in composition]
    elif isinstance(composition[0], Champion):
        composition = [champion.id for champion in composition]
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
    if isinstance(adc, str):
        adc = Champion(name=adc, region='NA').id
    elif isinstance(adc, Champion):
        adc = adc.id
    if isinstance(support, str):
        support = Champion(name=support, region='NA').id
    elif isinstance(support, Champion):
        support = support.id

    second_best_metric = -float('inf')
    second_best_roles = None
    second_best_play_percents = None
    if None not in [top, jungle, middle, adc, support]:
        best_roles = {
            Role.top: top,
            Role.jungle: jungle,
            Role.middle: middle,
            Role.adc: adc,
            Role.support: support
        }
        best_play_percents = {
            top: champion_roles[top][Role.top],
            jungle: champion_roles[jungle][Role.jungle],
            middle: champion_roles[middle][Role.middle],
            adc: champion_roles[adc][Role.adc],
            support: champion_roles[support][Role.support],
        }
        best_metric = sum(v for v in best_play_percents.values())/5
    else:
        best_roles = {
            Role.top: composition[0],
            Role.jungle: composition[1],
            Role.middle: composition[2],
            Role.adc: composition[3],
            Role.support: composition[4]
        }
        best_play_percents = {
            composition[0]: champion_roles[composition[0]][Role.top],
            composition[1]: champion_roles[composition[1]][Role.jungle],
            composition[2]: champion_roles[composition[2]][Role.middle],
            composition[3]: champion_roles[composition[3]][Role.adc],
            composition[4]: champion_roles[composition[4]][Role.support],
        }
        best_metric = sum(v for v in best_play_percents.values())/5
        second_best_roles = {
            Role.top: composition[0],
            Role.jungle: composition[1],
            Role.middle: composition[2],
            Role.adc: composition[3],
            Role.support: composition[4]
        }
        second_best_play_percents = {
            composition[0]: champion_roles[composition[0]][Role.top],
            composition[1]: champion_roles[composition[1]][Role.jungle],
            composition[2]: champion_roles[composition[2]][Role.middle],
            composition[3]: champion_roles[composition[3]][Role.adc],
            composition[4]: champion_roles[composition[4]][Role.support],
        }
        second_best_metric = sum(v for v in best_play_percents.values())/5
        for champs in itertools.permutations(composition, 5):
            roles = {
                Role.top: champion_roles[champs[0]][Role.top],
                Role.jungle: champion_roles[champs[1]][Role.jungle],
                Role.middle: champion_roles[champs[2]][Role.middle],
                Role.adc: champion_roles[champs[3]][Role.adc],
                Role.support: champion_roles[champs[4]][Role.support],
            }
            if top is not None and champs[0] != top:
                continue
            if jungle is not None and champs[1] != jungle:
                continue
            if middle is not None and champs[2] != middle:
                continue
            if adc is not None and champs[3] != adc:
                continue
            if support is not None and champs[4] != support:
                continue

            metric = sum(v for v in roles.values())/5
            if metric > best_metric:
                second_best_metric = best_metric
                second_best_roles = best_roles
                best_metric = metric
                best_roles = {
                    Role.top: champs[0],
                    Role.jungle: champs[1],
                    Role.middle: champs[2],
                    Role.adc: champs[3],
                    Role.support: champs[4]
                }
                best_play_percents = {
                    champs[0]: champion_roles[champs[0]][Role.top],
                    champs[1]: champion_roles[champs[1]][Role.jungle],
                    champs[2]: champion_roles[champs[2]][Role.middle],
                    champs[3]: champion_roles[champs[3]][Role.adc],
                    champs[4]: champion_roles[champs[4]][Role.support],
                }
            if best_metric > metric > second_best_metric:
                second_best_metric = metric
                second_best_roles = {
                    Role.top: champs[0],
                    Role.jungle: champs[1],
                    Role.middle: champs[2],
                    Role.adc: champs[3],
                    Role.support: champs[4]
                }
                second_best_play_percents = {
                    champs[0]: champion_roles[champs[0]][Role.top],
                    champs[1]: champion_roles[champs[1]][Role.jungle],
                    champs[2]: champion_roles[champs[2]][Role.middle],
                    champs[3]: champion_roles[champs[3]][Role.adc],
                    champs[4]: champion_roles[champs[4]][Role.support],
                }

    if second_best_roles == best_roles:
        second_best_roles = None
        second_best_play_percents = None
        second_best_metric = -float('inf')
    count_bad_assignments = 0
    for value in best_play_percents.values():
        if value < 0:
            count_bad_assignments += 1

    count_secondary_bad_assignments = 0
    if second_best_play_percents:
        found_acceptable_alternative = True
        for value in second_best_play_percents.values():
            if value < 0:
                count_secondary_bad_assignments += 1
        #if count_secondary_bad_assignments > count_bad_assignments:
        #    found_acceptable_alternative = False
    else:
        found_acceptable_alternative = False

    confidence = (best_metric - second_best_metric)/best_metric

    if found_acceptable_alternative:
        string = []
        for role in [Role.top, Role.jungle, Role.middle, Role.adc, Role.support]:
            if best_roles[role] != second_best_roles[role]:
                string.append("{}: {}".format(role, second_best_roles[role]))
        alternative = ', '.join(string)
    else:
        alternative = None

    if verbose:
        # These commented lines below are useful for debugging
        #print("Best roles: {}".format(best_metric))
        #if second_best_metric > -float('inf'):
        #    print("Second best roles: {}".format(second_best_metric))
        #    for role, champ in second_best_roles.items():
        #        print("    {}: {} == {}".format(role, champ, champion_roles[champ][role]))
        #    for role, champion in best_roles.items():
        #        print(champion, champion_roles[champion])
        #    print('')

        for role in [Role.top, Role.jungle, Role.middle, Role.adc, Role.support]:
            print("{}: {}  ({}%)".format(role, best_roles[role].name, round(100.*champion_roles[best_roles[role]][role],2)))
        print("Probability: {}%".format(round(100.*best_metric, 1)))
        if not found_acceptable_alternative:
            print("Confidence: {}%".format(round(100.*confidence, 1)))
        else:
            print("Confidence: {}% (Alternative is {})".format(round(100.*confidence, 1), [champion.name for champion in alternative]))
        print('')
    best_roles = {role: Champion(id=id_, region=region) for role, id_ in best_roles.items()}
    if second_best_roles is not None:
        second_best_roles = {role: Champion(id=id_, region=region) for role, id_ in second_best_roles.items()}
    return best_roles, best_metric, confidence, second_best_roles


def iterative_get_roles(champion_roles, composition: List[Union[Champion, str, int]], top=None, jungle=None, middle=None, adc=None, support=None, verbose=False):
    fixed = {}
    if top is not None:
        fixed[Role.top] = top
    if jungle is not None:
        fixed[Role.jungle] = jungle
    if middle is not None:
        fixed[Role.middle] = middle
    if adc is not None:
        fixed[Role.adc] = adc
    if support is not None:
        fixed[Role.support] = support

    _champion_roles = copy.deepcopy(champion_roles)
    second_best_roles = None
    second_best_prob = -float('inf')
    while len(fixed) < 4:
        # Modify data
        for role in fixed:
            for champion, play_rates in _champion_roles.items():
                if champion in fixed.values():
                    continue
                play_rate = play_rates[role]
                play_rates[role] = -1.0
                if play_rate > 0:
                    roles_left = sum([1 for v in play_rates.values() if v > 0])
                    if roles_left > 0:
                        to_distribute = play_rate / roles_left
                    else:
                        to_distribute = 0.
                    for r in play_rates:
                        if play_rates[r] < 0:
                            continue
                        play_rates[r] += to_distribute
        _fixed = {role.name.lower(): champion for role, champion in fixed.items()}
        roles, prob, confidence, sbr = get_roles(_champion_roles, composition, **_fixed, verbose=False)
        if sbr is not None:
            _roles, _prob, _confidence, _ = get_roles(_champion_roles, composition, **{k.name.lower(): v for k, v in sbr.items()}, verbose=False)

            # I'm pretty sure `prob` can only increase with iterations of this loop
            if prob > _prob > second_best_prob:
                second_best_prob = _prob
                second_best_roles = sbr

        best = sorted([(role, champion) for role, champion in roles.items() if role not in fixed],
                      key=lambda t: _champion_roles[t[1].id][t[0]], reverse=True)[0]
        fixed[best[0]] = best[1]

    if verbose:
        for role in [Role.top, Role.jungle, Role.middle, Role.adc, Role.support]:
            print("{}: {}  ({}%)".format(role, roles[role].name, round(100.*champion_roles[roles[role].id][role], 2)))
        print("Probability: {}%".format(round(100. * prob, 1)))
        confidence = (prob - second_best_prob)/prob
        if not second_best_roles:
            print("Confidence: {}%".format(round(100. * confidence, 1)))
        else:
            string = []
            for role in [Role.top, Role.jungle, Role.middle, Role.adc, Role.support]:
                if roles[role] != second_best_roles[role]:
                    string.append("{}: {}".format(role, second_best_roles[role].name))
            alternative = ', '.join(string)
            print("Confidence: {}% (Alternative is {})".format(round(100. * confidence, 1), alternative))
        print()
    return roles, prob, confidence, second_best_roles
