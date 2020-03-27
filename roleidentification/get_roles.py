import itertools
import copy
from typing import List, Union

from cassiopeia import Champion, Position


def highest_possible_playrate(champion_positions):
    maxes = {Position.top: 0.0, Position.jungle: 0.0, Position.middle: 0.0, Position.bottom: 0.0, Position.utility: 0.0}
    for champion, rates in champion_positions.items():
        for position, rate in rates.items():
            if rate > maxes[position]:
                maxes[position] = rate
    return sum(maxes.values()) / len(maxes)


def calculate_metric(champion_positions, champions_by_position):
    return sum(champion_positions[champion][position] for position, champion in champions_by_position.items()) / len(champions_by_position)


def calculate_confidence(champion_positions, best_metric, second_best_metric):
    #hpp = highest_possible_playrate(champion_positions)
    #lpp = 0.0
    #confidence = (best_metric - second_best_metric) / (hpp - lpp) * 100
    confidence = (best_metric - second_best_metric) / best_metric * 100
    return confidence


def get_positions(champion_positions, composition: List[Union[Champion, str, int]], top=None, jungle=None, middle=None, bottom=None, utility=None):
    # Check the types in `composition
    for i, champion in enumerate(composition):
        if isinstance(champion, str):
            composition[i] = Champion(name=champion, region='NA').id
        elif isinstance(champion, Champion):
            composition[i] = champion.id

    # Check the other input types
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

    if None not in (top, jungle, middle, bottom, utility):
        raise ValueError("The composition was predefined by the kwargs.")

    # Set the initial guess to be the champion in the composition, order doesn't matter
    best_positions = {
        Position.top: composition[0],
        Position.jungle: composition[1],
        Position.middle: composition[2],
        Position.bottom: composition[3],
        Position.utility: composition[4]
    }
    best_metric = calculate_metric(champion_positions, best_positions)
    second_best_metric = -float('inf')
    second_best_positions = None

    # Figure out which champions and positions we need to fill
    known_champions = [assigned for assigned in (top, jungle, middle, bottom, utility) if assigned is not None]
    unknown_champions = list(set(composition) - set(known_champions))
    unknown_positions = [position for position, assigned in zip(
        (Position.top, Position.jungle, Position.middle, Position.bottom, Position.utility),
        (top, jungle, middle, bottom, utility)
    ) if assigned is None]
    test_composition = {
        Position.top: top,
        Position.jungle: jungle,
        Position.middle: middle,
        Position.bottom: bottom,
        Position.utility: utility
    }
    # Iterate over the positions we need to fill and record how well each composition "performs"
    for champs in itertools.permutations(unknown_champions, len(unknown_positions)):
        for i, position in enumerate(unknown_positions):
            test_composition[position] = champs[i]

        metric = calculate_metric(champion_positions, test_composition)
        if metric > best_metric:
            second_best_metric = best_metric
            second_best_positions = best_positions
            best_metric = metric
            best_positions = copy.deepcopy(test_composition)

        if best_metric > metric > second_best_metric:
            second_best_metric = metric
            second_best_positions = copy.deepcopy(test_composition)

    best_play_percents = {champion: champion_positions[champion][position] for position, champion in best_positions.items()}
    if second_best_positions is not None:
        second_best_play_percents = {champion: champion_positions[champion][position] for position, champion in second_best_positions.items()}
    else:
        second_best_play_percents = None

    if second_best_positions == best_positions:
        second_best_positions = None
        second_best_play_percents = None
        second_best_metric = -float('inf')
    count_bad_assignments = 0
    for value in best_play_percents.values():
        if value < 0:
            count_bad_assignments += 1

    found_acceptable_alternative = (second_best_play_percents is not None)

    if found_acceptable_alternative:
        confidence = calculate_confidence(champion_positions, best_metric, second_best_metric)
    else:
        confidence = 0.0

    best_positions = {position: Champion(id=id_, region='NA') for position, id_ in best_positions.items()}
    if second_best_positions is not None:
        second_best_positions = {position: Champion(id=id_, region='NA') for position, id_ in second_best_positions.items()}
    return best_positions, best_metric, confidence, second_best_positions


def iterative_get_roles(champion_positions, composition: List[Union[Champion, str, int]], top=None, jungle=None, middle=None, bottom=None, utility=None):
    identified = {}
    if top is not None:
        identified[Position.top] = top
    if jungle is not None:
        identified[Position.jungle] = jungle
    if middle is not None:
        identified[Position.middle] = middle
    if bottom is not None:
        identified[Position.bottom] = bottom
    if utility is not None:
        identified[Position.utility] = utility

    if len(identified) >= len(composition):
        raise ValueError("The composition was predefined by the kwargs.")

    secondary_positions = None
    secondary_metric = -float('inf')
    while len(identified) < len(composition) - 1:
        kwargs = {position.name.lower(): champion for position, champion in identified.items()}
        positions, metric, confidence, sbp = get_positions(champion_positions, composition, **kwargs)
        if sbp is not None:
            _metric = calculate_metric(champion_positions, {position: champion.id for position, champion in sbp.items()})

            if secondary_positions is None:
                secondary_positions = sbp
                secondary_metric = _metric
            elif metric > _metric > secondary_metric:
                secondary_metric = _metric
                secondary_positions = sbp

        # Done! Grab the results.
        best = sorted([(position, champion) for position, champion in positions.items() if position not in identified],
                      key=lambda t: champion_positions[t[1].id][t[0]], reverse=True)[0]
        identified[best[0]] = best[1]
        confidence = calculate_confidence(champion_positions, metric, secondary_metric)

    return positions
