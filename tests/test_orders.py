"""Модульные тесты src/orders.py и src/storage.py."""
import io
import os
import tempfile
from contextlib import redirect_stdout
import unittest

from src.cart import add_to_cart
from src.orders import create_order, load_orders, print_order, save_orders
from src.storage import load_products, save_products
from tests.helpers import catalog


class TestCreateOrder(unittest.TestCase):
    def setUp(self):
        self.products = catalog()
        self.cart = []

    def test_empty_cart_raises(self):
        with self.assertRaises(ValueError):
            create_order([], 'Клиент', self.products)

    def test_order_decreases_stock_and_clears_cart(self):
        add_to_cart(self.cart, self.products, 2, 5, 3)
        order = create_order(self.cart, 'Клиент', self.products)
        self.assertEqual(order['total'], 3 * 2490)
        self.assertEqual(order['client'], 'Клиент')
        self.assertEqual(self.products[1]['sizes'][5], 9)
        self.assertEqual(self.cart, [])

    def test_print_order(self):
        add_to_cart(self.cart, self.products, 3, 'L', 1)
        with redirect_stdout(io.StringIO()):
            text = print_order(create_order(self.cart, 'Клиент', self.products))
        self.assertIn('Футболка DryFit', text)
        self.assertIn('Итого: 2990', text)


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_save_and_load_orders(self):
        path = os.path.join(self.tmp, 'orders.json')
        orders = [{'id': 1, 'total': 100, 'items': []}]
        save_orders(orders, path)
        self.assertEqual(load_orders(path), orders)

    def test_load_orders_missing_file(self):
        self.assertEqual(load_orders(os.path.join(self.tmp, 'nope.json')), [])

    def test_products_sizes_keep_type(self):
        path = os.path.join(self.tmp, 'products.json')
        save_products(catalog(), path)
        loaded = load_products(path)
        self.assertIn(41, loaded[0]['sizes'])      # числовой размер снова int
        self.assertIn('M', loaded[2]['sizes'])     # буквенный остаётся строкой


if __name__ == '__main__':
    unittest.main()
