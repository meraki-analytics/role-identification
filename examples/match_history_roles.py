from cassiopeia import Summoner

from roleidentification.get_roles import get_data
from roleidentification.utilities import get_team_roles


def main():
    champion_roles = get_data()

    summoner = Summoner(name="Kalturi", region="NA")
    for match in summoner.match_history:
        roles = get_team_roles(match.blue_team, champion_roles)
        print({role.name: champion.name for role, champion in roles.items()})

        roles = get_team_roles(match.red_team, champion_roles)
        print({role.name: champion.name for role, champion in roles.items()})
    return


if __name__ == "__main__":
    main()
