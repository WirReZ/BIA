import math


class TSP_City:
    def __init__(self, idx, x, y):
        self.id = idx
        self.x = x
        self.y = y

    def distance_to(self, city):
        distance_x = self.x - city.x
        distance_y = self.y - city.y
        return math.sqrt(pow(distance_x, 2) + pow(distance_y, 2))

    def __repr__(self):
        return str(self.id)
