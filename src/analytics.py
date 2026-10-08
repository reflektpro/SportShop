"""Модуль analytics — аналитика продаж по оформленным заказам."""
from __future__ import annotations


def total_revenue(orders: list[dict]) -> int:
    """Общая выручка по всем заказам."""
    return sum(o["total"] for o in orders)


def best_selling_product(orders: list[dict]) -> str | None:
    """Название самого продаваемого товара (по количеству единиц) или None."""
    sold: dict[str, int] = {}
    for o in orders:
        for i in o["items"]:
            sold[i["name"]] = sold.get(i["name"], 0) + i["quantity"]
    if not sold:
        return None
    return max(sold, key=sold.get)


def average_order_total(orders: list[dict]) -> float:
    """Средний чек (0, если заказов нет)."""
    if not orders:
        return 0
    return round(total_revenue(orders) / len(orders), 2)
