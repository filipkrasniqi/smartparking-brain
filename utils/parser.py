from map.elements.node import Node
from map.elements.parking import Slot, Parking
from map.elements.parking_container import ParkingContainer

class Parser:
    class __Parser:
        def __init__(self, data_dir):
            self.data_dir = data_dir

        def parse_node(self, idx, node):
            splits = list(filter(lambda x : x != "", node.replace("\n", "").split(" ")))
            assert len(splits) == 1, "Wrong init of node"
            return Node(idx, int(splits[0]))

        def parse_slot(self, idx, slot):
            splits = list(filter(lambda x : x != "", slot.replace("\n", "").split(" ")))
            assert len(splits) == 4, "Wrong init of slot"
            return Slot(idx, int(splits[0]), float(splits[1]), float(splits[2]), splits[3])

        def parse_parking(self, idx, parking):
            splits = list(filter(lambda x : x != "", parking.replace("\n", "").split(" ")))
            assert len(splits) == 3, "Wrong init of parking"
            return Parking(idx, float(splits[0]), float(splits[1]), splits[2])

        def __read_nodes(self):
            nodes = []
            with open(self.data_dir+"nodes.txt", "r") as nodes_data:
                for i, data in enumerate(nodes_data):
                    if i > 0:
                        # data is empty, but we keep it in case in future we need it
                        nodes.append(self.parse_node(i, data))
                    else:
                        num_nodes = int(data.replace("\n", ""))
            return nodes

        def __read_slots(self):
            slots = []
            with open(self.data_dir + "slots.txt", "r") as slots_data:
                for i, data in enumerate(slots_data):
                    if i > 0:
                        slots.append(self.parse_slot(i, data))
                    else:
                        num_slots = int(data.replace("\n", ""))
            return slots

        def __read_parkings(self):
            parking = []
            with open(self.data_dir + "parking.txt", "r") as parking_data:
                for i, data in enumerate(parking_data):
                    if i > 0:
                        parking.append(self.parse_parking(i, data))
                    else:
                        num_parking = int(data.replace("\n", ""))
            return parking

        def read_parking_container(self):
            nodes, slots, parking = self.__read_nodes(), self.__read_slots(), self.__read_parkings()
            return ParkingContainer(nodes, slots, parking)

    __instance = None

    def __init__(self, data_dir):
        if not Parser.__instance:
            Parser.__instance = Parser.__Parser(data_dir)
        else:
            Parser.__instance.data_dir = data_dir

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    def getInstance(self):
        return Parser.__instance