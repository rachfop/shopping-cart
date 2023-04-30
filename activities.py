from dataclasses import dataclass
from typing import List

from temporalio import activity


@dataclass
class Product:
    name: str
    description: str
    price: float
    quantity: int


products = {
    123: Product("Product A", "Description A", 10.99, 5),
    1234: Product("Product A2", "Description A", 10.99, 5),
    456: Product("Product B", "Description B", 5.99, 10),
    789: Product("Product C", "Description C", 20.99, 2),
}


@activity.defn
async def charge_customer(cart: List[Product]) -> float:
    total_price = 0.0
    print("Charging customer...")
    for product in cart:
        total_price += product.price * product.quantity
    return total_price
