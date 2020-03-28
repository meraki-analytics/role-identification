def pull_data():
    import requests
    r = requests.get("http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/championrates.json")
    j = r.json()
    data = {}
    for champion_id, positions in j["data"].items():
        champion_id = int(champion_id)
        play_rates = {}
        for position, rates in positions.items():
            play_rates[position.upper()] = rates["playRate"]
        for position in ("TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"):
            if position not in play_rates:
                play_rates[position] = 0.0
        data[champion_id] = play_rates
    return data
