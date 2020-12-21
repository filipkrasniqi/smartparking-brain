# Smart Parking: brain
For a brief description of the architecture, please refer to [this](https://github.com/filipkrasniqi/smartparking-node/blob/master/README.md#brief-summary-of-the-architecture).

This code refers to the **brain** and it is written in Python.

## A note: broker configuration
The broker is set-up with specific ACL. To run it with docker: sudo docker run -it --name mqtt_broker -p 1883:1883 -v /home/mqtt/mqtt_broker:/mosquitto eclipse-mosquitto. Additional information on ACL will be provided shortly.

## Used software: tools and libraries
We use [paho-mqtt](https://pypi.org/project/paho-mqtt/) to connect the MQTT client, jsonpickle to serialize Python objects.

## Downloading and building
To download and build this repository, you should simply clone the repo and run ```pip install -r requirements.txt```. A keys directory will follow, containing certificates in case MQTT is encrypted. Communication among brain, devices, anchors and effectors is done with MQTT. A list of the topics with payload info follows.

## Protocol
Communication among brain, devices, nodes and effectors is done with MQTT. A list of the topics with payload info follows.

### Nodes
- **parking/node/configure**: node sends request of configuration to the brain, that will tell the node the information. Node will became ready (status of node: TO_CONFIGURE -> READY).
- **parking/node/occupancy**: node sends occupancy to the brain. Disconnection of brain and unsynchronized info are handled here: in fact, in case brain closes ungracefully, the node must ask for a newer configuration. This is handled by checking, when a occupancy message is received, whether the node is READY; if not, the brain will tell the node that it must configure again by publising again on **parking/brain/configure** the node configuration.

### Devices
- **parking/device/activate**: device sends a message to brain with payload = <ID> to the brain. Once that is subscribed, the brain will consider this device as one that is moving towards a destination, i.e., a parking place (status of the device: READY).
- **parking/device/deactivate**: device sends a message to brain to change status to PAUSE (status of the device: READY/WARNING -> PAUSE). The brain will not send destination info anymore, until a change of status
- **parking/device/position**: a ready device sends its position to brain.

## Code

### Park information
The map is loaded from the [assets/](https://github.com/filipkrasniqi/smartparking-brain/tree/master/assets) directory. The files are mapped with Python classes in the [map/](https://github.com/filipkrasniqi/smartparking-brain/tree/master/map/elements) directory. [Parser](https://github.com/filipkrasniqi/smartparking-brain/blob/master/utils/parser.py) class handles parsing.

### Execution
You should run the [brain/main.py](https://github.com/filipkrasniqi/smartparking-brain/blob/master/brain/brain.py). This code will run the MQTTSubscriber thread, that initializes MQTT stuff (connection, subscribing to topics) and starts the [check timer](https://github.com/filipkrasniqi/smartparking-brain/blob/af36fcf85e2e79d3151cb746b36253d6a18960a8/mqtt/timer/check_timer.py#L7), whose duty is to check whether active nodes and devices communicate properly, handling reinitialization in case of disconnection / ungraceful close.

### Data collection
- **Parking**: all info regarding the parking is stored in the [ParkingContainer](https://github.com/filipkrasniqi/smartparking-brain/blob/af36fcf85e2e79d3151cb746b36253d6a18960a8/map/elements/parking_container.py#L11) instance. This instance resembles the following structure:
  - a ParkingContainer instance contains a list of [Parking](https://github.com/filipkrasniqi/smartparking-brain/blob/d3c1b25b9484c5f5d3c5310c404f913a714cb7da/map/elements/parking.py#L8) instances;
    - a Parking instance contains a list of [Node](https://github.com/filipkrasniqi/smartparking-brain/blob/d3c1b25b9484c5f5d3c5310c404f913a714cb7da/map/elements/node.py#L11) instances;
      - a Node instance contains a list of [Slot](https://github.com/filipkrasniqi/smartparking-brain/blob/d3c1b25b9484c5f5d3c5310c404f913a714cb7da/map/elements/node.py#L50) instances.
- **Devices**: they are stored in the **devices** dictionary, having **deviceID** as key and an instance of [DeviceTimer](https://github.com/filipkrasniqi/smartparking-brain/blob/af36fcf85e2e79d3151cb746b36253d6a18960a8/mqtt/timer/device_timer.py#L16) as value. Every time a new devices (with a new ID) is activated, a new DeviceTimer is instanced, having the goal of communicating to the device information about available parking spaces depending on its destination.

## Short term TODOs
- adding certificate for MQTT encryption
