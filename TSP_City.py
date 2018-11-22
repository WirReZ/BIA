import math


class TSP_City:
    def __init__(self, idx, x, y):
        self.id = idx
        self.x = x
        self.y = y

    def distance_to(self, city):
        distance_x = self.x - city.x
        distance_y = self.y - city.y
        return math.sqrt((distance_x * distance_x) + (distance_y * distance_y))

    def __repr__(self):
        return str(self.id)
