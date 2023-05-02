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
@app.route("/<string:email>", methods=["POST"])
async def start(email):
    client: Client = get_client()
    if request.method == "POST":
        await client.start_workflow(
            ShoppingCartWorkflow.run,
            id=f"shopping-cart-workflow-{email}",
            task_queue="shopping-cart-task-queue",
        )

        message = jsonify(
            {"message": f"Resource created successfully for email: {email}"}
        )
        response = make_response(message, 201)
        return response

    return jsonify({"message": "This endpoint requires a POST request."})


# Add item to cart
@app.route("/<string:email>/add_to_cart", methods=["POST"])
async def add_to_cart(email):
    client: Client = get_client()
    handle = client.get_workflow_handle(
        f"shopping-cart-workflow-{email}",
    )
    item: str = str(request.json["id"])
    await handle.signal(ShoppingCartWorkflow.add_to_cart, item)
    cart = await handle.query(ShoppingCartWorkflow.cart_details)
    for item in cart:
        if item["quantity"] >= 1:
            try:
                await client.create_schedule(
                    f"workflow-schedule-id-{email}",
                    Schedule(
                        action=ScheduleActionStartWorkflow(
                            ScheduleWorkflow.run,
                            item,
                            id=f"shopping-cart-workflow-{email}",
                            task_queue="shopping-cart-task-queue",
                        ),
                        spec=ScheduleSpec(
                            intervals=[ScheduleIntervalSpec(every=timedelta(seconds=5))]
                        ),
                        state=ScheduleState(
                            limited_actions=True,
                            remaining_actions=1,
                        ),
                    ),
                )
            except Exception as e:
                print(e)
    message = jsonify(
        {"message": f"Item with ID {item} added to cart for email: {email}"}
    )
    response = make_response(message, 200)
    return response


# Remove item from cart
@app.route("/<string:email>/remove_from_cart", methods=["DELETE"])
async def remove_from_cart(email):
    client: Client = get_client()
    handle = client.get_workflow_handle(
        f"shopping-cart-workflow-{email}",
    )
    item: str = str(request.json["id"])
    await handle.signal(ShoppingCartWorkflow.remove_from_cart, item)
    message = jsonify(
        {"message": f"Item with ID {item} removed from cart for email: {email}"}
    )
    response = make_response(message, 200)
    return response


# Checkout
@app.route("/<string:email>/checkout", methods=["POST"])
async def checkout(email):
    client: Client = get_client()
    handle = client.get_workflow_handle(
        f"shopping-cart-workflow-{email}",
    )
    schedule_handle = client.get_schedule_handle(
        f"workflow-schedule-id-{email}",
    )
    await handle.signal(ShoppingCartWorkflow.exit)
    desc = await schedule_handle.describe()
    if desc != None:
        await schedule_handle.delete()
    results = await handle.result()

    async def get_total_price() -> decimal.Decimal:
        total_price = decimal.Decimal(0)
        for product in results:
            total_price += decimal.Decimal(str(product["price"])) * product["quantity"]
        return total_price

    total_price = await get_total_price()
    message = jsonify(
        {
            "message": f"Checkout successful. Total price: ${total_price:.2f} for email: {email}"
        }
    )

    response = make_response(message, 200)
    return response


@app.route("/<string:email>/cart", methods=["GET"])
async def cart(email):
    client: Client = get_client()
    handle = client.get_workflow_handle(
        f"shopping-cart-workflow-{email}",
    )
    cart = await handle.query(ShoppingCartWorkflow.cart_details)
    message = jsonify({"message": f"Shopping cart contents for email: {email}: {cart}"})
    response = make_response(message, 200)
    return response


if __name__ == "__main__":
    asyncio.run(connect_temporal(app))
    app.run(debug=True)
