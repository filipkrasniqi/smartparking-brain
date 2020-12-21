import time
from datetime import datetime
from enum import Enum
from threading import Thread

import jsonpickle

from map.elements.parking_container import ParkingContainer
from map.elements.position import Position
from mqtt.log_thread import LogThread
import paho.mqtt.client as mqtt

from mqtt.messages.device import DeviceMessage


class DeviceTimer(LogThread):
    def __init__(self, client: mqtt.Client, device: DeviceMessage, parkingContainer: ParkingContainer):
        name = "DeviceTimer {}".format(device.idClient)
        LogThread.__init__(self, name)
        Thread.__init__(self, target=self.run)
        self.client, self.device, self.parkingContainer = client, device, parkingContainer
        self.__lastTimeUpdate = datetime.today()
        self.setReady()

    def run(self):
        while self.isActive():
            # find closest node to current position
            closestPark = self.parkingContainer.findClosestPark(self.device.currentPosition)
            if closestPark is not None:
                # communicate to device the destination park as an ID
                self.client.publish("parking/device/best_slot/{}".format(self.device.idClient), closestPark.idParking)
                self.logExcel("BEST SLOT", self.device.idClient, closestPark.idParking)
            else:
                # should happen only in case configuration is not ready yet
                self.log("No available park")
                self.logExcel("BEST SLOT", self.device.idClient, "NONE")
            time.sleep(10)

    # True if device can communicate. Also in case of warning
    # (e.g.: user temporarily entered some place where connection is not working properly)
    # in that case device is still considered active but a warning could be shown
    def isActive(self):
        return self.__deviceStatus == DeviceStatus.READY or self.__deviceStatus == DeviceStatus.WARNING

    def isReady(self):
        return self.__deviceStatus == DeviceStatus.READY

    def setReady(self):
        self.__deviceStatus = DeviceStatus.READY

    def setPause(self):
        self.__deviceStatus = DeviceStatus.PAUSE

    def warning(self):
        self.__deviceStatus = DeviceStatus.WARNING

    def setDevice(self, device: DeviceMessage):
        self.device = device
        self.__lastTimeUpdate = datetime.today()

    def lastCommunication(self):
        return self.__lastTimeUpdate


class DeviceStatus(Enum):
    READY = 1       # communicating
    PAUSE = 2       # stopped (deactivated)
    WARNING = 3     # active but not communicating in a while