import asyncio
import decimal
from datetime import timedelta

from flask import Flask, current_app, jsonify, make_response, request
from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleSpec,
    ScheduleState,
)

from activities import products
from shopping_cart import ScheduleWorkflow, ShoppingCartWorkflow

app = Flask(__name__)


async def connect_temporal(app):
    client: Client = await Client.connect("localhost:7233")
    app.temporal_client = client


def get_client() -> Client:
    return current_app.temporal_client


# Start Client
@app.route("/", methods=["POST"])
async def start():
    client: Client = get_client()
    if request.method == "POST":
        await client.start_workflow(
            ShoppingCartWorkflow.run,
            id="hello-signal-workflow-id",
            task_queue="hello-signal-task-queue",
        )

        message = jsonify({"message": "Resource created successfully"})
        response = make_response(message, 201)
        return response

    return jsonify({"message": "This endpoint requires a POST request."})


# Add item to cart
@app.route("/add_to_cart", methods=["POST"])
async def add_to_cart():
    client: Client = get_client()
    handle = client.get_workflow_handle(
        "hello-signal-workflow-id",
    )
    item: str = str(request.json["id"])
    await handle.signal(ShoppingCartWorkflow.add_to_cart, item)
    cart = await handle.query(ShoppingCartWorkflow.cart_details)
    for item in cart:
        if item["quantity"] >= 1:
            try:
                await client.create_schedule(
                    "workflow-schedule-id",
                    Schedule(
                        action=ScheduleActionStartWorkflow(
                            ScheduleWorkflow.run,
                            item,
                            id="hello-signal-workflow-id",
                            task_queue="hello-signal-task-queue",
                        ),
                        spec=ScheduleSpec(
                            intervals=[ScheduleIntervalSpec(every=timedelta(seconds=6))]
                        ),
                        state=ScheduleState(
                            limited_actions=True,
                            remaining_actions=1,
                        ),
                    ),
                )
            except Exception as e:
                print(e)
    message = jsonify({"message": f"Adding {item} to cart"})
    response = make_response(message, 200)
    return response


# Remove item from cart
@app.route("/remove_from_cart", methods=["DELETE"])
async def remove_from_cart():
    client: Client = get_client()
    handle = client.get_workflow_handle(
        "hello-signal-workflow-id",
    )
    item: str = str(request.json["id"])
    await handle.signal(ShoppingCartWorkflow.remove_from_cart, item)
    message = jsonify({"message": f"Removing {item} from cart"})

    response = make_response(message, 200)
    return response


# Checkout
@app.route("/checkout", methods=["POST"])
async def checkout():
    client: Client = get_client()
    handle = client.get_workflow_handle("hello-signal-workflow-id")
    schedule_handle = client.get_schedule_handle(
        "workflow-schedule-id",
    )
    await handle.signal(ShoppingCartWorkflow.exit)
    desc = await schedule_handle.describe()
    if desc != None:
        await schedule_handle.delete()
    results = await handle.result()

    async def get_total_price():
        total_price = decimal.Decimal(0)
        for product in results:
            total_price += decimal.Decimal(str(product["price"])) * product["quantity"]
        return f"{total_price:.2f}"

    total_price = await get_total_price()

    message = jsonify({"message": f"Checkout successful. Total price: ${total_price}"})
    response = make_response(message, 200)
    return response


@app.route("/cart", methods=["GET"])
async def cart():
    client: Client = get_client()
    handle = client.get_workflow_handle(
        "hello-signal-workflow-id",
    )
    cart = await handle.query(ShoppingCartWorkflow.cart_details)
    message = jsonify({"message": f"Cart: {cart}"})
    response = make_response(message, 200)
    return response


if __name__ == "__main__":
    asyncio.run(connect_temporal(app))
    app.run(debug=True)
