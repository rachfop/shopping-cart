import asyncio
from datetime import timedelta
from typing import List

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import Product, charge_customer, products


@workflow.defn
class GreetingWorkflow:
    def __init__(self) -> None:
        self._add_to_cart: asyncio.Queue[str] = asyncio.Queue()
        self._remove_from_cart: asyncio.Queue[str] = asyncio.Queue()
        self._exit = False
        self._cart: List[Product] = []

    @workflow.run
    async def run(self) -> float:
        cart: List[Product] = []
        while True:
            await workflow.wait_condition(
                lambda: not self._add_to_cart.empty()
                or not self._remove_from_cart.empty()
                or self._exit
            )
            # Process signals
            while not self._add_to_cart.empty():
                product_id = int(self._add_to_cart.get_nowait())
                if product_id in products:
                    product = products[product_id]
                    if product.quantity > 0:
                        product.quantity -= 1
                        self._cart.append(product)
                        print(f"Added {product.name} to cart, costs {product.price}.")
                        cart.append(product)
                    else:
                        print(f"Product with ID {product.id} is out of stock.")
                else:
                    print(f"Product with ID {product_id} not found.")
            while not self._remove_from_cart.empty():
                item_to_remove = self._remove_from_cart.get_nowait()
                if item_to_remove in self._cart:
                    self._cart.remove(item_to_remove)

            # Charge customer if exit signal received
            if self._exit:
                print(cart)
                print("Checking out...")
                total_price = await workflow.execute_activity(
                    charge_customer,
                    cart,
                    start_to_close_timeout=timedelta(seconds=3),
                )
                print(f"Total price: ${total_price}")
                return total_price

    @workflow.signal
    async def add_to_cart(self, item: str) -> None:
        await self._add_to_cart.put(item)

    @workflow.signal
    async def remove_from_cart(self, item: str) -> None:
        await self._remove_from_cart.put(item)

    @workflow.signal
    def exit(self) -> None:
        self._exit = True

    @workflow.query
    def cart_details(self):
        return self._cart
