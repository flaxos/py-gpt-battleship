import random
from board import Board
from ships import create_ships, Ship


class BattleshipGame:
    def __init__(self):
        self.human_board = Board()
        self.ai_board = Board()
        self.human_ships = create_ships()
        self.ai_ships = create_ships()

    def place_ai_ships(self):
        for ship in self.ai_ships:
            placed = False
            while not placed:
                x = random.randint(0, self.ai_board.size - 1)
                y = random.randint(0, self.ai_board.size - 1)
                orientation = random.choice(['H', 'V'])
                placed = self.ai_board.place_ship(ship, x, y, orientation)

    def place_human_ship(self, ship, x, y, orientation):
        return self.human_board.place_ship(ship, x, y, orientation)

    def is_valid_human_ship_position(self, ship, x, y, orientation):
        return self.human_board.is_valid_position(ship, x, y, orientation)

    def ai_fire(self):
        while True:
            x = random.randint(0, self.human_board.size - 1)
            y = random.randint(0, self.human_board.size - 1)
            if self.human_board.grid[x][y] != 'X' and self.human_board.grid[x][y] != 'O':
                break

        for ship in self.human_ships:
            if self.human_board.grid[x][y] == ship.symbol:
                ship.hits += 1
                self.human_board.grid[x][y] = 'X'
                return x, y, True
        self.human_board.grid[x][y] = 'O'
        return x, y, False

    def human_fire(self, x, y):
        for ship in self.ai_ships:
            if self.ai_board.grid[x][y] == ship.symbol:
                ship.hits += 1
                self.ai_board.grid[x][y] = 'X'
                return True
        self.ai_board.grid[x][y] = 'O'
        return False

    def all_ships_sunk(self, ships):
        return all(ship.is_sunk() for ship in ships)

    def game_over(self):
        return self.all_ships_sunk(self.human_ships) or self.all_ships_sunk(self.ai_ships)
import tkinter as tk
from game import BattleshipGame
from ships import create_ships


class BattleshipGUI:
    def __init__(self, master):
        self.master = master
        self.game = BattleshipGame()
        self.ship_index = 0
        self.stage = 0
        self.start_x, self.start_y = None, None

        self.human_canvas = tk.Canvas(master, width=300, height=300, bg="white")
        self.ai_canvas = tk.Canvas(master, width=300, height=300, bg="white")

        self.human_canvas.grid(row=0, column=0)
        self.ai_canvas.grid(row=0, column=1)

        self.human_canvas.bind("<Button-1>", self.human_canvas_click)
        self.ai_canvas.bind("<Button-1>", self.ai_canvas_click)

        self.draw_grids()
        self.game.place_ai_ships()

    def draw_grids(self):
        for i in range(11):
            self.human_canvas.create_line(i * 30, 0, i * 30, 300)
            self.human_canvas.create_line(0, i * 30, 300, i * 30)
            self.ai_canvas.create_line(i * 30, 0, i * 30, 300)
            self.ai_canvas.create_line(0, i * 30, 300, i * 30)

    def human_canvas_click(self, event):
        if self.stage == 1:
            x, y = event.x // 30, event.y // 30
            if self.start_x is None and self.start_y is None:
                self.start_x, self.start_y = x, y
            else:
                ship = self.game.human_ships[self.ship_index]
                orientation = "H" if self.start_x == x else "V"
                if self.game.is_valid_human_ship_position(ship, self.start_x, self.start_y, orientation):
                    self.game.place_human_ship(ship, self.start_x, self.start_y, orientation)
                    self.draw_ship_on_human_canvas(ship, self.start_x, self.start_y, orientation)
                    self.ship_index += 1
                    if self.ship_index == len(self.game.human_ships):
                        self.stage = 2
                else:
                    self.human_canvas.configure(bg="red")
                    self.master.after(500, lambda: self.human_canvas.configure(bg="white"))
                self.start_x, self.start_y = None, None

    def ai_canvas_click(self, event):
        if self.stage == 2:
            x, y = event.x // 30, event.y // 30
            hit = self.game.human_fire(x, y)
            if hit:
                self.ai_canvas.create_rectangle(x * 30, y * 30, x * 30 + 30, y * 30 + 30, fill="red")
            else:
                self.ai_canvas.create_oval(x * 30 + 10, y * 30 + 10, x * 30 + 20, y * 30 + 20, fill="blue")
            if self.game.game_over():
                self.stage = 3
                # Option to play again can be added here
            else:
                self.stage = 2
                x, y, hit = self.game.ai_fire()
                if hit:
                    self.human_canvas.create_rectangle(x * 30, y * 30, x * 30 + 30, y * 30 + 30, fill="red")
                else:
                                        self.human_canvas.create_oval(x * 30 + 10, y * 30 + 10, x * 30 + 20, y * 30 + 20, fill="blue")
                if self.game.game_over():
                    self.stage = 3
                    # Option to play again can be added here

    def draw_ship_on_human_canvas(self, ship, x, y, orientation):
        if orientation == 'H':
            for i in range(ship.size):
                self.human_canvas.create_rectangle((y + i) * 30, x * 30, (y + i) * 30 + 30, x * 30 + 30, fill="gray")
        elif orientation == 'V':
            for i in range(ship.size):
                self.human_canvas.create_rectangle(y * 30, (x + i) * 30, y * 30 + 30, (x + i) * 30 + 30, fill="gray")

    def reset_game(self):
        # Reset the game state and GUI elements
        self.game = BattleshipGame()
        self.ship_index = 0
        self.stage = 0
        self.start_x, self.start_y = None, None

        self.human_canvas.delete("all")
        self.ai_canvas.delete("all")

        self.draw_grids()
        self.game.place_ai_ships()


if __name__ == "__main__":
    root = tk.Tk()
    gui = BattleshipGUI(root)
    root.mainloop()