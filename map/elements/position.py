class Position:
    def __init__(self, latitude: float, longitude: float, name = ""):
        self.latitude, self.longitude, self.name = latitude, longitude, name

    def getPosition(self):
        return (self.latitude, self.longitude)

class PositionBuilder:
    def build(self, positionString):
        latitude, longitude = [float(coord) for coord in positionString.split(",")]
        return Position(latitude, longitude)