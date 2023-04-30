from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    name: str
    description: str
    price: float
    quantity: int


products = {
    0: Product("iPhone 12 Pro", "Test description for ID 0", 999.99, 1),
    1: Product("iPhone 12", "Test description for ID 1", 699.99, 1),
    2: Product("iPhone SE", "Test description for ID 2", 399.99, 1),
    3: Product("iPhone 11", "Test description for ID 3", 599.99, 1),
}
