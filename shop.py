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

def main() -> None:
    print("=== СпортТовары ===")
    print(f"Товаров в каталоге: {len(PRODUCTS)}")

if __name__ == "__main__":
    main()
