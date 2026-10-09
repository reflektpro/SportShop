"""Точка входа магазина «СпортТовары».

Без аргументов запускается демонстрация работы всех модулей (её использует build.py).
С аргументами работает как консольное приложение, например:

    python main.py catalog
    python main.py search nike --max-price 9000
    python main.py cart add 1 40 2
    python main.py checkout --client "Иванов И.И."
    python main.py analytics

Полный список команд: python main.py --help
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.analytics import average_order_total, best_selling_product, total_revenue
from src.cart import add_to_cart, cart_total, remove_from_cart, update_quantity
from src.catalog import (avg_price, count_by_category, get_low_stock, highlight_low_stock,
                         search_advanced, stock_of)
from src.orders import create_order, load_orders, next_order_id, print_order, save_orders
from src.storage import load_cart, load_products, save_cart, save_products

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE / "data"
PRODUCTS_FILE = DATA_DIR / "products.json"
ORDERS_FILE = DATA_DIR / "orders.json"

VERSION = "1.0"


# ---------------------------------------------------------------- демонстрация
def demo() -> None:
    """Демонстрационный сценарий: каталог → поиск → корзина → заказ → JSON → аналитика."""
    print("=== СпортТовары ===")
    products = load_products(PRODUCTS_FILE)
    print(f"Загружено товаров: {len(products)}, средняя цена: {avg_price(products)} руб.")
    print(highlight_low_stock(products))
    print("Поиск «nike»:", [p["name"] for p in search_advanced(products, "nike")])
    print("Остатки по категориям:", count_by_category(products))

    cart: list[dict] = []
    for product_id, size, qty in [(1, 40, 2), (2, 5, 1), (8, "M", 3)]:
        ok, message = add_to_cart(cart, products, product_id, size, qty)
        print(("[+] " if ok else "[!] ") + message)
    print(f"Сумма корзины: {cart_total(cart)} руб.")

    order = create_order(cart, "Лаптев В.И.", products)
    print_order(order)
    save_orders([order], ORDERS_FILE)
    orders = load_orders(ORDERS_FILE)
    print(f"Заказов в {ORDERS_FILE.relative_to(BASE)}: {len(orders)}")
    print(f"Выручка: {total_revenue(orders)} руб., средний чек: {average_order_total(orders)} руб., "
          f"хит продаж: {best_selling_product(orders)}")


# ---------------------------------------------------------------- вспомогательное
def parse_size(text: str):
    """Размер из командной строки: «40» → 40, «M» → «M», «5 кг» → «5 кг»."""
    return int(text) if text.isdigit() else text


def format_sizes(sizes: dict) -> str:
    return ", ".join(f"{k}: {v}" for k, v in sizes.items()) or "—"


def print_products(products: list[dict]) -> None:
    if not products:
        print("Товары не найдены.")
        return
    print(f"{'ID':>3}  {'Название':<20} {'Бренд':<8} {'Категория':<10} {'Цена':>7}  "
          f"{'Остаток':>7}  Размеры")
    for p in products:
        print(f"{p['id']:>3}  {p['name']:<20} {p['brand']:<8} {p['category']:<10} "
              f"{p['price']:>7}  {stock_of(p):>7}  {format_sizes(p['sizes'])}")


def print_cart(cart: list[dict]) -> None:
    if not cart:
        print("Корзина пуста.")
        return
    print("Корзина:")
    for i in cart:
        print(f"  [{i['id']}] {i['name']} (размер {i['size']}) × {i['quantity']} = "
              f"{i['price'] * i['quantity']} руб.")
    print(f"  Итого: {cart_total(cart)} руб.")


class Store:
    """Пути к файлам данных одного «магазина» (по умолчанию — папка data/)."""

    def __init__(self, data_dir: Path):
        self.dir = Path(data_dir)
        self.products_file = self.dir / "products.json"
        self.orders_file = self.dir / "orders.json"
        self.cart_file = self.dir / "cart.json"

    def products(self) -> list[dict]:
        if not self.products_file.exists():
            raise FileNotFoundError(f"Не найден файл каталога {self.products_file}")
        return load_products(self.products_file)


# ---------------------------------------------------------------- команды
def cmd_catalog(store: Store, args) -> int:
    products = store.products()
    print_products(products)
    print(f"Всего товаров: {len(products)}, средняя цена: {avg_price(products)} руб.")
    return 0


def cmd_search(store: Store, args) -> int:
    found = search_advanced(store.products(), args.query, args.category,
                            args.min_price, args.max_price)
    print_products(found)
    print(f"Найдено: {len(found)}")
    return 0


def cmd_low_stock(store: Store, args) -> int:
    print(highlight_low_stock(store.products(), args.threshold))
    return 0


def cmd_stats(store: Store, args) -> int:
    products = store.products()
    print(f"Товаров в каталоге: {len(products)}")
    print(f"Средняя цена: {avg_price(products)} руб.")
    print("Остатки по категориям:")
    for category, qty in sorted(count_by_category(products).items()):
        print(f"  {category:<10} {qty:>4} шт.")
    print(f"Товаров с низким остатком (≤ 3): {len(get_low_stock(products))}")
    return 0


def cmd_cart(store: Store, args) -> int:
    cart = load_cart(store.cart_file)
    if args.action == "show":
        print_cart(cart)
        return 0
    if args.action == "clear":
        save_cart([], store.cart_file)
        print("Корзина очищена.")
        return 0
    products = store.products()
    size = parse_size(args.size)
    if args.action == "add":
        ok, message = add_to_cart(cart, products, args.product_id, size, args.quantity)
    elif args.action == "remove":
        ok = remove_from_cart(cart, args.product_id, size)
        message = "Позиция удалена" if ok else "Такой позиции нет в корзине"
    else:  # set
        ok = update_quantity(cart, products, args.product_id, size, args.quantity)
        message = "Количество изменено" if ok else "Нельзя установить такое количество"
    print(("[+] " if ok else "[!] ") + message)
    if ok:
        save_cart(cart, store.cart_file)
    print_cart(cart)
    return 0 if ok else 1


def cmd_checkout(store: Store, args) -> int:
    cart = load_cart(store.cart_file)
    products = store.products()
    orders = load_orders(store.orders_file)
    try:
        order = create_order(cart, args.client, products, order_id=next_order_id(orders))
    except ValueError as e:
        print(f"[!] Заказ не оформлен: {e}")
        return 1
    print_order(order)
    orders.append(order)
    save_orders(orders, store.orders_file)
    save_products(products, store.products_file)
    save_cart(cart, store.cart_file)
    print(f"Заказ сохранён в {store.orders_file.name}, остатки на складе обновлены.")
    return 0


def cmd_orders(store: Store, args) -> int:
    source = Path(args.file) if args.file else store.orders_file
    orders = load_orders(source)
    if not orders:
        print(f"Заказов нет ({source.name}).")
        return 0
    print(f"Загружено заказов из {source.name}: {len(orders)}")
    for o in orders:
        print_order(o)
    if args.export:
        path = save_orders(orders, args.export)
        print(f"Заказы сохранены в {path}")
    return 0


def cmd_analytics(store: Store, args) -> int:
    orders = load_orders(store.orders_file)
    print(f"Заказов: {len(orders)}")
    print(f"Выручка: {total_revenue(orders)} руб.")
    print(f"Средний чек: {average_order_total(orders)} руб.")
    print(f"Хит продаж: {best_selling_product(orders) or '—'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py", description="СпортТовары — система управления магазином спортивных товаров. "
                                    "Без команды запускается демонстрация.")
    parser.add_argument("--version", action="version", version=f"СпортТовары {VERSION}")
    parser.add_argument("--data", default=str(DATA_DIR),
                        help="папка с products.json, orders.json и cart.json (по умолчанию data/)")
    sub = parser.add_subparsers(dest="command", metavar="КОМАНДА")

    sub.add_parser("demo", help="демонстрационный сценарий (то же, что запуск без команды)")
    p = sub.add_parser("catalog", help="показать весь каталог")
    p.set_defaults(func=cmd_catalog)

    p = sub.add_parser("search", help="поиск товара по названию, бренду, категории и цене")
    p.add_argument("query", nargs="?", default="", help="строка поиска (название/бренд/категория)")
    p.add_argument("--category", help="точная категория, например «Обувь»")
    p.add_argument("--min-price", type=float, help="минимальная цена, руб.")
    p.add_argument("--max-price", type=float, help="максимальная цена, руб.")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("low-stock", help="товары с низким остатком")
    p.add_argument("--threshold", type=int, default=3, help="порог остатка (по умолчанию 3)")
    p.set_defaults(func=cmd_low_stock)

    p = sub.add_parser("stats", help="статистика каталога")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("cart", help="корзина: show | add | remove | set | clear")
    csub = p.add_subparsers(dest="action", required=True, metavar="ДЕЙСТВИЕ")
    csub.add_parser("show", help="показать корзину")
    csub.add_parser("clear", help="очистить корзину")
    for name, text in (("add", "добавить товар"), ("remove", "удалить позицию"),
                       ("set", "изменить количество (0 — удалить)")):
        c = csub.add_parser(name, help=text)
        c.add_argument("product_id", type=int, help="id товара")
        c.add_argument("size", help="размер (40, M, «5 кг»)")
        if name != "remove":
            c.add_argument("quantity", type=int, nargs="?" if name == "add" else None,
                           default=1, help="количество")
    p.set_defaults(func=cmd_cart)

    p = sub.add_parser("checkout", help="оформить заказ из корзины")
    p.add_argument("--client", required=True, help="ФИО клиента")
    p.set_defaults(func=cmd_checkout)

    p = sub.add_parser("orders", help="загрузить и показать заказы")
    p.add_argument("--file", help="загрузить заказы из другого JSON-файла")
    p.add_argument("--export", metavar="ФАЙЛ", help="сохранить загруженные заказы в ФАЙЛ")
    p.set_defaults(func=cmd_orders)

    p = sub.add_parser("analytics", help="аналитика продаж по оформленным заказам")
    p.set_defaults(func=cmd_analytics)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command in (None, "demo"):
        demo()
        return 0
    try:
        return args.func(Store(Path(args.data)), args)
    except (FileNotFoundError, ValueError) as e:
        print(f"[!] Ошибка: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
