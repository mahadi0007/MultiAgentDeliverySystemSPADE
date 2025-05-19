
# MultiAgentDeliverySystemSPADE

A SPADE-based multi-agent system for simulating delivery operations, built with Python and integrated with an Openfire XMPP server. The system implements two scenarios: a straightforward delivery (ORD001) and a delivery with a traffic disruption requiring rerouting (ORD002). Four agents—Customer, Task, Delivery, and Map—collaborate to handle delivery requests, task assignments, route navigation, and delivery confirmations.

## Table of Contents
- [Features](#features)
- [Scenarios](#scenarios)
- [Dependencies](#dependencies)
- [File Structure](#file-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#running-the-project)
- [Example Output](#example-output)

## Features
- **Multi-Agent Architecture**: Utilizes SPADE for asynchronous agent communication.
- **XMPP Integration**: Leverages Openfire for robust message passing.
- **Two Delivery Scenarios**:
  - ORD001: Straightforward delivery with no disruptions.
  - ORD002: Delivery with dynamic traffic detection and rerouting.
- **Robust Design**: Includes state management, error handling, and detailed logging.
- **Extensible**: Easily adaptable for additional scenarios or real-time routing APIs.

## Scenarios

### Scenario 1: Straightforward Delivery (ORD001)
- **Order ID**: ORD001
- **Description**: The CustomerAgent initiates a delivery request to {lat: 40.7128, lon: -74.006}. The TaskAgent assigns it to the DeliveryAgent, which navigates a single route from {lat: 40.73, lon: -73.995} via an intermediate point and reports delivery. The CustomerAgent confirms receipt.
- **Behavior**: No disruptions, single route, single delivery confirmation.

### Scenario 2: Delivery with Traffic Disruption (ORD002)
- **Order ID**: ORD002
- **Description**: The CustomerAgent requests a delivery to {lat: 40.7128, lon: -74.006}. The DeliveryAgent navigates an initial route, detects traffic at an intermediate point, requests a reroute from the MapAgent, navigates the new route, and reports delivery. The CustomerAgent confirms receipt.
- **Behavior**: Traffic triggers a reroute, ensuring a single delivery to the destination.

## Dependencies
- **Python**: 3.8 or higher
- **SPADE**: 3.2.5 or higher (`pip install spade`)
- **Openfire XMPP Server**: Latest version (tested with 4.8.3)
- **Operating System**: Windows, macOS, or Linux

## File Structure
```
agent_technology/
├── agents/
│   ├── customer_agent.py    # CustomerAgent: Initiates and confirms deliveries
│   ├── task_agent.py       # TaskAgent: Coordinates task assignments
│   ├── delivery_agent.py   # DeliveryAgent: Navigates routes, handles traffic
│   ├── map_agent.py        # MapAgent: Provides routing and rerouting
├── config/
│   ├── openfire_config.py  # XMPP server configuration
├── main.py                 # Orchestrates agent execution
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
```

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/MultiAgentDeliverySystemSPADE.git
   cd MultiAgentDeliverySystemSPADE
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The requirements.txt contains:
   ```
   spade>=3.2.5
   ```

3. **Set Up Openfire XMPP Server**:
   - Download Openfire from https://www.igniterealtime.org/projects/openfire/.
   - Install and start Openfire, then access the admin console at http://localhost:9090.
   - Create the following users with password 12345:
     - customer1@localhost
     - taskagent1@localhost
     - deliveryagent1@localhost
     - mapagent1@localhost
   - Ensure the server runs on localhost:5222.

4. **Verify Directory Structure**:
   - Confirm all files are present as listed in File Structure.
   - Check `openfire_config.py` for correct XMPP server settings (host: localhost, port: 5222).

## Running the Project

1. **Start Openfire**:
   - Launch the Openfire server:
     ```bash
     # Example for Linux/macOS
     openfire/bin/openfire start
     ```
   - On Windows, use the Openfire service or launcher.
   - Verify the server is running by accessing http://localhost:9090.

2. **Run the Project**:
   ```bash
   python main.py
   ```
   - The script executes for 120 seconds, running both ORD001 and ORD002 scenarios sequentially.
   - Console output logs agent interactions, including requests, assignments, routing, traffic detection (ORD002), delivery, and confirmation.

3. **Expected Behavior**:
   - ORD001: Completes in ~20 seconds with a single route and delivery.
   - ORD002: Completes in ~30-40 seconds, including traffic detection and rerouting.

   Logs follow the format:
   ```
   CustomerAgent: Sent delivery request for <ORDER_ID>
   TaskAgent: Processing delivery request <ORDER_ID>
   ...
   CustomerAgent: Confirmed delivery for <ORDER_ID>
   ```

4. **Capture Logs (Optional)**:
   Redirect output to a file for analysis:
   ```bash
   python main.py > output.log
   ```

## Example Output

Below is a sample console output for Scenario 1 (ORD001), showing key agent interactions:
```
CustomerAgent: Starting...
CustomerAgent: Waiting 5 seconds for agent synchronization...
TaskAgent: Starting...
TaskAgent: Waiting for message...
DeliveryAgent: Starting...
DeliveryAgent: Waiting for message...
MapAgent: Starting...
MapAgent: Waiting for message...
CustomerAgent: Sent delivery request for ORD001
TaskAgent: Received message from customer1@localhost with metadata: {'performative': 'request'}
TaskAgent: Message body: {"type": "delivery_request", "order_id": "ORD001", "destination": {"lat": 40.7128, "lon": -74.006}}
TaskAgent: Parsed message: {'type': 'delivery_request', 'order_id': 'ORD001', 'destination': {'lat': 40.7128, 'lon': -74.006}}
TaskAgent: Processing delivery request ORD001
TaskAgent: Assigned ORD001 to DeliveryAgent
TaskAgent: Waiting for message...
DeliveryAgent: Received message from taskagent1@localhost with metadata: {'performative': 'request'}
DeliveryAgent: Parsed message: {'type': 'assign_delivery', 'order_id': 'ORD001', 'destination': {'lat': 40.7128, 'lon': -74.006}}
DeliveryAgent: Assigned order ORD001
DeliveryAgent: Requested route for ORD001
DeliveryAgent: Waiting for message...
MapAgent: Received message from deliveryagent1@localhost with metadata: {'performative': 'request'}
MapAgent: Parsed message: {'type': 'route_request', 'order_id': 'ORD001', 'start': {'lat': 40.73, 'lon': -73.995}, 'destination': {'lat': 40.7128, 'lon': -74.006}}
MapAgent: Processing route request for ORD001
MapAgent: Sent route for ORD001
MapAgent: Waiting for message...
DeliveryAgent: Received message from mapagent1@localhost with metadata: {'performative': 'inform'}
DeliveryAgent: Parsed message: {'type': 'route_response', 'order_id': 'ORD001', 'route': [{'lat': 40.73, 'lon': -73.995}, {'lat': 40.7214, 'lon': -74.0005}, {'lat': 40.7128, 'lon': -74.006}]}
DeliveryAgent: Received route for ORD001: [{'lat': 40.73, 'lon': -73.995}, {'lat': 40.7214, 'lon': -74.0005}, {'lat': 40.7128, 'lon': -74.006}]
DeliveryAgent: Navigating to ORD001 destination
DeliveryAgent: Reported delivered for ORD001
DeliveryAgent: Waiting for message...
TaskAgent: Received message from deliveryagent1@localhost with metadata: {'performative': 'inform'}
TaskAgent: Message body: {"type": "status_update", "order_id": "ORD001", "status": "delivered"}
TaskAgent: Parsed message: {'type': 'status_update', 'order_id': 'ORD001', 'status': 'delivered'}
TaskAgent: Status update for ORD001: delivered
TaskAgent: Notified customer about ORD001 status
TaskAgent: Waiting for message...
CustomerAgent: Received message from taskagent1@localhost with metadata: {'performative': 'inform'}
CustomerAgent: Parsed message: {'type': 'delivery_update', 'order_id': 'ORD001', 'status': 'delivered'}
CustomerAgent: Received update for ORD001: delivered
CustomerAgent: Confirmed delivery for ORD001
TaskAgent: Received message from customer1@localhost with metadata: {'performative': 'inform'}
TaskAgent: Message body: {"type": "delivery_confirmed", "order_id": "ORD001"}
TaskAgent: Parsed message: {'type': 'delivery_confirmed', 'order_id': 'ORD001'}
TaskAgent: Delivery confirmed for ORD001
TaskAgent: Waiting for message...
```

Below is a sample console output for Scenario 2 (ORD002), showing key agent interactions:
```
CustomerAgent: Sent delivery request for ORD002
MapAgent: No message received in timeout period
DeliveryAgent: No message received in timeout period
CustomerAgent: No update received in timeout period
TaskAgent: No message received in timeout period
MapAgent: Waiting for message...
DeliveryAgent: Waiting for message...
TaskAgent: Waiting for message...
TaskAgent: Received message from customer1@localhost with metadata: {'performative': 'request'}
TaskAgent: Message body: {"type": "delivery_request", "order_id": "ORD002", "destination": {"lat": 40.7128, "lon": -74.006}}
TaskAgent: Parsed message: {'type': 'delivery_request', 'order_id': 'ORD002', 'destination': {'lat': 40.7128, 'lon': -74.006}}
TaskAgent: Processing delivery request ORD002
TaskAgent: Assigned ORD002 to DeliveryAgent
TaskAgent: Waiting for message...
DeliveryAgent: Received message from taskagent1@localhost with metadata: {'performative': 'request'}
DeliveryAgent: Parsed message: {'type': 'assign_delivery', 'order_id': 'ORD002', 'destination': {'lat': 40.7128, 'lon': -74.006}}
DeliveryAgent: Assigned order ORD002
DeliveryAgent: Requested route for ORD002
DeliveryAgent: Waiting for message...
MapAgent: Received message from deliveryagent1@localhost with metadata: {'performative': 'request'}
MapAgent: Parsed message: {'type': 'route_request', 'order_id': 'ORD002', 'start': {'lat': 40.7128, 'lon': -74.006}, 'destination': {'lat': 40.7128, 'lon': -74.006}}
MapAgent: Processing route request for ORD002
MapAgent: Sent route for ORD002
MapAgent: Waiting for message...
DeliveryAgent: Received message from mapagent1@localhost with metadata: {'performative': 'inform'}
DeliveryAgent: Parsed message: {'type': 'route_response', 'order_id': 'ORD002', 'route': [{'lat': 40.7128, 'lon': -74.006}, {'lat': 40.7214, 'lon': -74.0005}, {'lat': 40.7128, 'lon': -74.006}]}
DeliveryAgent: Received route for ORD002: [{'lat': 40.7128, 'lon': -74.006}, {'lat': 40.7214, 'lon': -74.0005}, {'lat': 40.7128, 'lon': -74.006}]
DeliveryAgent: Navigating to ORD002 destination
DeliveryAgent: Traffic detected, requesting reroute for ORD002
DeliveryAgent: Waiting for message...
MapAgent: Received message from deliveryagent1@localhost with metadata: {'performative': 'request'}
MapAgent: Parsed message: {'type': 'reroute_request', 'order_id': 'ORD002', 'start': {'lat': 40.7128, 'lon': -74.006}, 'destination': {'lat': 40.7128, 'lon': -74.006}}
MapAgent: Processing reroute request for ORD002
MapAgent: Sent route for ORD002
MapAgent: Waiting for message...
DeliveryAgent: Received message from mapagent1@localhost with metadata: {'performative': 'inform'}
DeliveryAgent: Parsed message: {'type': 'route_response', 'order_id': 'ORD002', 'route': [{'lat': 40.7128, 'lon': -74.006}, {'lat': 40.717, 'lon': -74.003}, {'lat': 40.7128, 'lon': -74.006}]}
DeliveryAgent: Received route for ORD002: [{'lat': 40.7128, 'lon': -74.006}, {'lat': 40.717, 'lon': -74.003}, {'lat': 40.7128, 'lon': -74.006}]
DeliveryAgent: Navigating to ORD002 destination
DeliveryAgent: Reported delivered for ORD002
DeliveryAgent: Waiting for message...
TaskAgent: Received message from deliveryagent1@localhost with metadata: {'performative': 'inform'}
TaskAgent: Message body: {"type": "status_update", "order_id": "ORD002", "status": "delivered"}
TaskAgent: Parsed message: {'type': 'status_update', 'order_id': 'ORD002', 'status': 'delivered'}
TaskAgent: Status update for ORD002: delivered
TaskAgent: Notified customer about ORD002 status
TaskAgent: Waiting for message...
CustomerAgent: Received message from taskagent1@localhost with metadata: {'performative': 'inform'}
CustomerAgent: Parsed message: {'type': 'delivery_update', 'order_id': 'ORD002', 'status': 'delivered'}
CustomerAgent: Received update for ORD002: delivered
CustomerAgent: Confirmed delivery for ORD002
TaskAgent: Received message from customer1@localhost with metadata: {'performative': 'inform'}
TaskAgent: Message body: {"type": "delivery_confirmed", "order_id": "ORD002"}
TaskAgent: Parsed message: {'type': 'delivery_confirmed', 'order_id': 'ORD002'}
TaskAgent: Delivery confirmed for ORD002
TaskAgent: Waiting for message...
MapAgent: No message received in timeout period
DeliveryAgent: No message received in timeout period
CustomerAgent: No update received in timeout period
TaskAgent: No message received in timeout period
MapAgent: Waiting for message...
DeliveryAgent: Waiting for message...
TaskAgent: Waiting for message...
MapAgent: No message received in timeout period
TaskAgent: No message received in timeout period
DeliveryAgent: No message received in timeout period
CustomerAgent: No update received in timeout period
MapAgent: Waiting for message...
TaskAgent: Waiting for message...
DeliveryAgent: Waiting for message...
```
