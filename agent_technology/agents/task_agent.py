from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json
import logging

# logging.basicConfig(level=logging.DEBUG)

class TaskAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.active_deliveries = {}

    class HandleRequests(CyclicBehaviour):
        async def run(self):
            print("TaskAgent: Waiting for message...")
            msg = await self.receive(timeout=20)
            if msg:
                print(f"TaskAgent: Received message from {msg.sender} with metadata: {msg.metadata}")
                print(f"TaskAgent: Message body: {msg.body}")
                try:
                    data = json.loads(msg.body)
                    print(f"TaskAgent: Parsed message: {data}")
                    if data.get("type") == "delivery_request":
                        order_id = data["order_id"]
                        print(f"TaskAgent: Processing delivery request {order_id}")
                        self.agent.active_deliveries[order_id] = "pending"
                        await self.assign_delivery(data)
                    elif data.get("type") == "status_update":
                        order_id = data["order_id"]
                        status = data["status"]
                        print(f"TaskAgent: Status update for {order_id}: {status}")
                        self.agent.active_deliveries[order_id] = status
                        if status == "delivered" and self.agent.active_deliveries.get(order_id) != "confirmed":
                            await self.notify_customer(data)
                    elif data.get("type") == "delivery_confirmed":
                        order_id = data["order_id"]
                        print(f"TaskAgent: Delivery confirmed for {order_id}")
                        self.agent.active_deliveries[order_id] = "confirmed"
                except json.JSONDecodeError as e:
                    print(f"TaskAgent: JSON decode error: {e}")
            else:
                print("TaskAgent: No message received in timeout period")

        async def assign_delivery(self, request):
            msg = Message(to="deliveryagent1@localhost")
            msg.set_metadata("performative", "request")
            msg.body = json.dumps({
                "type": "assign_delivery",
                "order_id": request["order_id"],
                "destination": request["destination"]
            })
            await self.send(msg)
            print(f"TaskAgent: Assigned {request['order_id']} to DeliveryAgent")

        async def notify_customer(self, update):
            msg = Message(to="customer1@localhost")
            msg.set_metadata("performative", "inform")
            msg.body = json.dumps({
                "type": "delivery_update",
                "order_id": update["order_id"],
                "status": update["status"]
            })
            await self.send(msg)
            print(f"TaskAgent: Notified customer about {update['order_id']} status")

    async def setup(self):
        print("TaskAgent: Starting...")
        behaviour = self.HandleRequests()
        self.add_behaviour(behaviour)