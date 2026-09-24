import tkinter as tk
import time

WHITE = '#FFFFFF'
YELLOW = '#FFD500'
RED = '#C41E3A'
ORANGE = '#FF5800'
BLUE = '#0051BA'
GREEN = '#009E60'
GRAY = '#A0A0A0'

class App():
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry('2550x1600+0+0')
        self.root.configure(bg='#FFF6C7')
        self.root.title('2x2solver')

        self.pixel = tk.PhotoImage(width=1, height=1)

        self.posx = [0.45, 0.35, 0.45, 0.55, 0.65, 0.45]
        self.posy = [0.35, 0.5, 0.5, 0.5, 0.5, 0.65]
        self.faces = []
        self.stickers = []

        for i in range(6):
            face = tk.Frame(self.root)
            face.place(relx=self.posx[i], rely=self.posy[i], anchor='center')
            self.faces.append(face)
            for j in range(4):
                sticker = tk.Button(
                    face, 
                    image=self.pixel, 
                    width=100,
                    height=100,
                    bg=GRAY,
                    activebackground=BLUE,
                )
                sticker.configure(command=lambda s=sticker: s.configure(bg=BLUE))
                sticker.grid(row=j//2, column=j%2)
                self.stickers.append(sticker)

        self.root.mainloop()

def main():
    app = App()


if __name__ == '__main__':
    main()
