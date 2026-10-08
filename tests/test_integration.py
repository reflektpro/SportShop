"""Интеграционные тесты: catalog + cart + orders + storage + analytics вместе."""
import os
import unittest
from pathlib import Path

from src.analytics import best_selling_product, total_revenue
from src.cart import add_to_cart, cart_total
from src.catalog import get_low_stock
from src.orders import create_order, load_orders, save_orders
from src.storage import load_products

BASE = Path(__file__).resolve().parents[1]


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.products = load_products(BASE / 'data' / 'products.json')
        self.cart = []
        self.orders_file = BASE / 'data' / 'test_orders.json'

    def tearDown(self):
        if os.path.exists(self.orders_file):
            os.remove(self.orders_file)

    def test_full_cycle(self):
        """Каталог → корзина → заказ → сохранение → загрузка."""
        ok, _ = add_to_cart(self.cart, self.products, 1, 40, 2)
        self.assertTrue(ok)
        order = create_order(self.cart, 'Тестовый клиент', self.products)
        self.assertGreater(order['total'], 0)
        save_orders([order], self.orders_file)
        loaded = load_orders(self.orders_file)
        self.assertEqual(loaded[0]['total'], order['total'])

    def test_order_updates_stock_for_catalog(self):
        """После заказа catalog видит уменьшившийся остаток."""
        add_to_cart(self.cart, self.products, 1, 40, 2)
        create_order(self.cart, 'Тестовый клиент', self.products)
        self.assertEqual(self.products[0]['sizes'][40], 0)
        self.assertIn(1, [p['id'] for p in get_low_stock(self.products)])

    def test_analytics_on_saved_orders(self):
        """analytics корректно считает заказы, прочитанные из файла."""
        orders = []
        for pid, size, qty in [(2, 5, 3), (8, 'M', 1)]:
            add_to_cart(self.cart, self.products, pid, size, qty)
            expected = cart_total(self.cart)
            orders.append(create_order(self.cart, 'Тестовый клиент', self.products))
            self.assertEqual(orders[-1]['total'], expected)
        save_orders(orders, self.orders_file)
        loaded = load_orders(self.orders_file)
        self.assertEqual(total_revenue(loaded), 3 * 2490 + 2490)
        self.assertEqual(best_selling_product(loaded), 'Мяч Pro Match')


if __name__ == '__main__':
    unittest.main()
