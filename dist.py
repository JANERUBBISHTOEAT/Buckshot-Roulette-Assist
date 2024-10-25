import math
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Total Aces and other cards in the remaining set
total = 20
total_a = 6
total_na = total - total_a
per_player = 5


# Calculate for n aces for player BCD given k aces for player A
def dist_given_a(a_A):

    # distribution = {}
    ace_count_dist_given_a = {}

    for a_B, a_C, a_D in product(range(per_player + 1), repeat=3):
        # Save for later
        total_aces_used = a_A + a_B + a_C + a_D

        # Trim invalid distributions
        if total_aces_used > total_a:
            continue  # early return

        # Non-ace cards
        na_A = per_player - a_A
        na_B = per_player - a_B
        na_C = per_player - a_C
        na_D = per_player - a_D
        total_non_aces_used = na_A + na_B + na_C + na_D

        # Trim invalid distributions
        if total_non_aces_used != total_na:
            continue

        # Combinations
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


PMF = {}

for aces_a in range(per_player + 1):
    PMF[aces_a] = dist_given_a(aces_a)

print(PMF)


# Plotting
k_values = range(0, 6)
n_values = range(0, 6)

CDF_matrix = np.zeros((len(n_values), len(k_values)))
PMF_matrix = np.zeros((len(n_values), len(k_values)))


for k in k_values:
    acc_ways = 0
    total_ways = sum(PMF.get(k, {}).values())
    for n in reversed(n_values):
        ways = PMF.get(k, {}).get(n, 0)
        acc_ways += ways
        CDF_matrix[n, k] = acc_ways / total_ways
        PMF_matrix[n, k] = ways / total_ways


def CDF_heatmap():
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        CDF_matrix,
        annot=True,
        fmt=".4f",
        cmap="YlGnBu",
        xticklabels=k_values,
        yticklabels=n_values,
    )
    plt.xlabel("k")
    plt.ylabel("n")
    plt.title("CDF")
    # plt.savefig("CDF.png", dpi=600)
    plt.show()


def PMF_heatmap():
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        PMF_matrix,
        annot=True,
        fmt=".4f",
        cmap="YlGnBu",
        xticklabels=k_values,
        yticklabels=n_values,
    )
    plt.xlabel("k")
    plt.ylabel("n")
    plt.title("PMF")
    # plt.savefig("PMF.png", dpi=600)
    plt.show()


def close_plt():
    plt.close()


# CDF_heatmap()
# PMF_heatmap()
