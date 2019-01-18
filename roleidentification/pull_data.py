import cassiopeia as cass
from cassiopeia import RoleGG
from .data import Role

# The Riot API, champion.gg, and this library all use different Role enums... Woo!
# We have to do some conversion.
role_conversion = {
    RoleGG.top: Role.top,
    RoleGG.jungle: Role.jungle,
    RoleGG.middle: Role.middle,
    RoleGG.adc: Role.adc,
    RoleGG.support: Role.support,
}


def get_data(filename=None):
    # If the value for a role is 0, that is somewhat noticeable in comparison to e.g. 0.1 == 10%
    # That means when we do the calculation, if the value for e.g. Support for e.g. Lux is value is really low but non-zero,
    # and Mid for Lux is very high in comparison to Corki (who has Support==0), then Corki will be assigned as support and Lux
    # as mid. By setting all 0's to -1, this ensures a champion never gets placed in a role they never play.
    # However, champion.gg only seems to record play rates above 10%, so we should distribute the unaccounted for data over
    # all the undefined roles.

    champions = cass.get_champions(region="NA")
    champion_roles = {}
    for champion in champions:
        champion.championgg.load()
        d = {role_conversion[role]: champion.championgg[role].play_rate for role in champion.championgg.roles}
        champion_roles[champion.id] = d

    for champion, play_rates in champion_roles.items():
        number_missing = 0
        missing_fraction = 1.
        for role in Role:
            if role not in play_rates:
                number_missing += 1
            else:
                missing_fraction -= champion_roles[champion][role]
        missing_per_uncounted_role = missing_fraction / number_missing
        for role in Role:
            if role not in play_rates:
                play_rates[role] = -1. + missing_per_uncounted_role

    return champion_roles
