from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
import logging

# logging.basicConfig(level=logging.DEBUG)

class MapAgent(agent.Agent):
    class RouteBehaviour(CyclicBehaviour):
        async def run(self):
            print("MapAgent: Waiting for message...")
            msg = await self.receive(timeout=20)
            if msg:
                print(f"MapAgent: Received message from {msg.sender} with metadata: {msg.metadata}")
                try:
                    data = json.loads(msg.body)
                    print(f"MapAgent: Parsed message: {data}")
                    order_id = data["order_id"]
                    if data.get("type") == "route_request":
                        print(f"MapAgent: Processing route request for {order_id}")
                        route = self.compute_route(data["start"], data["destination"])
                        await self.send_route(order_id, route)
                    elif data.get("type") == "reroute_request":
                        print(f"MapAgent: Processing reroute request for {order_id}")
                        route = self.compute_alternative_route(data["start"], data["destination"])
                        await self.send_route(order_id, route)
                except json.JSONDecodeError as e:
                    print(f"MapAgent: JSON decode error: {e}")
            else:
                print("MapAgent: No message received in timeout period")

        def compute_route(self, start, destination):
            return [
                start,
                {"lat": 40.7214, "lon": -74.0005},
                destination
            ]

        def compute_alternative_route(self, start, destination):
            return [
                start,
                {"lat": 40.717, "lon": -74.003},
                destination
            ]

        async def send_route(self, order_id, route):
            msg = Message(to="deliveryagent1@localhost")
            msg.set_metadata("performative", "inform")
            msg.body = json.dumps({
                "type": "route_response",
                "order_id": order_id,
                "route": route
            })
            await self.send(msg)
            print(f"MapAgent: Sent route for {order_id}")

    async def setup(self):
        print("MapAgent: Starting...")
        behaviour = self.RouteBehaviour()
        self.add_behaviour(behaviour)