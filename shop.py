"""Консольный магазин «СпортТовары»."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

PRODUCTS: list[dict[str, Any]] = [
    {"id": 1, "name": "Кроссовки RunFast", "brand": "Nike", "category": "Обувь", "price": 8990, "qty": 2},
    {"id": 2, "name": "Мяч Pro Match", "brand": "Adidas", "category": "Мячи", "price": 2490, "qty": 12},
    {"id": 3, "name": "Гантели 5 кг", "brand": "Torneo", "category": "Тренажёры", "price": 1590, "qty": 1},
    {"id": 4, "name": "Футболка DryFit", "brand": "Nike", "category": "Одежда", "price": 2990, "qty": 3},
    {"id": 5, "name": "Ракетка Power", "brand": "Wilson", "category": "Ракетки", "price": 5490, "qty": 0},
    {"id": 6, "name": "Бутсы Predator", "brand": "Adidas", "category": "Обувь", "price": 10990, "qty": 8},
    {"id": 7, "name": "Коврик YogaPro", "brand": "Torneo", "category": "Йога", "price": 1990, "qty": 3},
    {"id": 8, "name": "Шорты Training", "brand": "Puma", "category": "Одежда", "price": 2490, "qty": 15},
]
ORDERS: list[dict[str, Any]] = []


def get_low_stock(products: list[dict], threshold: int = 3) -> list[dict]:
    """Товары с суммарным количеством ≤ threshold, отсортированные по qty."""
    low = [p for p in products if p.get("qty", 0) <= threshold]
    return sorted(low, key=lambda p: p.get("qty", 0))


def highlight_low_stock(products: list[dict], threshold: int = 3) -> str:
    """Текстовый отчёт о товарах с низким остатком."""
    low = get_low_stock(products, threshold)
    if not low:
        return "Нет товаров с низким остатком."
    lines = [f"Товары с остатком ≤ {threshold}:"]
    for p in low:
        lines.append(f"  [{p['id']}] {p['name']} ({p['brand']}) — {p['qty']} шт.")
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

def main() -> None:
    print("=== СпортТовары ===")
    print(highlight_low_stock(PRODUCTS))
    print("Поиск nike:", [p["name"] for p in search_advanced(PRODUCTS, "nike")])

if __name__ == "__main__":
    main()
