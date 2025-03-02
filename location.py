class Location:
    def __init__(self, i, x, y, d, S, O, C):
        self.i = i
        self.x = x
        self.y = y
        self.d = d
        self.S = S
        self.O = O
        self.C = C
        self.arrival_time = 0
        self.departure_time = 0
        self.delay=0
