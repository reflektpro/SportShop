"""Модуль orders — оформление, вывод, сохранение и загрузка заказов."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.cart import cart_total
from src.catalog import find_product
from src.storage import read_json, write_json

_next_id = 1


def create_order(cart: list[dict], client_name: str, products: list[dict],
                 order_id: int | None = None) -> dict:
    """Оформляет заказ из корзины: списывает остатки со склада и очищает корзину.

    order_id — номер заказа; если не задан, берётся следующий номер счётчика модуля.
    ValueError — если корзина пуста, имя клиента пустое или товара на складе уже не хватает.
    """
    global _next_id
    if not cart:
        raise ValueError("Корзина пуста")
    for item in cart:
        product = find_product(products, item["id"])
        if product is None or product["sizes"].get(item["size"], 0) < item["quantity"]:
            raise ValueError(f"Недостаточно товара «{item['name']}» размера {item['size']}")
    if not client_name or not client_name.strip():
        raise ValueError("Не указано имя клиента")
    for item in cart:
        find_product(products, item["id"])["sizes"][item["size"]] -= item["quantity"]
    if order_id is None:
        order_id = _next_id
    order = {
        "id": order_id,
        "client": client_name,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "items": [{"id": i["id"], "name": i["name"], "size": i["size"],
                   "price": i["price"], "quantity": i["quantity"]} for i in cart],
        "total": cart_total(cart),
    }
    _next_id = max(_next_id, order_id) + 1
    cart.clear()
    return order


def print_order(order: dict) -> str:
    """Печатает заказ в консоль и возвращает его текст."""
    lines = [f"Заказ №{order['id']} от {order['date']}, клиент: {order['client']}"]
    for i in order["items"]:
        lines.append(f"  {i['name']} (размер {i['size']}) × {i['quantity']} = "
                     f"{i['price'] * i['quantity']} руб.")
    lines.append(f"  Итого: {order['total']} руб.")
    text = "\n".join(lines)
    print(text)
    return text


def save_orders(orders: list[dict], filename: str | Path = "data/orders.json") -> Path:
    """Сохраняет список заказов в JSON."""
    return write_json(orders, filename)


def load_orders(filename: str | Path = "data/orders.json") -> list[dict]:
    """Загружает заказы из JSON (пустой список, если файла нет)."""
    return read_json(filename, default=[])


def next_order_id(orders: list[dict]) -> int:
    """Номер для следующего заказа: максимальный id среди orders + 1 (1, если заказов нет)."""
    return max((o["id"] for o in orders), default=0) + 1
