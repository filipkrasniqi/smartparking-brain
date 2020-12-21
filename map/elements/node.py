from datetime import datetime
from enum import Enum

import json
from functools import reduce

from map.elements.position import Position
from mqtt.messages.node import OccupancyMessage


class Node:
    def __init__(self, idNode, idParking):
        self.idNode = idNode
        self.idParking = idParking
        self.slots: list[Slot] = []
        self._status = NodeStatus.TO_CONFIGURE
        self.__lastTimeUpdate = datetime.today()

    def setSlots(self, slots):
        self.slots = slots

    def setOccupancy(self, occupancy: OccupancyMessage):
        self.__lastTimeUpdate = datetime.today()
        for slotOccupancy in occupancy.slots:
            slot = next((slot for slot in self.slots if slot.idSlot == slotOccupancy.idSlot), None)
            if slot is not None:
                slot.setOccupied(slotOccupancy.occupied)

    def setReady(self):
        self._status = NodeStatus.READY

    def isReady(self):
        return self._status == NodeStatus.READY

    def configure(self):
        self._status = NodeStatus.TO_CONFIGURE

    def hasEmptySlots(self):
        slots_occupation = [slot.occupied for slot in self.slots]
        return self.isReady() and reduce((lambda occupied1, occupied2: occupied1 or occupied2), slots_occupation)

    def lastCommunication(self):
        return self.__lastTimeUpdate

class NodeStatus(Enum):
    TO_CONFIGURE = 1
    READY = 2

# useful when we want to guide the user inside the slot
class Slot(Position):
    def __init__(self, idSlot, idNode, latitude, longitude, name = ""):
        Position.__init__(self, latitude, longitude, name)
        self.idSlot = idSlot
        self.idNode = idNode
        self.occupied = False

    def setOccupied(self, occupied: bool):
        self.occupied = occupied