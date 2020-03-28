import copy


def pull_data():
    import cassiopeia as cass
    # If the value for a position is 0, that is somewhat noticeable in comparison to e.g. 0.1 == 10%
    # That means when we do the calculation, if the value for e.g. support for e.g. Lux is value is really low but non-zero,
    # and Mid for Lux is very high in comparison to Corki (who has support==0), then Corki will be assigned as support and Lux
    # as mid. By setting all 0's to -1, this ensures a champion never gets placed in a position they never play.
    # However, champion.gg only seems to record play rates above 10%, so we should distribute the unaccounted for data over
    # all the undefined positions.

    champions = cass.get_champions(region="NA")
    champion_positions = {}
    for champion in champions:
        rates = copy.deepcopy(champion.play_rates)
        transformed = {}
        for role, rate in rates.items():
            transformed[role.value] = rate
        champion_positions[champion.id] = transformed

    for champion, play_rates in champion_positions.items():
        for position in ("TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"):
            if position not in play_rates:
                play_rates[position] = 0.0

    for champion, play_rates in champion_positions.items():
        for value in play_rates.values():
            assert value >= 0

    return champion_positions
