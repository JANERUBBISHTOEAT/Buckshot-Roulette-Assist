import tkinter as tk
from math import factorial

from dist import CDF_heatmap, CDF_matrix, PMF_heatmap, PMF_matrix, close_plt


def multinomial_coefficient(total, counts):
    result = factorial(total)
    for count in counts:
        result //= factorial(count)
    return result


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lier's Bar Assist")
        self.geometry("300x220")
        self.attributes("-topmost", False)

        # Variables
        self.heatmap_on = False

        # Slider Frame
        slider_frame = tk.Frame(self)
        slider_frame_mine = tk.Frame(slider_frame)
        self.place_slider_mine(slider_frame_mine)
        slider_frame_mine.grid(row=0, column=0, padx=10)
        slider_frame.pack(padx=10, pady=10)

        # CDF Button
        control_buttons_frame = tk.Frame(self)
        self.clear_button = tk.Button(
            control_buttons_frame, text="CDF", command=self.CDF_handler
        )
        self.clear_button.grid(row=0, column=0, padx=10, pady=10)

        # PMF Button
        self.clear_button = tk.Button(
            control_buttons_frame, text="PMF", command=self.PMF_handler
        )
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)

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
        self.topmost_button.grid(row=0, column=2, padx=10, pady=10)
        control_buttons_frame.pack()

        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(padx=10, pady=10)
        self.stats_label = tk.Label(self.stats_frame, text="Statistics")
        self.stats_label.pack()

        # This is Lier's Bar
        return

    def place_slider_mine(self, frame: tk.Frame):
        self.slider_label_mine = tk.Label(frame, text="My Cards")
        self.slider_label_mine.grid(row=0, column=0)
        self.slider_my_card = tk.Scale(frame, from_=0, to=5, orient="horizontal")
        self.slider_my_card.config(command=lambda _: self.place_stats())
        self.slider_my_card.set(4)
        self.slider_my_card.grid(row=1, column=0)

    def calculate_stats(self):
        # Get my cards
        my_cards = self.slider_my_card.get()

        # Get probabilities for each n
        probabilities = CDF_matrix[:, my_cards]

        # Print statistics for each n
        stats = ""
        for n, probability in enumerate(probabilities):
            stats += f"Friend having {n} K's: {probability:.4f}\n"

        return stats

    def place_stats(self):
        self.stats_label.config(text=self.calculate_stats())

    def CDF_handler(self):
        if self.heatmap_on:
            close_plt()
            self.heatmap_on = False
            return
        self.heatmap_on = True
        CDF_heatmap()

    def PMF_handler(self):
        if self.heatmap_on:
            close_plt()
            self.heatmap_on = False
            return
        self.heatmap_on = True
        PMF_heatmap()


if __name__ == "__main__":
    app = App()
    app.mainloop()
