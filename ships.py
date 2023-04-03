class Ship:
    def __init__(self, name, size, symbol):
        self.name = name
        self.size = size
        self.symbol = symbol
        self.hits = 0

    def is_sunk(self):
        return self.hits == self.size


def create_ships():
    return [
        Ship("Frigate", 2, "F"),
        Ship("Destroyer", 3, "D"),
        Ship("Submarine", 3, "S"),
        Ship("Battleship", 4, "B"),
        Ship("Aircraft Carrier", 5, "A"),
    ]