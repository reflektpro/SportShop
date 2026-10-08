"""Модуль catalog — работа с каталогом товаров: поиск, остатки, статистика."""
from __future__ import annotations


def stock_of(product: dict) -> int:
    """Общий остаток товара: сумма по размерам (sizes) или поле qty."""
    if "sizes" in product:
        return sum(product["sizes"].values())
    return product.get("qty", 0)


def find_product(products: list[dict], product_id: int) -> dict | None:
    """Товар по id или None, если такого нет."""
    return next((p for p in products if p["id"] == product_id), None)


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
        lines.append(f"  [{p['id']}] {p['name']} ({p['brand']}) — {stock_of(p)} шт.")
    return "\n".join(lines)


def search_advanced(
    products: list[dict],
    query: str = "",
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """Комбинированный поиск по названию/бренду/категории, категории и диапазону цен.

    Пустой запрос и None в фильтрах означают «без ограничения».
    Если min_price > max_price — выбрасывается ValueError.
    """
    if min_price is not None and max_price is not None and min_price > max_price:
        raise ValueError("min_price не может быть больше max_price")
    q = query.lower().strip()
    result = []
    for p in products:
        haystack = f"{p['name']} {p['brand']} {p['category']}".lower()
        if q and q not in haystack:
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
    """Словарь {категория: суммарное количество единиц на складе}."""
    counts: dict[str, int] = {}
    for p in products:
        counts[p["category"]] = counts.get(p["category"], 0) + stock_of(p)
    return counts


def avg_price(products: list[dict]) -> float:
    """Средняя цена товаров каталога (0, если каталог пуст)."""
    if not products:
        return 0
    return round(sum(p["price"] for p in products) / len(products), 2)
