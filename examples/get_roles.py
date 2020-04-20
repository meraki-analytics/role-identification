from roleidentification import pull_data, get_roles


def main():
    print("Pulling data...")
    champion_roles = pull_data()
    print("Finished pulling data.")
    print()

    champions = [122, 64, 69, 119, 201]  # ['Darius', 'Lee Sin', 'Cassiopeia', 'Draven', 'Braum']
    roles = get_roles(champion_roles, champions)
    print(roles)


if __name__ == "__main__":
    main()
