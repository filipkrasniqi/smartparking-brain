from functools import reduce

from map.elements.node import Node

from map.elements.parking import Slot, Parking, Position
from mqtt.messages.node import OccupancyMessage

import geopy.distance as distance


class ParkingContainer:

    def __init__(self, nodes: list[Node], slots: list[Slot], parking: list[Parking]):
        # add slot to the corresponding node
        for node in nodes:
            currentNodeSlots = [slot for slot in slots if slot.idNode == node.idNode]
            node.setSlots(currentNodeSlots)

        # add node to the corresponding parking
        for park in parking:
            currentParkNodes = [node for node in nodes if node.idParking == park.idParking]
            park.setNodes(currentParkNodes)

        self.parking = parking

    '''
    Search in the parking list the node given the ID.
    Useful for first configuration of the node, as it only knows its own ID
    '''
    def getNodeIdxGivenID(self, idNode):
        idxPark, found = 0, False
        # search in every park
        while not found and idxPark < len(self.parking):
            # search the node
            idxNode = 0
            while idxNode < len(self.parking[idxPark].nodes) and idNode != self.parking[idxPark].nodes[idxNode].idNode:
                idxNode += 1
            if idxNode < len(self.parking[idxPark].nodes):
                found = self.parking[idxPark].nodes[idxNode].idNode == idNode
            if not found:
                idxPark += 1
        assert found, "Wrong node"
        return idxPark, idxNode

    '''
    Search in the parking list the node given the ID.
    Useful for first configuration of the node, as it only knows its own ID
    '''
    def getNodeGivenID(self, idNode):
        idxPark, idxNode = self.getNodeIdxGivenID(idNode)
        return self.parking[idxPark].nodes[idxNode]

    def setNodeReady(self, idNode):
        idxPark, idxNode = self.getNodeIdxGivenID(idNode)
        self.parking[idxPark].nodes[idxNode].setReady()
        return self.parking[idxPark].nodes[idxNode]

    def setOccupancy(self, occupancy: OccupancyMessage):
        park = next((park for park in self.parking  if park.idParking == occupancy.idParking), None)
        assert park != None, "Wrong park"
        park.setOccupancy(occupancy)

    def findClosestPark(self, position: Position):
        # first, filter park among those that are active and that are empty
        activeParks = list(filter(lambda park: park.isActive(), self.parking))
        # then find the closest one
        if(len(activeParks) > 0):
            closestActivePark = min(
                activeParks,
                key=lambda park: distance.distance(position.getPosition(), park.getPosition())
            )
        else:
            closestActivePark = None
        return closestActivePark

    def nodes(self):
        nodes = []
        for p in self.parking:
            nodes += p.nodes
        return nodes

