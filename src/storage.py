"""Модуль storage — чтение и запись данных магазина в JSON-файлы."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _size_key(key: str) -> Any:
    """Размер из JSON всегда строка; числовые размеры (40, 41, 5) возвращаем как int."""
    return int(key) if key.isdigit() else key


def read_json(filename: str | Path, default: Any = None) -> Any:
    """Читает JSON-файл. Если файла нет — возвращает default."""
    path = Path(filename)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(data: Any, filename: str | Path) -> Path:
    """Записывает данные в JSON (UTF-8, с отступами). Возвращает путь к файлу."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_products(filename: str | Path = "data/products.json") -> list[dict]:
    """Загружает каталог товаров из JSON и приводит ключи размеров к исходным типам."""
    products = read_json(filename, default=[])
    for p in products:
        p["sizes"] = {_size_key(str(k)): v for k, v in p.get("sizes", {}).items()}
    return products


def save_products(products: list[dict], filename: str | Path = "data/products.json") -> Path:
    """Сохраняет каталог товаров в JSON."""
    return write_json(products, filename)


def load_cart(filename: str | Path = "data/cart.json") -> list[dict]:
    """Загружает сохранённую корзину (пустой список, если файла нет).

    Размеры приводятся к исходным типам так же, как в load_products.
    """
    cart = read_json(filename, default=[])
    for item in cart:
        item["size"] = _size_key(str(item["size"]))
    return cart


def save_cart(cart: list[dict], filename: str | Path = "data/cart.json") -> Path:
    """Сохраняет корзину в JSON, чтобы она сохранялась между запусками программы."""
    return write_json(cart, filename)
