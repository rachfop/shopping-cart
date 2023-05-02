import asyncio
from datetime import timedelta
from typing import List

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import Product, products, send_email


@workflow.defn
class ShoppingCartWorkflow:
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
            while not self._add_to_cart.empty():
                product_id = int(self._add_to_cart.get_nowait())
                if product_id in products:
                    product = products[product_id]
                    # add 1 to quantity if product already in cart
                    product_in_cart = next(
                        (p for p in self._cart if p.name == product.name), None
                    )
                    if product_in_cart:
                        product_in_cart.quantity += 1
                    else:
                        new_product = Product(
                            name=product.name,
                            description=product.description,
                            price=product.price,
                            quantity=1,
                        )
                        self._cart.append(new_product)
                        print(
                            f"Added {new_product.name} to cart, costs {new_product.price}."
                        )
                        cart.append(new_product)

                else:
                    print(f"Product with ID {product_id} not found.")
            while not self._remove_from_cart.empty():
                product_id = int(self._remove_from_cart.get_nowait())
                if product_id in products:
                    product = products[product_id]
                    # add 1 to quantity if product already in cart
                    product_in_cart = next(
                        (p for p in self._cart if p.name == product.name), None
                    )
                    if product_in_cart:
                        product_in_cart.quantity -= 1
                        if product_in_cart.quantity == 0:
                            self._cart.remove(product_in_cart)
                            print(
                                f"Removed {product_in_cart.name} from cart, costs {product_in_cart.price}."
                            )
                            cart.remove(product_in_cart)
                else:
                    print(f"Product with ID {product_id} not found.")

            if self._exit:
                return cart
        return cart

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


@workflow.defn
class ScheduleWorkflow:
    @workflow.run
    async def run(self, cart: Product) -> None:
        await workflow.execute_activity(
            send_email,
            cart,
            start_to_close_timeout=timedelta(seconds=15),
        )
