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
    0: Product("iPhone 12 Pro", "Test description for ID 0", 999.99, 0),
    1: Product("iPhone 12", "Test description for ID 1", 699.99, 0),
    2: Product("iPhone SE", "Test description for ID 2", 399.99, 0),
    3: Product("iPhone 11", "Test description for ID 3", 599.99, 0),
}


@activity.defn
async def send_email(item: Product) -> str:
    print(
        f"Did you forget something? Looks like you left your cart with: {item.name} in your basket."
    )
    return "Did you forget something? Looks like you left your cart with: {item.name} in your basket."
