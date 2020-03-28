import itertools
import copy
from typing import List


def highest_possible_playrate(champion_positions):
    maxes = {"TOP": 0.0, "JUNGLE": 0.0, "MIDDLE": 0.0, "BOTTOM": 0.0, "UTILITY": 0.0}
    for champion, rates in champion_positions.items():
        for position, rate in rates.items():
            if rate > maxes[position]:
                maxes[position] = rate
    return sum(maxes.values()) / len(maxes)


def calculate_metric(champion_positions, champions_by_position):
    return sum(champion_positions[champion][position] for position, champion in champions_by_position.items()) / len(champions_by_position)


def calculate_confidence(best_metric, second_best_metric):
    confidence = (best_metric - second_best_metric) / best_metric * 100
    return confidence


def get_positions(champion_positions, composition: List[int], top=None, jungle=None, middle=None, bottom=None, utility=None):
    # Check the types in `composition` and the other input types
    for i, champion in enumerate(composition):
        if not isinstance(champion, int):
            raise ValueError("The composition must be a list of champion IDs.")
    if (top is not None and not isinstance(top, int)) or \
            (jungle is not None and not isinstance(jungle, int)) or \
            (middle is not None and not isinstance(middle, int)) or \
            (bottom is not None and not isinstance(bottom, int)) or \
            (utility is not None and not isinstance(utility, int)):
        raise ValueError("The composition must be a list of champion IDs.")

    if None not in (top, jungle, middle, bottom, utility):
        raise ValueError("The composition was predefined by the kwargs.")

    # Set the initial guess to be the champion in the composition, order doesn't matter
    best_positions = {
        "TOP": composition[0],
        "JUNGLE": composition[1],
        "MIDDLE": composition[2],
        "BOTTOM": composition[3],
        "UTILITY": composition[4]
    }
    best_metric = calculate_metric(champion_positions, best_positions)
    second_best_metric = -float('inf')
    second_best_positions = None

    # Figure out which champions and positions we need to fill
    known_champions = [assigned for assigned in (top, jungle, middle, bottom, utility) if assigned is not None]
    unknown_champions = list(set(composition) - set(known_champions))
    unknown_positions = [position for position, assigned in zip(
        ("TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"),
        (top, jungle, middle, bottom, utility)
    ) if assigned is None]
    test_composition = {
        "TOP": top,
        "JUNGLE": jungle,
        "MIDDLE": middle,
        "BOTTOM": bottom,
        "UTILITY": utility
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
        confidence = calculate_confidence(best_metric, second_best_metric)
    else:
        confidence = 0.0

    return best_positions, best_metric, confidence, second_best_positions


def get_roles(champion_positions, composition: List[int], top=None, jungle=None, middle=None, bottom=None, utility=None):
    # Check the types in `composition` and the other input types
    for i, champion in enumerate(composition):
        if not isinstance(champion, int):
            raise ValueError("The composition must be a list of champion IDs.")
    if (top is not None and not isinstance(top, int)) or \
            (jungle is not None and not isinstance(jungle, int)) or \
            (middle is not None and not isinstance(middle, int)) or \
            (bottom is not None and not isinstance(bottom, int)) or \
            (utility is not None and not isinstance(utility, int)):
        raise ValueError("The composition must be a list of champion IDs.")

    identified = {}
    if top is not None:
        identified["TOP"] = top
    if jungle is not None:
        identified["JUNGLE"] = jungle
    if middle is not None:
        identified["MIDDLE"] = middle
    if bottom is not None:
        identified["BOTTOM"] = bottom
    if utility is not None:
        identified["UTILITY"] = utility

    if len(identified) >= len(composition):
        raise ValueError("The composition was predefined by the kwargs.")

    secondary_positions = None
    secondary_metric = -float('inf')
    while len(identified) < len(composition) - 1:
        kwargs = {position.lower(): champion for position, champion in identified.items()}
        positions, metric, confidence, sbp = get_positions(champion_positions, composition, **kwargs)
        if sbp is not None:
            _metric = calculate_metric(champion_positions, {position: champion for position, champion in sbp.items()})

            if secondary_positions is None:
                secondary_positions = sbp
                secondary_metric = _metric
            elif metric > _metric > secondary_metric:
                secondary_metric = _metric
                secondary_positions = sbp

        # Done! Grab the results.
        best = sorted([(position, champion) for position, champion in positions.items() if position not in identified],
                      key=lambda t: champion_positions[t[1]][t[0]], reverse=True)[0]
        identified[best[0]] = best[1]
        confidence = calculate_confidence(metric, secondary_metric)

    return positions
