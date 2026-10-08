"""Точка входа магазина «СпортТовары»: демонстрация работы всех модулей вместе."""
from pathlib import Path

from src.analytics import average_order_total, best_selling_product, total_revenue
from src.cart import add_to_cart, cart_total
from src.catalog import avg_price, count_by_category, highlight_low_stock, search_advanced
from src.orders import create_order, load_orders, print_order, save_orders
from src.storage import load_products

BASE = Path(__file__).resolve().parent
PRODUCTS_FILE = BASE / "data" / "products.json"
ORDERS_FILE = BASE / "data" / "orders.json"


def main() -> None:
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


if __name__ == "__main__":
    main()
