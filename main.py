import tkinter as tk
from math import comb, factorial

# import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap


def multinomial_coefficient(total, counts):
    result = factorial(total)
    for count in counts:
        result //= factorial(count)
    return result


def calculate_probability(k, n):
    K_remaining = 6 - k
    Non_K_remaining = 9 + k
    Total_ways = factorial(15) // (factorial(5) ** 3)

    favorable_ways = 0

    # Generate all possible combinations of (k1, k2, k3)
    def generate_combinations(K_remaining):
        combinations = []
        for k1 in range(0, min(5, K_remaining) + 1):
            for k2 in range(0, min(5, K_remaining - k1) + 1):
                k3 = K_remaining - k1 - k2
                if 0 <= k3 <= 5:
                    combinations.append((k1, k2, k3))
        return combinations

    combinations = generate_combinations(K_remaining)

    for k1, k2, k3 in combinations:
        if max(k1, k2, k3) <= n:
            n1, n2, n3 = 5 - k1, 5 - k2, 5 - k3
            if min(n1, n2, n3) >= 0:
                ways_K = multinomial_coefficient(K_remaining, [k1, k2, k3])
                ways_NonK = multinomial_coefficient(Non_K_remaining, [n1, n2, n3])
                favorable_ways += ways_K * ways_NonK

    probability_no_opponent_exceeds_n = favorable_ways / Total_ways
    probability_at_least_one_exceeds_n = 1 - probability_no_opponent_exceeds_n

    return probability_at_least_one_exceeds_n


probability_results = {
    k: {n: calculate_probability(k, n) for n in range(6)} for k in range(6)
}

print(probability_results)


k_values = range(0, 6)
n_values = range(0, 6)

prob_matrix = np.zeros((len(n_values), len(k_values)))

for i, n in enumerate(n_values):
    for j, k in enumerate(k_values):
        prob = probability_results[k][n]
        prob_matrix[i, j] = prob

plt.figure(figsize=(8, 6))
sns.heatmap(
    prob_matrix,
    annot=True,
    fmt=".4f",
    cmap="YlGnBu",
    xticklabels=k_values,
    yticklabels=n_values,
)
plt.xlabel("k")
plt.ylabel("n")
plt.title("prob")
plt.show()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lier's Bar Assist")
        self.geometry("300x220")
        self.attributes("-topmost", False)

        # Variables
        self.bullets_float = []  # Float probability of *red* bullets
        self.bullets_state = []  # Int state of bullets
        # bullets_state: 0: default, 1: deemed red, 2: deemed black
        self.prob_map = probability_results

        # Slider Frame
        slider_frame = tk.Frame(self)
        slider_frame_mine = tk.Frame(slider_frame)
        self.place_slider_mine(slider_frame_mine)
        slider_frame_mine.grid(row=0, column=0, padx=10)
        slider_frame.pack(padx=10, pady=10)

        # Clear Button
        control_buttons_frame = tk.Frame(self)
        self.clear_button = tk.Button(control_buttons_frame, text="Clear")
        self.clear_button.config(state=tk.DISABLED)
        self.clear_button.grid(row=0, column=0, padx=10, pady=10)

        # Topmost Button
        self.topmost_button = tk.Button(
            control_buttons_frame,
            text="Pin",
            command=lambda: (
                self.attributes("-topmost", not self.attributes("-topmost")),
                self.topmost_button.config(
                    text="Unpin" if self.attributes("-topmost") else "Pin"
                ),
            ),
        )
        self.topmost_button.grid(row=0, column=1, padx=10, pady=10)
        control_buttons_frame.pack()

        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(padx=10, pady=10)
        self.stats_label = tk.Label(self.stats_frame, text="Statistics")
        self.stats_label.pack()

        # This is Lier's Bar
        return

        # Bullets Frame
        self.bullets_frame = tk.Frame(self)
        self.place_bullets()
        self.bullets_frame.pack(padx=10, pady=10)

        # Initialize bullets
        self.clear_bullets()

    def place_slider_mine(self, frame: tk.Frame):
        self.slider_label_mine = tk.Label(frame, text="My Cards")
        self.slider_label_mine.grid(row=0, column=0)
        self.slider_my_card = tk.Scale(frame, from_=0, to=5, orient="horizontal")
        self.slider_my_card.config(command=lambda _: self.place_stats())
        self.slider_my_card.set(4)
        self.slider_my_card.grid(row=1, column=0)

    def clear_bullets(self):
        for widget in self.bullets_frame.winfo_children():
            widget.destroy()
        l = self.slider_my_card.get() + self.slider_black.get()
        self.bullets_float = [-1 for _ in range(l)]
        self.bullets_state = [0 for _ in range(l)]
        self.update_bullets()
        self.place_bullets()

    def place_bullets(self):
        for i, e in enumerate(self.bullets_float):
            bullet_button = tk.Button(self.bullets_frame)
            display_index = (
                i + 1 if self.bullets_state[i] == 0 else " " + str(i + 1) + "*"
            )
            display_prob = (
                e if self.bullets_state[i] == 0 else self.bullets_state[i] % 2
            )
            bullet_button.config(text="{}\n{: .2f}".format(display_index, display_prob))
            bullet_button.config(fg="white" if display_prob > 0.5 else "white")
            bullet_button.config(font=("Arial", 12, "bold"))
            bullet_button.config(command=lambda i=i: self.flip_bullet(i))
            self.apply_color(display_prob, bullet_button)
            bullet_button.pack(side=tk.LEFT)

    def apply_color(self, e, bullet_button: tk.Button):
        # color = cm.Reds(float(e))
        cmap = LinearSegmentedColormap.from_list(
            "my_colormap", [(0, "grey"), (1, "red")], N=256
        )
        color = cmap(float(e))
        hex_color = colors.rgb2hex(color[:3])
        bullet_button.config(bg=hex_color)

    def flip_bullet(self, i):
        self.bullets_state[i] = (self.bullets_state[i] + 1) % 3
        for widget in self.bullets_frame.winfo_children():
            widget.destroy()
        self.update_bullets()
        self.place_bullets()

    def update_bullets(self):
        deemed_r = sum([1 for e in self.bullets_state if e == 1])
        deemed_b = sum([1 for e in self.bullets_state if e == 2])
        actual_r = self.slider_my_card.get()
        actual_b = self.slider_black.get()
        remaining_r = actual_r - deemed_r
        remaining_b = actual_b - deemed_b

        tentative_r_prob = (
            remaining_r / (remaining_r + remaining_b)
            if remaining_r + remaining_b != 0
            else actual_r / (actual_r + actual_b)
        )

        self.bullets_float = [
            (
                tentative_r_prob
                if self.bullets_state[i] == 0
                else self.bullets_state[i] % 2
            )
            for i in range(actual_r + actual_b)
        ]

    def calculate_stats(self):
        # Get my cards
        my_cards = self.slider_my_card.get()

        # Get probabilities for each n
        probabilities = self.prob_map[my_cards]

        # Print statistics for each n
        stats = ""
        for n, probability in probabilities.items():
            stats += f"Friend having {n} K's: {probability:.4f}\n"

        return stats

    def place_stats(self):
        self.stats_label.config(text=self.calculate_stats())


if __name__ == "__main__":
    app = App()
    app.mainloop()
