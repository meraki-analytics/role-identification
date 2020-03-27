import sys

import cassiopeia as cass
from roleidentification import pull_data, get_roles, get_team_roles


def main():
    print("Pulling data...")
    champion_roles = pull_data()
    print("Finished pulling data.")
    print()

    if len(sys.argv) == 6:
        c1, c2, c3, c4, c5 = sys.argv[1:6]
        roles = get_roles(champion_roles, [c1, c2, c3, c4, c5])
    else:
        roles = get_roles(champion_roles, ['Darius', 'Lee Sin', 'Cassiopeia', 'Draven', 'Braum'])
    print({role.name: champion.name for role, champion in roles.items()})

    # Use the utility function `get_team_roles` to get the roles from a Cassiopeia.Match.Team object
    match = cass.get_match(id=3344134840, region="NA")
    team = match.blue_team
    roles = get_team_roles(team, champion_roles)
    print({role.name: champion.name for role, champion in roles.items()})


if __name__ == '__main__':
    main()
