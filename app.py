import asyncio

from flask import Flask, current_app, jsonify, make_response, request
from temporalio.client import Client

from activities import products
from greeting_workflow import GreetingWorkflow

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
            GreetingWorkflow.run,
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
    await handle.signal(GreetingWorkflow.add_to_cart, item)

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
    await handle.signal(GreetingWorkflow.remove_from_cart, item)
    message = jsonify({"message": f"Removing {item} from cart"})

    response = make_response(message, 200)
    return response


# Checkout
@app.route("/checkout", methods=["POST"])
async def checkout():
    client: Client = get_client()
    handle = client.get_workflow_handle("hello-signal-workflow-id")
    await handle.signal(GreetingWorkflow.exit)
    results = await handle.result()

    async def get_total_price():
        total_price = 0
        for product in results:
            total_price += product["price"] * product["quantity"]
        return total_price

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
    cart = await handle.query(GreetingWorkflow.cart_details)
    message = jsonify({"message": f"Cart: {cart}"})
    response = make_response(message, 200)
    return response


if __name__ == "__main__":
    asyncio.run(connect_temporal(app))
    app.run(debug=True)
