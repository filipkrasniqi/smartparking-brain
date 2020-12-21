class NodeMessage:
    def __init__(self, idNode, idParking):
        self.idNode = idNode
        self.idParking = idParking
class SlotMessage:
    def __init__(self, idSlot, occupied: bool):
        self.idSlot = idSlot
        self.occupied = occupied

class OccupancyMessage(NodeMessage):
    def __init__(self, idNode, idParking, slots):
        NodeMessage.__init__(self, idNode, idParking)
        self.slots = slots

    def __str__(self):
        _str = "NODE: {}".format(self.idNode)
        for slot in self.slots:
            _str += "{}:{}\n".format(slot.idSlot, slot.occupied)
        return _str