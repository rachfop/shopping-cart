import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import send_email
from shopping_cart import ScheduleWorkflow, ShoppingCartWorkflow


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    worker = Worker(
        client,
        task_queue="hello-signal-task-queue",
        workflows=[ShoppingCartWorkflow, ScheduleWorkflow],
        activities=[send_email],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
