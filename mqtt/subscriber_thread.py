import collections
import socket
import threading
from concurrent.futures import thread
import time
from threading import Thread


import paho.mqtt.client as mqtt

from map.elements.node import Node
from map.elements.position import Position, PositionBuilder
from mqtt.log_thread import LogThread
from map.elements.parking_container import ParkingContainer

import datetime
import json
import jsonpickle

from mqtt.messages.device import DeviceMessage
from mqtt.messages.node import OccupancyMessage
from mqtt.timer.check_timer import CheckTimer
from mqtt.timer.device_timer import DeviceTimer

BROKER_IP = "80.211.69.17"    # "192.168.1.151" # my laptop

class MQTTSubscriber(LogThread):

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe("parking/#")
        self.client.message_callback_add('parking/node/configure', self.on_configure)
        self.client.message_callback_add('parking/node/occupancy', self.on_occupancy)
        self.client.message_callback_add('parking/device/activate/#', self.on_activate_device)
        self.client.message_callback_add('parking/device/deactivate/#', self.on_deactivate_device)
        self.client.message_callback_add('parking/device/position/#', self.on_position_device)

        # start check timer to check for nodes and devices

    def on_activate_device(self, client, userdata, msg):
        # TODO dovrei fare che qui prima chiede eventualmente una selezione della destination al client
        deviceMessage = DeviceMessage(msg.payload)
        if deviceMessage.idClient not in self.devices:
            self.devices[deviceMessage.idClient] = DeviceTimer(self.client, deviceMessage, self.parkingContainer)
            self.devices[deviceMessage.idClient].start()
        else:
            self.devices[deviceMessage.idClient].setReady()

    def on_deactivate_device(self, client, userdata, msg):
        idClient = msg.payload
        if idClient in self.devices:
            self.devices[idClient].setPause()

    def on_position_device(self, client, userdata, msg):
        deviceMessage = DeviceMessage(msg.payload)
        if deviceMessage.idClient in self.devices:
            self.devices[deviceMessage.idClient].setDevice(deviceMessage)
            self.devices[deviceMessage.idClient].setReady()

    def sendConfig(self, idNode):
        # set node as ready
        node = self.parkingContainer.setNodeReady(idNode)
        # returning the node information: we provide everything
        self.client.publish('parking/brain/configure', jsonpickle.encode(node))

    def on_configure(self, client, userdata, msg):
        # getting idNode
        idNode = int(msg.payload)
        # retrieving node from ID
        # sending config message to node
        self.sendConfig(idNode)
        # log
        self.logExcel("ON_CONFIGURE", idNode, idNode)

    def on_occupancy(self, client, userdata, msg):
        # setting the occupancy for that node
        node_slots: OccupancyMessage = jsonpickle.decode(msg.payload)
        # retrieving node from ID
        node = self.parkingContainer.getNodeGivenID(node_slots.idNode)
        # checking if to set occupancy or whether to do the config
        if node.isReady():
            self.parkingContainer.setOccupancy(node_slots)
        else:
            # sending config message to node
            self.sendConfig(node_slots.idNode)
        # log
        self.logExcel("ON_OCCUPANCY", node.idNode, node_slots)


    def __init__(self, name, parkingContainer):
        LogThread.__init__(self, name)

        # Initializing mqtt protocol
        self.client = mqtt.Client("brain")

        self.client.username_pw_set(username="brain", password="brain")

        # self.client.tls_set(ca_certs="../keys/mosquitto.org.crt", certfile="../keys/client.crt",
        #                keyfile="../keys/client.key")

        self.client.connect(BROKER_IP, 1883, 60)

        self.client.on_connect = self.on_connect

        # Initializing architecture stuff
        self.parkingContainer = parkingContainer

        # devices
        self.devices = {}

        # starting CheckTimer
        self.checkTimer = CheckTimer(self.parkingContainer, self.devices)

    def run(self):
        self.client.loop_forever()
