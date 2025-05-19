from spade import agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import json
import asyncio
import logging

# logging.basicConfig(level=logging.DEBUG)

class CustomerAgent(agent.Agent):
    class HandleMessages(CyclicBehaviour):
        async def run(self):
            # Wait for delivery updates
            msg = await self.receive(timeout=20)
            if msg:
                print(f"CustomerAgent: Received message from {msg.sender} with metadata: {msg.metadata}")
                try:
                    data = json.loads(msg.body)
                    print(f"CustomerAgent: Parsed message: {data}")
                    if data.get("type") == "delivery_update":
                        order_id = data["order_id"]
                        status = data["status"]
                        print(f"CustomerAgent: Received update for {order_id}: {status}")
                        if status == "delivered":
                            # Send confirmation
                            reply = Message(to="taskagent1@localhost")
                            reply.set_metadata("performative", "inform")
                            reply.body = json.dumps({
                                "type": "delivery_confirmed",
                                "order_id": order_id
                            })
                            await self.send(reply)
                            print(f"CustomerAgent: Confirmed delivery for {order_id}")
                except json.JSONDecodeError as e:
                    print(f"CustomerAgent: JSON decode error: {e}")
            else:
                print("CustomerAgent: No update received in timeout period")

    class SendDeliveryRequest(OneShotBehaviour):
        async def run(self):
            # Wait for agents to connect to Openfire
            print("CustomerAgent: Waiting 5 seconds for agent synchronization...")
            await asyncio.sleep(5)

            # Send ORD001 (Scenario 1)
            msg = Message(to="taskagent1@localhost")
            msg.set_metadata("performative", "request")
            msg.body = json.dumps({
                "type": "delivery_request",
                "order_id": "ORD001",
                "destination": {"lat": 40.7128, "lon": -74.0060}
            })
            await self.send(msg)
            print(f"CustomerAgent: Sent delivery request for ORD001")

            # Wait before sending ORD002 (Scenario 2)
            await asyncio.sleep(20)

            # Send ORD002
            msg = Message(to="taskagent1@localhost")
            msg.set_metadata("performative", "request")
            msg.body = json.dumps({
                "type": "delivery_request",
                "order_id": "ORD002",
                "destination": {"lat": 40.7128, "lon": -74.0060}
            })
            await self.send(msg)
            print(f"CustomerAgent: Sent delivery request for ORD002")

    async def setup(self):
        print("CustomerAgent: Starting...")
        self.add_behaviour(self.HandleMessages())
        self.add_behaviour(self.SendDeliveryRequest())