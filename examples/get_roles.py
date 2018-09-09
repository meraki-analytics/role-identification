import sys
import itertools
import copy
from typing import List

from cassiopeia.data import Role
from cassiopeia import Champion, Champions
from roleidentification import get_data, get_roles


def main():
    print("Pulling data...")
    champion_roles = get_data()
    print("Finished pulling data.")
    print()

    if len(sys.argv) == 6:
        c1, c2, c3, c4, c5 = sys.argv[1:6]
        roles, prob, confidence, alternative = get_roles(champion_roles, [c1, c2, c3, c4, c5], verbose=True)
    else:
        roles, prob, confidence, alternative = get_roles(champion_roles, ['Galio', 'Maokai', 'Jarvan IV', 'Tristana', 'Tahm Kench'], verbose=True)
        roles, prob, confidence, alternative = get_roles(champion_roles, ['Brand', 'Caitlyn', 'Vi', 'Lulu', 'Cassiopeia'], verbose=True)


if __name__ == '__main__':
    main()
