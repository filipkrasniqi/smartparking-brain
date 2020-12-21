from functools import reduce

from map.elements.node import *
from map.elements.position import Position
from mqtt.messages.node import OccupancyMessage


class Parking(Position):
    def __init__(self, idParking, latitude, longitude, name):
        Position.__init__(self, latitude, longitude, name)
        self.idParking = idParking
        self.nodes: list[Node] = []

    def setNodes(self, nodes):
        self.nodes = nodes

    def getActiveNodes(self):
        return [node for node in self.nodes if node.status == NodeStatus.READY]

    def setOccupancy(self, occupancy: OccupancyMessage):
        # find correct node
        node: Node = next((node for node in self.nodes if node.idNode == occupancy.idNode), None)
        assert node != None, "Wrong node"
        node.setOccupancy(occupancy)

    def isActive(self):
        assert self.nodes != None and len(self.nodes) > 0, "Wrong park"
        if len(self.nodes) > 1:
            return reduce((lambda node1, node2: node1.hasEmptySlots() and node2.hasEmptySlots()), self.nodes)
        else:
            return self.nodes[0].hasEmptySlots()
