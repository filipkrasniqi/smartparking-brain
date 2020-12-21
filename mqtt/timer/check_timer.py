import time
from datetime import datetime

from mqtt.log_thread import LogThread


class CheckTimer(LogThread):
    TIME_THRESHOLD = 2
    def __init__(self, parkingContainer, devices, name = "CheckTimer"):
        LogThread.__init__(self, name)
        self.parkingContainer, self.devices = parkingContainer, devices
        self.start()
        self.__keepRunning, self.__isRunning = True, False

    def run(self):
        self.__isRunning = True
        while self.__keepRunning:
            self.log("Checking node to communicate to...")
            # check if every node is communicating constantly
            now = datetime.today()
            for node in self.parkingContainer.nodes():
                # check if node is ready and has not been communicating for a while
                if node.isReady() and abs((now - node.lastCommunication()).seconds) > CheckTimer.TIME_THRESHOLD * 60:
                    # node becomes TO_CONFIGURE. Not considered anymore with devices
                    self.log("WARNING: node to be configured")
                    node.configure()
                    self.logExcel("NODE DISCONNECT", node.idNode, node.idNode)
            # check if every device is communicating constantly, and eventually set it to WARNING
            for device_key in self.devices:
                device = self.devices[device_key]
                # check if device is ready and has not been communicating for a while
                if device.isReady() and abs((now - device.lastCommunication()).seconds) > CheckTimer.TIME_THRESHOLD * 60:
                    # just a warning state
                    self.log("WARNING: device not communicating")
                    device.warning()
                    self.logExcel("DEVICE DISCONNECT", device_key, device_key)
            time.sleep(30)
        self.__isRunning = False

    def stop(self):
        self.__keepRunning = False

    def kill(self):
        self.log("Starting kill...")
        self.stop()
        while self.__isRunning:
            time.sleep(1)
