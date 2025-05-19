from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
import logging

# logging.basicConfig(level=logging.DEBUG)

class DeliveryAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.beliefs = {"current_location": {"lat": 40.73, "lon": -73.995}, "traffic_detected": False}
        self.desires = {"deliver_package": None}
        self.intentions = []
        self.order_status = {}  # Track order status and route count

    class DeliveryBehaviour(CyclicBehaviour):
        async def run(self):
            print("DeliveryAgent: Waiting for message...")
            msg = await self.receive(timeout=20)
            if msg:
                print(f"DeliveryAgent: Received message from {msg.sender} with metadata: {msg.metadata}")
                try:
                    data = json.loads(msg.body)
                    print(f"DeliveryAgent: Parsed message: {data}")
                    order_id = data.get("order_id")
                    if data.get("type") == "assign_delivery":
                        if order_id not in self.agent.order_status:
                            self.agent.desires["deliver_package"] = data
                            self.agent.intentions.append("navigate")
                            self.agent.order_status[order_id] = {"status": "assigned", "route_count": 0}
                            print(f"DeliveryAgent: Assigned order {order_id}")
                            await self.request_route(data["destination"])
                    elif data.get("type") == "route_response":
                        print(f"DeliveryAgent: Received route for {order_id}: {data['route']}")
                        self.agent.order_status[order_id]["route_count"] += 1
                        await self.execute_delivery(data)
                        # Simulate traffic for ORD002 on initial route
                        if order_id == "ORD002" and self.agent.order_status[order_id]["route_count"] == 1:
                            self.agent.beliefs["traffic_detected"] = True
                            self.agent.intentions.append("reroute")
                            await self.request_reroute(order_id)
                except json.JSONDecodeError as e:
                    print(f"DeliveryAgent: JSON decode error: {e}")
            else:
                print("DeliveryAgent: No message received in timeout period")

        async def request_route(self, destination):
            order_id = self.agent.desires["deliver_package"]["order_id"]
            msg = Message(to="mapagent1@localhost")
            msg.set_metadata("performative", "request")
            msg.body = json.dumps({
                "type": "route_request",
                "order_id": order_id,
                "start": self.agent.beliefs["current_location"],
                "destination": destination
            })
            await self.send(msg)
            print(f"DeliveryAgent: Requested route for {order_id}")

        async def request_reroute(self, order_id):
            print(f"DeliveryAgent: Traffic detected, requesting reroute for {order_id}")
            msg = Message(to="mapagent1@localhost")
            msg.set_metadata("performative", "request")
            msg.body = json.dumps({
                "type": "reroute_request",
                "order_id": order_id,
                "start": self.agent.beliefs["current_location"],
                "destination": self.agent.desires["deliver_package"]["destination"]
            })
            await self.send(msg)

        async def execute_delivery(self, data):
            order_id = data["order_id"]
            route = data["route"]
            destination = self.agent.desires["deliver_package"]["destination"]
            self.agent.order_status[order_id]["status"] = "navigating"
            print(f"DeliveryAgent: Navigating to {order_id} destination")
            self.agent.beliefs["current_location"] = route[-1]
            # Report delivered only if at destination and not already delivered
            if route[-1] == destination and self.agent.order_status[order_id]["status"] != "delivered":
                # For ORD002, only report delivered after reroute (route_count >= 2)
                if order_id != "ORD002" or self.agent.order_status[order_id]["route_count"] >= 2:
                    await self.report_status(order_id, "delivered")
                    self.agent.order_status[order_id]["status"] = "delivered"

        async def report_status(self, order_id, status):
            msg = Message(to="taskagent1@localhost")
            msg.set_metadata("performative", "inform")
            msg.body = json.dumps({
                "type": "status_update",
                "order_id": order_id,
                "status": status
            })
            await self.send(msg)
            print(f"DeliveryAgent: Reported {status} for {order_id}")
            self.agent.desires["deliver_package"] = None
            self.agent.intentions = []
            self.agent.beliefs["traffic_detected"] = False

    async def setup(self):
        print("DeliveryAgent: Starting...")
        behaviour = self.DeliveryBehaviour()
        self.add_behaviour(behaviour)