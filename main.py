import asyncio

from greeting_workflow import ShoppingCartWorkflow
from temporalio.client import Client
from temporalio.worker import Worker


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    worker = Worker(
        client,
        task_queue="hello-signal-task-queue",
        workflows=[ShoppingCartWorkflow],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
