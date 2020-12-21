# from ble.subscriber_thread import MQTTSubscriber
from mqtt.subscriber_thread import MQTTSubscriber
from utils.parser import Parser
import pandas as pd

def start():
    # initializing nodes
    data_path = "../assets/"
    parser = Parser(data_path).getInstance()
    parking_container = parser.read_parking_container()
    subscriberThread = MQTTSubscriber("MQTT", parking_container)
    subscriberThread.start()

if __name__ == "__main__":
    start()