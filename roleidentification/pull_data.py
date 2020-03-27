from cassiopeia import Position
import cassiopeia as cass


def pull_data(filename=None):
    # If the value for a position is 0, that is somewhat noticeable in comparison to e.g. 0.1 == 10%
    # That means when we do the calculation, if the value for e.g. support for e.g. Lux is value is really low but non-zero,
    # and Mid for Lux is very high in comparison to Corki (who has support==0), then Corki will be assigned as support and Lux
    # as mid. By setting all 0's to -1, this ensures a champion never gets placed in a position they never play.
    # However, champion.gg only seems to record play rates above 10%, so we should distribute the unaccounted for data over
    # all the undefined positions.

    champions = cass.get_champions(region="NA")
    champion_positions = {}
    for champion in champions:
        champion_positions[champion.id] = champion.play_rates

    for champion, play_rates in champion_positions.items():
        number_missing = 0
        missing_fraction = 1.
        for position in (Position.top, Position.jungle, Position.middle, Position.bottom, Position.utility):
            if position not in play_rates:
                number_missing += 1
            else:
                missing_fraction -= champion_positions[champion][position]
        missing_per_uncounted_position = missing_fraction / number_missing
        assert missing_per_uncounted_position >= 0
        for position in (Position.top, Position.jungle, Position.middle, Position.bottom, Position.utility):
            if position not in play_rates:
                play_rates[position] = 0  # missing_per_uncounted_position

    for champion, play_rates in champion_positions.items():
        for value in play_rates.values():
            assert value >= 0
    #    total = sum(play_rates.values())
    #    print(champion, total, play_rates)
    #    assert 0.99 < total < 1.01

    return champion_positions
