from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


# Desactivamos el orden automático para personalizarlo abajo
@dataclass(order=False)
class Order:
    order_id: str
    customer_id: str
    items: list[dict[str, float]] = field(default_factory=list)
    tax_percentage: float = 16.0

    @property
    def subtotal(self) -> float:
        return sum(item['price'] * item.get('qty', 1) for item in self.items)

    @property
    def total(self) -> float:
        return round((self.subtotal + (self.subtotal * self.tax_percentage / 100)), 2)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other: Order) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.total < other.total

    def __le__(self, other: Order) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.total <= other.total


items_user_1 = [
    {'name': 'Laptop', 'price': 1000.0, 'qty': 1},
    {'name': 'Mouse', 'price': 50.0, 'qty': 2},
]
items_user_2 = [{'name': 'Smartphone', 'price': 600.0, 'qty': 1}]
items_user_3 = [
    {'name': 'Tablet', 'price': 300.0, 'qty': 1},
    {'name': 'Headphones', 'price': 80.0, 'qty': 1},
]

order_1 = Order('ORD-001', 'CUST-A', items_user_1, tax_percentage=16.0)
order_2 = Order('ORD-002', 'CUST-B', items_user_2, tax_percentage=16.0)
order_3 = Order('ORD-003', 'CUST-C', items_user_3, tax_percentage=16.0)

print(
    f"Pedido 1 - Subtotal: ${order_1.subtotal} | Total con impuesto: ${order_1.total}",
)
print(
    f"Pedido 2 - Subtotal: ${order_2.subtotal} | Total con impuesto: ${order_2.total}",
)
print(
    f"Pedido 3 - Subtotal: ${order_3.subtotal} | Total con impuesto: ${order_3.total}",
)

print(f"¿order_1 es igual a order_3? {order_1.__eq__(order_3)}")

print(f"¿order_2 es más barato que order_1? {order_2.__lt__(order_1)}")

orders_list = [order_1, order_2, order_3]
sorted_orders = sorted(orders_list)
print(f"Pedidos ordenados por total: {[o.total for o in sorted_orders]}")
