"""Консольный магазин «СпортТовары»."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PRODUCTS: list[dict[str, Any]] = [
    {"id": 1, "name": "Кроссовки RunFast", "brand": "Nike", "category": "Обувь", "price": 8990,
     "sizes": {41: 1, 42: 1, 43: 0}},
    {"id": 2, "name": "Мяч Pro Match", "brand": "Adidas", "category": "Мячи", "price": 2490,
     "sizes": {5: 12}},
    {"id": 3, "name": "Гантели 5 кг", "brand": "Torneo", "category": "Тренажёры", "price": 1590,
     "sizes": {"5 кг": 1}},
    {"id": 4, "name": "Футболка DryFit", "brand": "Nike", "category": "Одежда", "price": 2990,
     "sizes": {"M": 2, "L": 1}},
    {"id": 5, "name": "Ракетка Power", "brand": "Wilson", "category": "Ракетки", "price": 5490,
     "sizes": {"L2": 0}},
    {"id": 6, "name": "Бутсы Predator", "brand": "Adidas", "category": "Обувь", "price": 10990,
     "sizes": {40: 2, 41: 3, 42: 3}},
    {"id": 7, "name": "Коврик YogaPro", "brand": "Torneo", "category": "Йога", "price": 1990,
     "sizes": {"183 см": 3}},
    {"id": 8, "name": "Шорты Training", "brand": "Puma", "category": "Одежда", "price": 2490,
     "sizes": {"S": 5, "M": 6, "L": 4}},
]
# Совместимость со старым кодом: общий остаток qty = сумма по размерам
for _p in PRODUCTS:
    _p["qty"] = sum(_p["sizes"].values())

ORDERS: list[dict[str, Any]] = []


def stock_of(product: dict) -> int:
    """Общий остаток товара: сумма по размерам (sizes) или поле qty."""
    if "sizes" in product:
        return sum(product["sizes"].values())
    return product.get("qty", 0)


def get_low_stock(products: list[dict], threshold: int = 3) -> list[dict]:
    """Товары с суммарным остатком ≤ threshold (по всем размерам), по возрастанию остатка."""
    low = [p for p in products if stock_of(p) <= threshold]
    return sorted(low, key=stock_of)


def highlight_low_stock(products: list[dict], threshold: int = 3) -> str:
    """Текстовый отчёт о товарах с низким остатком."""
    low = get_low_stock(products, threshold)
    if not low:
        return "Нет товаров с низким остатком."
    lines = [f"Товары с остатком ≤ {threshold}:"]
    for p in low:
        lines.append(
            f"  [{p['id']}] {p['name']} ({p['brand']}) — {stock_of(p)} шт."
        )
    return "\n".join(lines)


def search_advanced(
    products: list[dict],
    query: str = "",
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """Комбинированный поиск по названию/бренду, категории и цене."""
    q = query.lower().strip()
    result = []
    for p in products:
        if q and q not in p["name"].lower() and q not in p["brand"].lower():
            continue
        if category and p["category"].lower() != category.lower():
            continue
        if min_price is not None and p["price"] < min_price:
            continue
        if max_price is not None and p["price"] > max_price:
            continue
        result.append(p)
    return result


def count_by_category(products: list[dict]) -> dict[str, int]:
    """Словарь {категория: суммарное количество единиц}."""
    counts: dict[str, int] = {}
    for p in products:
        cat = p["category"]
        counts[cat] = counts.get(cat, 0) + p.get("qty", 0)
    return counts


def save_orders(orders: list[dict], filename: str = "orders.json") -> Path:
    """Сохранение заказов в JSON. Возвращает путь к файлу."""
    path = Path(filename)
    path.write_text(json.dumps(orders, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def create_order(products: list[dict], product_id: int, qty: int) -> dict:
    """Оформление заказа: уменьшает остаток и добавляет запись в ORDERS."""
    for p in products:
        if p["id"] == product_id:
            if p["qty"] < qty:
                raise ValueError(f"Недостаточно товара: есть {p['qty']}, нужно {qty}")
            p["qty"] -= qty
            order = {
                "product_id": product_id,
                "name": p["name"],
                "qty": qty,
                "price": p["price"],
                "total": p["price"] * qty,
            }
            ORDERS.append(order)
            return order
    raise ValueError(f"Товар id={product_id} не найден")


# ---------- Корзина покупателя (US-5) ----------

def add_to_cart(cart: list[dict], products: list[dict], product_id: int,
                size: Any, quantity: int = 1) -> tuple[bool, str]:
    """Добавляет товар нужного размера в корзину. Возвращает (успех, сообщение)."""
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return False, f"Товар id={product_id} не найден"
    if size not in product.get("sizes", {}):
        return False, f"Размер {size} отсутствует у товара «{product['name']}»"
    if quantity <= 0:
        return False, "Количество должно быть больше нуля"
    in_cart = next((i for i in cart if i["id"] == product_id and i["size"] == size), None)
    already = in_cart["quantity"] if in_cart else 0
    if product["sizes"][size] < already + quantity:
        return False, f"Недостаточно товара размера {size}: есть {product['sizes'][size]} шт."
    if in_cart:
        in_cart["quantity"] += quantity
    else:
        cart.append({"id": product_id, "name": product["name"], "size": size,
                     "price": product["price"], "quantity": quantity})
    return True, f"«{product['name']}» (размер {size}) добавлен в корзину"


def cart_total(cart: list[dict]) -> int:
    """Итоговая сумма корзины."""
    return sum(item["price"] for item in cart)


def remove_from_cart(cart: list[dict], product_id: int, size: Any) -> bool:
    """Удаляет позицию из корзины. True, если позиция была найдена."""
    for i, item in enumerate(cart):
        if item["id"] == product_id and item["size"] == size:
            del cart[i]
            return True
    return False


def update_quantity(cart: list[dict], product_id: int, size: Any, quantity: int) -> bool:
    """Меняет количество позиции в корзине."""
    for item in cart:
        if item["id"] == product_id and item["size"] == size:
            item["quantity"] = quantity
            return True
    return False


def total_sum(products):
    return sum(p['price'] for p in products)


def main() -> None:
    print("=== СпортТовары ===")
    print(highlight_low_stock(PRODUCTS))
    print("Поиск nike:", [p["name"] for p in search_advanced(PRODUCTS, "nike")])
    print("По категориям:", count_by_category(PRODUCTS))
    order = create_order(PRODUCTS, 2, 1)
    path = save_orders(ORDERS)
    print(f"Заказ сохранён: {order} → {path}")


if __name__ == "__main__":
    main()
