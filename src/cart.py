"""Модуль cart — корзина покупателя."""
from __future__ import annotations

from typing import Any

from src.catalog import find_product


def _find_line(cart: list[dict], product_id: int, size: Any) -> dict | None:
    return next((i for i in cart if i["id"] == product_id and i["size"] == size), None)


def add_to_cart(cart: list[dict], products: list[dict], product_id: int,
                size: Any, quantity: int = 1) -> tuple[bool, str]:
    """Добавляет товар нужного размера в корзину. Возвращает (успех, сообщение)."""
    product = find_product(products, product_id)
    if product is None:
        return False, f"Товар id={product_id} не найден"
    if size not in product.get("sizes", {}):
        return False, f"Размер {size} отсутствует у товара «{product['name']}»"
    if quantity <= 0:
        return False, "Количество должно быть больше нуля"
    line = _find_line(cart, product_id, size)
    already = line["quantity"] if line else 0
    if product["sizes"][size] < already + quantity:
        return False, f"Недостаточно товара размера {size}: есть {product['sizes'][size]} шт."
    if line:
        line["quantity"] += quantity
    else:
        cart.append({"id": product_id, "name": product["name"], "size": size,
                     "price": product["price"], "quantity": quantity})
    return True, f"«{product['name']}» (размер {size}) добавлен в корзину"


def remove_from_cart(cart: list[dict], product_id: int, size: Any) -> bool:
    """Удаляет позицию из корзины. True, если позиция была найдена."""
    line = _find_line(cart, product_id, size)
    if line is None:
        return False
    cart.remove(line)
    return True


def update_quantity(cart: list[dict], products: list[dict], product_id: int,
                    size: Any, new_qty: int) -> bool:
    """Меняет количество позиции. new_qty ≤ 0 удаляет позицию.

    Возвращает False, если позиции нет в корзине или на складе не хватает товара.
    """
    line = _find_line(cart, product_id, size)
    if line is None:
        return False
    if new_qty <= 0:
        cart.remove(line)
        return True
    product = find_product(products, product_id)
    if product is None or product["sizes"].get(size, 0) < new_qty:
        return False
    line["quantity"] = new_qty
    return True


def cart_total(cart: list[dict]) -> int:
    """Итоговая сумма корзины: цена × количество по каждой позиции."""
    return sum(item["price"] * item["quantity"] for item in cart)


def total_sum(items: list[dict]) -> int:
    """Сумма позиций с учётом количества (цена × quantity)."""
    return sum(p["price"] * p["quantity"] for p in items)
