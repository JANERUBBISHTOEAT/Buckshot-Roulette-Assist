import tkinter as tk

# import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("450x220")

        # Variables
        self.bullets_float = []  # Float probability of *red* bullets
        self.bullets_state = []  # Int state of bullets
        # bullets_state: 0: default, 1: deemed red, 2: deemed black

        # Slider Frame
        slider_frame = tk.Frame(self)
        slider_frame_red = tk.Frame(slider_frame)
        slider_frame_black = tk.Frame(slider_frame)
        self.place_slider_red(slider_frame_red)
        self.place_slider_black(slider_frame_black)
        slider_frame_red.grid(row=0, column=0, padx=10)
        slider_frame_black.grid(row=0, column=1, padx=10)
        slider_frame.pack(padx=10, pady=10)

        # Clear Button
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_bullets)
        self.clear_button.pack(padx=10, pady=10)

        # Bullets Frame
        self.bullets_frame = tk.Frame(self)
        self.place_bullets()
        self.bullets_frame.pack(padx=10, pady=10)

        # Initialize bullets
        self.clear_bullets()

    def place_slider_red(self, frame: tk.Frame):
        self.slider_label_red = tk.Label(frame, text="Red")
        self.slider_label_red.grid(row=0, column=0)
        self.slider_label_red.config(fg="white", bg="red")
        self.slider_red = tk.Scale(frame, from_=0, to=8, orient="horizontal")
        self.slider_red.config(fg="red")
        self.slider_red.set(4)
        self.slider_red.grid(row=1, column=0)

    def place_slider_black(self, frame: tk.Frame):
        self.slider_label_black = tk.Label(frame, text="Black")
        self.slider_label_black.grid(row=0, column=1)
        self.slider_label_black.config(fg="white", bg="black")
        self.slider_black = tk.Scale(frame, from_=0, to=8, orient="horizontal")
        self.slider_black.config(fg="black")
        self.slider_black.set(4)
        self.slider_black.grid(row=1, column=1)

    def clear_bullets(self):
        for widget in self.bullets_frame.winfo_children():
            widget.destroy()
        l = self.slider_red.get() + self.slider_black.get()
        self.bullets_float = [-1 for _ in range(l)]
        self.bullets_state = [0 for _ in range(l)]
        self.update_bullets()
        self.place_bullets()

    def place_bullets(self):
        for i, e in enumerate(self.bullets_float):
            bullet_button = tk.Button(self.bullets_frame)
            display_prob = (
                e if self.bullets_state[i] == 0 else self.bullets_state[i] % 2
            )
            bullet_button.config(text="{}\n{: .2f}".format(i + 1, display_prob))
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
        actual_r = self.slider_red.get()
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


if __name__ == "__main__":
    app = App()
    app.mainloop()
