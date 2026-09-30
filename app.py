import tkinter as tk
from solver import Solver

WHITE = '#FFFFFF'; WHITE_HOVER = '#E0E0E0'
YELLOW = '#FFE033'; YELLOW_HOVER = '#E6C72A'
RED = '#C41E3A'; RED_HOVER = '#A01830'
ORANGE = '#FF7733'; ORANGE_HOVER = '#E06030'
BLUE = '#0051BA'; BLUE_HOVER = '#003D8F'
GREEN = '#33C45A'; GREEN_HOVER = '#28A04A'
GRAY = '#A0A0A0'; GRAY_HOVER = '#B8B8B8'
BACKGROUND = '#FFF6C7'
TO_HOVER = {
    WHITE:WHITE_HOVER,
    YELLOW:YELLOW_HOVER,
    RED:RED_HOVER,
    ORANGE:ORANGE_HOVER,
    BLUE:BLUE_HOVER,
    GREEN:GREEN_HOVER,
    GRAY:GRAY_HOVER
}
TO_COLOR = {
    WHITE_HOVER:WHITE,
    YELLOW_HOVER:YELLOW,
    RED_HOVER:RED,
    ORANGE_HOVER:ORANGE,
    BLUE_HOVER:BLUE,
    GREEN_HOVER:GREEN,
    GRAY_HOVER:GRAY
}
COLOR2INT = {
    GRAY:0,
    WHITE:1,
    YELLOW:2,
    RED:3,
    ORANGE:4,
    BLUE:5,
    GREEN:6,
}
COLORS = [GRAY, WHITE, YELLOW, RED, ORANGE, BLUE, GREEN]
COLORS_HOVER = [GRAY_HOVER, WHITE_HOVER, YELLOW_HOVER, RED_HOVER, ORANGE_HOVER, BLUE_HOVER, GREEN_HOVER]

W = 2550
H = 1600
STICKER_SIZE = min(H, W) // 16
PANEL_SIZE = int(STICKER_SIZE * 1.5)
PANEL_PAD = int(STICKER_SIZE * 0.5)

class App():
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry(str(W)+'x'+str(H)+'+0+0')
        self.root.configure(bg=BACKGROUND)
        self.root.title('2x2solver')

        self.pixel = tk.PhotoImage(width=1, height=1)

        self.posx = [0.45, 0.35, 0.45, 0.55, 0.65, 0.45]
        self.posy = [0.25, 0.4, 0.4, 0.4, 0.4, 0.55]
        self.faces = []
        self.stickers = []
        self.state = [0] * 24
        self.active = None
        self.activeid = None

        for i in range(6):
            face = tk.Frame(self.root, background=BACKGROUND)
            face.place(relx=self.posx[i], rely=self.posy[i], anchor='center')
            self.faces.append(face)
            for j in range(4):
                sticker = tk.Button(
                    face, 
                    image=self.pixel, 
                    width=STICKER_SIZE,
                    height=STICKER_SIZE,
                    bg=GRAY,
                    activebackground=GRAY_HOVER,
                    relief='raised',
                    bd=5
                )
                sticker.configure(command=lambda id=i*4+j: self.activate(id))
                sticker.grid(row=j//2, column=j%2)
                self.stickers.append(sticker)
        self.reset()

        self.colorpanel = tk.Frame(self.root, background=BACKGROUND)
        self.colorpanel.place(relx=0.5, rely=0.75, anchor='center')
        for i in range(1, 7):
            panel = tk.Button(
                self.colorpanel,
                image=self.pixel,
                width=PANEL_SIZE,
                height=PANEL_SIZE,
                bg=COLORS[i],
                activebackground=COLORS_HOVER[i],
                relief='ridge',
                bd=5,
                command=lambda c=COLORS[i]: self.place_color(c)
            )
            panel.grid(row=0, column=i, padx=PANEL_PAD)

        self.buttons = tk.Frame(self.root, background=BACKGROUND)
        self.buttons.place(relx=0.5, rely=0.9, anchor='center')
        self.resetbutton = tk.Button(
            self.buttons,
            text='RESET',
            width=10,
            height=3,
            command=self.reset
        )
        self.resetbutton.grid(row=0, column=0, padx=PANEL_PAD)
        self.solvebutton = tk.Button(
            self.buttons,
            text='SOLVE',
            width=10,
            height=3,
            command=self.solve
        )
        self.solvebutton.grid(row=0, column=1, padx=PANEL_PAD)

        introtext = 'Welcome to 2x2solver! Enter the state of the cube to start.'
        self.solutionfield = tk.Label(self.root, text=introtext, bg=BACKGROUND, font=('Arial', 50))
        self.solutionfield.place(relx=0.5, rely=0.1, anchor='center')

        self.root.mainloop()

    def reset(self):
        for s in self.stickers:
            s.configure(bg=GRAY, activebackground=GRAY_HOVER)
        self.state = [0] * 24
        self.activate(0)

    def activate(self, id):
        sticker = self.stickers[id]
        if self.active != None:
            current = self.active.cget('bg')
            if current in COLORS: self.active.configure(bg=current)
            else: self.active.configure(bg=TO_COLOR[current])
        current = sticker.cget('bg')
        sticker.configure(bg=TO_HOVER[current])
        self.active = sticker
        self.activeid = id

    def place_color(self, color):
        if self.active != None:
            self.active.configure(bg=color, activebackground=TO_HOVER[color])
            self.state[self.activeid] = COLOR2INT[color]
            if self.activeid < 23: self.activate(self.activeid + 1)

    def solve(self):
        solver = Solver()
        solution = solver.run(self.state)
        self.solutionfield.configure(text=solution)

def main():
    app = App()

if __name__ == '__main__':
    main()
