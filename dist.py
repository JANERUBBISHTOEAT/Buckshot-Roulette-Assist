import pandas as pd
import math
from itertools import product

# Total Aces and other cards in the remaining set
total = 20
total_a = 6
total_na = total - total_a
per_player = 5


# Calculate for 0 to 5 aces each for player B, C, and D under the constraint
def dist_given_a(a_A):

    # distribution = {}
    ace_count_dist_given_a = {}

    for a_B, a_C, a_D in product(range(per_player + 1), repeat=3):
        # Total aces used by B, C, and D
        total_aces_used = a_A + a_B + a_C + a_D

        # Only calculate if total used aces do not exceed total aces
        if total_aces_used > total_a:
            continue  # early return reduces indentation

        # Non-ace cards calculation
        na_A = per_player - a_A
        na_B = per_player - a_B
        na_C = per_player - a_C
        na_D = per_player - a_D
        total_non_aces_used = na_A + na_B + na_C + na_D

        # Only consider valid distributions
        if total_non_aces_used != total_na:
            continue

        # Calculate combinations
        ways_b = math.comb(total_a, a_B) * math.comb(total_na, na_B)
        ways_c = math.comb(total_a - a_B, a_C) * math.comb(total_na - na_B, na_C)
        ways_d = math.comb(total_a - a_B - a_C, a_D) * math.comb(
            total_na - na_B - na_C, na_D
        )

        # Total ways for this specific distribution
        total_ways = ways_b * ways_c * ways_d

        # Record distribution and count
        # distribution[(aces_b, aces_c, aces_d)] = total_ways
        ace_count_dist_given_a[max(a_B, a_C, a_D)] = (
            ace_count_dist_given_a.get(max(a_B, a_C, a_D), 0) + total_ways
        )

    print(a_A, ace_count_dist_given_a)
    return ace_count_dist_given_a


ace_count_dist = {}

for aces_a in range(per_player + 1):
    ace_count_dist[aces_a] = dist_given_a(aces_a)

print(ace_count_dist)
