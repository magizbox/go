import tkinter as tk
import subprocess
import os
from subprocess import Popen
from subprocess import PIPE
from time import sleep
import re


class Game:
    def __init__(self):
        # self.suggest = (1, 1)
        self.suggest = None
        # self.moves = [('B', 4, 4), ('W', 16, 16), ('B', 5, 5), ('W', 9, 9)]
        self.moves = []
        args = 'gnugo --mode gtp --boardsize {0}'.format(19)
        self.gnugo = subprocess.Popen(args.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)

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
        moves = []
        for move in self.moves:
            color, x, y = move
            x = chr(x + ord('a') - 1)
            y = chr(y + ord('a') - 1)
            content = "{}[{}{}]".format(color, x, y)
            moves.append(content)
        moves = ";".join(moves)
        template = "(;GM[1]FF[4]CA[UTF-8]AP[WebGoBoard:0.10.10]ST[0]SZ[19]KM[0]HA[0]PB[Black]PW[White];{})"
        content = template.format(moves)
        with open("temp.sgf", "w") as f:
            f.write(content)
        # run gnugo engine
        Popen('gnugo -l temp.sgf -o temp_output.sgf', shell=True, stdout=PIPE).stdout
        sleep(3)
        with open("temp_output.sgf", "r") as f:
            try:
                content = f.read().replace("\n", "")
                move = re.match("(.*)W\[(.*)]C\[.*\].*", content).groups()[1]
                x, y = move
                x = ord(x) - ord('a') + 1
                y = ord(y) - ord('a') + 1

            except Exception as e:
                pass
        print('next move', move, x, y)
        self.add_move('W', x, y)
        print('next move')


game = Game()
game.init_moves([('B', 4, 4), ('W', 16, 16), ('B', 3, 5)])
# game.next_move()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.suggest_size = 10
        self.base = 25
        self.n = 19 * self.base
        self.game = Game()
        self.create_widgets()
        self.draw_board()

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
            self.draw_board()

    def draw_board(self):
        base = self.base
        n = self.n
        canvas = self.canvas
        game = self.game
        canvas.delete("all")
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
            color, x, y = move
            colors = {'B': 'black', 'W': 'white'}
            color = colors[color]
            move_size = 10
            canvas.create_oval(base * x - move_size, base * y - move_size, base * x + move_size, base * y + move_size,
                               fill=color)

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
            self.draw_board()
            self.game.next_move()
            self.draw_board()

    def create_widgets(self):
        base = self.base
        n = self.n
        canvas = tk.Canvas(self, height=n + base * 2, width=n + base * 2)
        canvas.place(x=1, y=1)
        canvas.bind('<Motion>', self.motion)
        canvas.bind('<Button-1>', self.click)
        canvas.pack()
        self.canvas = canvas
        self.draw_board()

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Cờ vây"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("cờ vây")

# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()
