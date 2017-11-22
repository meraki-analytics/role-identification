## Role Identification for League of Legends

### Setup

Install from GitHub using pip:  `pip install git+https://github.com/meraki-analytics/role-identification.git`

This code uses [Cassiopeia](https://github.com/meraki-analytics/cassiopeia), which will also be installed if it isn't already.

### Example

    # Pull the data required to make role assignments
    champion_roles = get_data()

    # Create one of a summoner's match using Cassiopeia
    summoner = Summoner(name="Kalturi", region="NA")
    match = summoner.match_history[0]

    # Use this role identification code to get the blue team's roles
    roles = get_team_roles(match.blue_team, champion_roles)
    print({role.name: champion.name for role, champion in roles.items()})

    # Output:
    # {'top': 'Pantheon', 'jungle': 'Nunu', 'mid': 'Akali', 'adc': 'Caitlyn', 'support': 'Morgana'}

See the `examples` directory for more.


### Work-In-Progress

This code is a work in progress. It currently uses aggregated data from champion.gg to identify which champions play what roles. It then does a simple brute force calculation to identify the most likely lane assignment of each champion.

In the future, we will replace champion.gg's data and the brute force algorithm with a robust machine learning algorithm that takes into account the champion, summoner spells, and runes.