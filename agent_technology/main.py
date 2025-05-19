from agents.customer_agent import CustomerAgent
from agents.task_agent import TaskAgent
from agents.delivery_agent import DeliveryAgent
from agents.map_agent import MapAgent
from config.openfire_config import AGENT_CREDENTIALS
import asyncio

async def main():
    agents = [
        CustomerAgent("customer1@localhost", AGENT_CREDENTIALS["customer1@localhost"]),
        TaskAgent("taskagent1@localhost", AGENT_CREDENTIALS["taskagent1@localhost"]),
        DeliveryAgent("deliveryagent1@localhost", AGENT_CREDENTIALS["deliveryagent1@localhost"]),
        MapAgent("mapagent1@localhost", AGENT_CREDENTIALS["mapagent1@localhost"])
    ]

    for agent in agents:
        await agent.start()

    # Keep running for 120 seconds to allow both scenarios
    await asyncio.sleep(120)

    for agent in agents:
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())