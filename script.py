import tkinter as tk
import subprocess
from subprocess import Popen
from subprocess import PIPE
from time import sleep
import re


class Game:
    def __init__(self):
        self.suggest = None
        # self.moves = [('B', 4, 4), ('W', 16, 16), ('B', 5, 5), ('W', 9, 9)]
        self.moves = []
        args = 'gnugo --mode gtp --boardsize {0}'.format(19)
        self.gnugo = subprocess.Popen(args.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False,
                                      universal_newlines=True)
        self.turn = 'black'

    def update_suggest(self, *suggest):
        self.suggest = suggest

    def add_move(self, color, x, y):
        self.moves.append((color, x, y))

    def init_moves(self, moves):
        self.moves = moves
        self.gnugo.stdin.write(b'showboard\n')
        sleep(2)
        while True:
            data = self.gnugo.stdout.read()
            if not data:
                print("hehe")
                break
            print(0)
        print(0)

    def next_move(self):
        """
        Use gnugo engine
        """
        # save game to sgf format
        if self.turn == 'black':
            self.gnugo.stdin.write('genmove black\n')
            self.gnugo.stdin.flush()
            new_move = self.gnugo.stdout.readline().strip().split(" ")[1]
            self.gnugo.stdout.readline()
            self.moves.append(('B', new_move))
            self.turn = 'white'
        elif self.turn == 'white':
            self.gnugo.stdin.write('genmove white\n')
            self.gnugo.stdin.flush()
            new_move = self.gnugo.stdout.readline().strip().split(" ")[1]
            self.gnugo.stdout.readline()
            self.moves.append(('W', new_move))
            self.turn = 'black'

        print(0)


# game = Game()
# game.init_moves([('B', 4, 4), ('W', 16, 16), ('B', 3, 5)])
# # game.next_move()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.suggest_size = 10
        self.base = 25
        self.n = 19 * self.base
        self.game = Game()
        self.create_widgets()

    def create_widgets(self):
        base = self.base
        n = self.n
        canvas = tk.Canvas(self, height=n + base * 2, width=n + base * 2, background='yellow')
        canvas.place(x=1, y=1)
        canvas.bind('<Motion>', self.motion)
        canvas.bind('<Button-1>', self.click)
        canvas.pack()
        self.canvas = canvas

        self.auto_button = tk.Button(self, text="auto", command=self.auto, )
        self.auto_button.pack(side="bottom")
        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")

    def gen_move(self, i):
        if i < 200:
            self.game.next_move()
            self.after_idle(self.gen_move, i + 1)

    def auto(self):
        self.gen_move(0)

    def get_position(self, event):
        ex, ey = event.x, event.y
        if ex > self.base and ey > self.base:
            x = int(ex / self.base)
            y = int(ey / self.base)
            x_valid = (ex - self.base * x < self.suggest_size) or (self.base * (x + 1) - ex < self.suggest_size)
            y_valid = (ey - self.base * y < self.suggest_size) or (self.base * (y + 1) - ey < self.suggest_size)
            if x_valid and y_valid:
                if self.base * (x + 1) - ex < self.suggest_size:
                    x += 1
                if self.base * (y + 1) - ey < self.suggest_size:
                    y += 1
                return x, y
        return None

    def motion(self, event):
        if self.get_position(event):
            x, y = self.get_position(event)
            self.game.update_suggest(x, y)

    def draw_board(self):
        print('draw')
        base = self.base
        n = self.n
        canvas = self.canvas
        game = self.game
        canvas.delete("all")
        texts = "ABCDEFGHJKLMNOPQRST"
        print(game.moves)
        for i in range(19):
            canvas.create_text(25 * (i + 1), 10, text=texts[i])
            canvas.create_text(10, 25 * (19 - i), text=str(i + 1))
        for i in [4, 10, 16]:
            for j in [4, 10, 16]:
                self.draw_special_point(i, j)
        for i in range(1, 20):
            canvas.create_line(n / 19 * i, base, n / 19 * i, n)
            canvas.create_line(base, n / 19 * i, n, n / 19 * i)

        if game.suggest:
            size = self.suggest_size
            x, y = game.suggest
            canvas.create_oval(base * x - size, base * y - size, base * x + size, base * y + size)

        for move in game.moves:
            color, position = move
            y, x = position[0], position[1:]
            y = 19 - texts.find(y)
            x = int(x)
            colors = {'B': 'black', 'W': 'white'}
            color = colors[color]
            move_size = 10
            canvas.create_oval(base * x - move_size, base * y - move_size, base * x + move_size, base * y + move_size,
                               fill=color)
        self.canvas.after(50, self.draw_board)

    def draw_special_point(self, x, y):
        size = 3
        base = self.base
        canvas = self.canvas
        canvas.create_oval(base * x - size, base * y - size, base * x + size, base * y + size, fill='black')

    def add_suggest(self, x, y):
        canvas = self.canvas
        canvas.create_oval(self.base * x, self.base * y, self.base * x + 10, self.base * y + 10)
        print(x, y)

    def click(self, event):
        if self.get_position(event):
            x, y = self.get_position(event)
            self.game.add_move('B', x, y)
            self.game.next_move()


root = tk.Tk()
root.title("Go Game")
app = Application(master=root)
app.draw_board()
app.mainloop()
