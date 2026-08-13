from dataclasses import field
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict


class OrderIn(BaseModel):
    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    price: float
    tax_percentage: float = 16.0

    @property
    def subtotal(self) -> float:
        return sum(self.price * self.quantity)

    @property
    def total(self) -> float:
        return round((self.subtotal + (self.subtotal * self.tax_percentage / 100)), 2)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderIn):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other: "OrderIn") -> bool:
        if not isinstance(other, OrderIn):
            return NotImplemented
        return self.total < other.total

    def __le__(self, other: "OrderIn") -> bool:
        if not isinstance(other, OrderIn):
            return NotImplemented
        return self.total <= other.total


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    customer_id: int
    product_id: int
    quantity: int
    price: float
    tax_percentage: float = 16.0
    created_at: datetime

    @property
    def subtotal(self) -> float:
        return sum(self.price * self.quantity)

    @property
    def total(self) -> float:
        return round((self.subtotal + (self.subtotal * self.tax_percentage / 100)), 2)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderOut):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other: OrderOut) -> bool:
        if not isinstance(other, OrderOut):
            return NotImplemented
        return self.total < other.total

    def __le__(self, other: OrderOut) -> bool:
        if not isinstance(other, OrderOut):
            return NotImplemented
        return self.total <= other.total

class OrderEntity:
    def __init__(self, order_id=None, customer_id=None, product_id=None, quantity=None, price=None, tax_percentage=None, created_at=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.tax_percentage = tax_percentage
        self.created_at = created_at or datetime.now(timezone.utc)


order_entrada_1 = OrderIn(order_id=1, customer_id=1, product_id=1, quantity=1, price=1000.0, tax_percentage=16.0)
order_entrada_2 = OrderIn(order_id=2, customer_id=2, product_id=2, quantity=1, price=600.0, tax_percentage=16.0)
order_entrada_3 = OrderIn(order_id=3, customer_id=3, product_id=3, quantity=1, price=300.0, tax_percentage=16.0)

# --- PROCESO DE CONVERSIÓN ---

nueva_entidad = OrderEntity(**order_entrada_1.model_dump())

nueva_entidad.order_id = 1

respuesta_cliente = OrderOut.model_validate(nueva_entidad)

print(respuesta_cliente.json())

