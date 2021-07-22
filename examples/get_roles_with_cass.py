import cassiopeia as cass
from roleidentification import pull_data
from roleidentification.utilities import get_team_roles

API_KEY = "your key here"

def main():
    print("Pulling data...")
    champion_roles = pull_data()
    print("Finished pulling data.")
    print()

    # Pull a summoner's most recent match using Cassiopeia
    cass.set_riot_api_key(API_KEY)
    match = cass.get_match(id=3344134840, region="NA")
    team = match.blue_team
    # Get the roles
    roles = get_team_roles(team, champion_roles)

    # Print the results
    print({role.name: champion.name for role, champion in roles.items()})

    # Output:
    # {'top': 'Darius', 'jungle': 'Lee Sin', 'middle': 'Cassiopeia', 'bottom': 'Draven', 'utility': 'Braum'}


if __name__ == "__main__":
    main()
