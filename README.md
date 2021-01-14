## Role Identification for League of Legends

### Setup

Install from GitHub using pip: `pip install git+https://github.com/meraki-analytics/role-identification.git`

This code can be used in [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) `Match` objects.

### Example Using Champion IDs

    # Pull the data required to make role assignments
    champion_roles = get_data()

    # You can pass in a list of champions to `get_roles`
    champions = [122, 64, 69, 119, 201]  # ['Darius', 'Lee Sin', 'Cassiopeia', 'Draven', 'Braum']
    roles = get_roles(champion_roles, champions)

    # Output:
    {'TOP': 122, 'JUNGLE': 64, 'MIDDLE': 69, 'BOTTOM': 119, 'UTILITY': 201}

### Example Using Cassiopeia

    # Or you can use the utility function `get_team_roles` to get the roles from a Cassiopeia.Match.Team object
    # Pull a summoner's most recent match using Cassiopeia
    match = cass.get_match(id=3344134840, region="NA")
    team = match.blue_team
    # Get the roles
    roles = get_team_roles(team, champion_roles)

    # Print the results
    print({role.name: champion.name for role, champion in roles.items()})

    # Output:
    # {'TOP': 'Darius', 'JUNGLE': 'Lee Sin', 'MIDDLE': 'Cassiopeia', 'BOTTOM': 'Draven', 'UTILITY': 'Braum'}

See the `examples` directory for more.
