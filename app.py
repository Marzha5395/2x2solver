import tkinter as tk
from solver import Solver

WHITE = "#FFFFFF"; WHITE_HOVER = "#E0E0E0"
YELLOW = "#FFE033"; YELLOW_HOVER = "#E6C72A"
RED = "#C41E3A"; RED_HOVER = "#A01830"
ORANGE = "#FF7733"; ORANGE_HOVER = "#E06030"
BLUE = "#0051BA"; BLUE_HOVER = "#003D8F"
GREEN = "#33C45A"; GREEN_HOVER = "#28A04A"
GRAY = "#A0A0A0"; GRAY_HOVER = "#B8B8B8"
BACKGROUND = "#FFF6C7"
COLORS = [GRAY, WHITE, YELLOW, RED, ORANGE, BLUE, GREEN]
COLORS_HOVER = [GRAY_HOVER, WHITE_HOVER, YELLOW_HOVER, RED_HOVER, ORANGE_HOVER, BLUE_HOVER, GREEN_HOVER]
TO_HOVER = {c:ch for c, ch in zip(COLORS, COLORS_HOVER)}
TO_COLOR = {ch:c for c, ch in zip(COLORS, COLORS_HOVER)}
COLOR2INT = {c:i for i, c in enumerate(COLORS)}

class App:
    def __init__(self):
        self.root = tk.Tk()

        # Configure dimensions & general
        h = self.root.winfo_screenheight()
        w = self.root.winfo_screenwidth()
        stickersize = min(h, w) // 16
        panelsize = int(stickersize * 1.5)
        padding = int(stickersize * 0.5)

        self.root.geometry(f"{w}x{h}+0+0")
        self.root.configure(bg=BACKGROUND)
        self.root.title("2x2solver")

        self.pixel = tk.PhotoImage(width=1, height=1)

        posx = [0.45, 0.35, 0.45, 0.55, 0.65, 0.45]
        posy = [0.25, 0.4, 0.4, 0.4, 0.4, 0.55]
        self.faces = []
        self.stickers = []
        self.state = [0] * 24
        self.active = None
        self.activeid = None

        # Text & solution field
        self.solutionfield = tk.Label(self.root, text="", bg=BACKGROUND, font=("Arial", 40))
        self.solutionfield.place(relx=0.5, rely=0.1, anchor="center")

        # Cube faces and stickers
        for i in range(6):
            face = tk.Frame(self.root, background=BACKGROUND)
            face.place(relx=posx[i], rely=posy[i], anchor="center")
            self.faces.append(face)
            for j in range(4):
                sticker = tk.Button(
                    face, 
                    image=self.pixel, 
                    width=stickersize,
                    height=stickersize,
                    bg=GRAY,
                    activebackground=GRAY_HOVER,
                    relief="raised",
                    bd=5
                )
                sticker.configure(command=lambda id=i*4+j: self.activate(id))
                sticker.grid(row=j//2, column=j%2)
                self.stickers.append(sticker)

        # Colorpanel for choosing color
        self.colorpanel = tk.Frame(self.root, background=BACKGROUND)
        self.colorpanel.place(relx=0.5, rely=0.75, anchor="center")
        for i in range(1, 7):
            panel = tk.Button(
                self.colorpanel,
                image=self.pixel,
                width=panelsize,
                height=panelsize,
                bg=COLORS[i],
                activebackground=COLORS_HOVER[i],
                relief="ridge",
                bd=5,
                command=lambda c=COLORS[i]: self.placecolor(c)
            )
            panel.grid(row=0, column=i, padx=padding)

        # Buttons exit, reset and solve
        self.buttons = tk.Frame(self.root, background=BACKGROUND)
        self.exitbutton = tk.Button(
            self.buttons,
            text="EXIT",
            width=10,
            height=2,
            font=("Arial", 30),
            command=self.root.destroy
        )
        self.exitbutton.grid(row=0, column=0, padx=padding)
        self.buttons.place(relx=0.5, rely=0.9, anchor="center")
        self.resetbutton = tk.Button(
            self.buttons,
            text="RESET",
            width=10,
            height=2,
            font=("Arial", 30),
            command=self.reset
        )
        self.resetbutton.grid(row=0, column=1, padx=padding)
        self.solvebutton = tk.Button(
            self.buttons,
            text="SOLVE",
            width=10,
            height=2,
            font=("Arial", 30),
            command=self.solve
        )
        self.solvebutton.grid(row=0, column=2, padx=padding)

        self.reset()
        self.root.mainloop()

    def reset(self):
        # ========================================
        # Reset window to initial states
        # ========================================
        for s in self.stickers:
            s.configure(bg=GRAY, activebackground=GRAY_HOVER)
        self.state = [0] * 24
        self.activate(0)
        introtext = "Welcome to 2x2solver! Enter the state of the cube to start.\nTo fill in the colors, click on a sticker and then the color of that sticker."
        self.solutionfield.configure(text=introtext)

    def activate(self, id):
        # ========================================
        # Change activated sticker on the cube
        # to stickers[id]
        # ========================================
        sticker = self.stickers[id]
        if self.active is not None:
            current = self.active.cget("bg")
            if current in COLORS: self.active.configure(bg=current)
            else: self.active.configure(bg=TO_COLOR[current])
        current = sticker.cget("bg")
        sticker.configure(bg=TO_HOVER[current])
        self.active = sticker
        self.activeid = id

    def placecolor(self, color):
        # ========================================
        # Places the color clicked on the
        # activated sticker
        # ========================================
        if self.active is not None:
            self.active.configure(bg=color, activebackground=TO_HOVER[color])
            self.state[self.activeid] = COLOR2INT[color]
            if self.activeid < 23: self.activate(self.activeid + 1)

    def solve(self):
        # ========================================
        # Call the solver to solve
        # Show solution on screen
        # ========================================
        solver = Solver()
        solution = solver.run(self.state)
        self.solutionfield.configure(text=solution)

def main():
    App()

if __name__ == "__main__":
    main()
