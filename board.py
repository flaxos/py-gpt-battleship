class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    def place_ship(self, ship, x, y, orientation):
        if orientation == 'H':
            if y + ship.size > self.size:
                return False
            for i in range(ship.size):
                if self.grid[x][y + i] != ' ':
                    return False
            for i in range(ship.size):
                self.grid[x][y + i] = ship.symbol
        elif orientation == 'V':
            if x + ship.size > self.size:
                return False
            for i in range(ship.size):
                if self.grid[x + i][y] != ' ':
                    return False
            for i in range(ship.size):
                self.grid[x + i][y] = ship.symbol
        return True

    def is_valid_position(self, ship, x, y, orientation):
        if orientation == 'H':
            if y + ship.size > self.size:
                return False
            for i in range(ship.size):
                if self.grid[x][y + i] != ' ':
                    return False
        elif orientation == 'V':
            if x + ship.size > self.size:
                return False
            for i in range(ship.size):
                if self.grid[x + i][y] != ' ':
                    return False
        return True

    def display(self, show_ships=True):
        for row in self.grid:
            print(' '.join(row if show_ships else ('*' if cell != ' ' else ' ' for cell in row)))