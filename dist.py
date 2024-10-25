import pandas as pd
import math

# Total Aces and other cards in the remaining set
total_aces = 6
total_non_aces = 9
cards_per_player = 5

# Probability distribution for different possible counts of aces among players B, C, and D
distribution = {}
ace_count_dist = {}

# Calculate for 0 to 5 aces each for player B, C, and D under the constraint
for aces_b in range(cards_per_player + 1):
    for aces_c in range(cards_per_player + 1):
        for aces_d in range(cards_per_player + 1):
            # Total aces used by B, C, and D
            total_aces_used = aces_b + aces_c + aces_d

            # Only calculate if total used aces do not exceed total aces
            if total_aces_used <= total_aces:
                # Non-ace cards calculation
                non_aces_b = cards_per_player - aces_b
                non_aces_c = cards_per_player - aces_c
                non_aces_d = cards_per_player - aces_d
                total_non_aces_used = non_aces_b + non_aces_c + non_aces_d

                # Only consider valid distributions
                if total_non_aces_used == total_non_aces:
                    # Calculate combinations
                    ways_b = math.comb(total_aces, aces_b) * math.comb(
                        total_non_aces, non_aces_b
                    )
                    ways_c = math.comb(total_aces - aces_b, aces_c) * math.comb(
                        total_non_aces - non_aces_b, non_aces_c
                    )
                    ways_d = math.comb(
                        total_aces - aces_b - aces_c, aces_d
                    ) * math.comb(total_non_aces - non_aces_b - non_aces_c, non_aces_d)

                    # Total ways for this specific distribution
                    total_ways = ways_b * ways_c * ways_d

                    # Record distribution and count
                    distribution[(aces_b, aces_c, aces_d)] = total_ways
                    ace_count_dist[max(aces_b, aces_c, aces_d)] = (
                        ace_count_dist.get(max(aces_b, aces_c, aces_d), 0) + total_ways
                    )

# Create DataFrame to display results in sorted order
distribution_df = pd.DataFrame(
    list(distribution.items()), columns=["Ace Distribution (B, C, D)", "Ways"]
)
distribution_df["Probability"] = distribution_df["Ways"] / sum(distribution.values())
distribution_df = distribution_df.sort_values(
    by="Probability", ascending=False
).reset_index(drop=True)

print(distribution_df)
print(ace_count_dist)
