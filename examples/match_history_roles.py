from cassiopeia import Summoner, Champion
from roleidentification import pull_data
from roleidentification.utilities import get_champion_roles, get_team_roles


def main():
    # Pull the data
    champion_roles = pull_data()

    # Use individual champions
    darius = Champion(name='Darius', region='NA')
    leesin = Champion(name='Lee Sin', region='NA')
    syndra = Champion(name='Syndra', region='NA')
    draven = Champion(name='Draven', region='NA')
    braum = Champion(name='Braum', region='NA')
    champions = [darius, leesin, syndra, draven, braum]

    roles = get_champion_roles(champions, top=darius, champion_roles=champion_roles)
    print({role.name: champion.name for role, champion in roles.items()})


    # Use Cassiopeia's match.blue_team and/or match.red_team objects
    summoner = Summoner(name="Kalturi", region="NA")
    for match in summoner.match_history:
        roles = get_team_roles(match.blue_team, champion_roles)
        print({role.name: champion.name for role, champion in roles.items()})

        roles = get_team_roles(match.red_team, champion_roles)
        print({role.name: champion.name for role, champion in roles.items()})

        break


if __name__ == "__main__":
    main()
