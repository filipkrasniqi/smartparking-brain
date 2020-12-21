from map.elements.position import PositionBuilder


class DeviceMessage:
    def __init__(self, payload):
        idClient, currentPositionString, destinationString = payload.decode("utf-8").split("$$$")
        self.idClient, self.currentPosition, self.destination = idClient, PositionBuilder().build(
            currentPositionString), PositionBuilder().build(destinationString)