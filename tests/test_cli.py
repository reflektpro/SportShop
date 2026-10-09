"""Тесты консольного интерфейса main.py (сценарии руководства пользователя)."""
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import main

BASE = Path(__file__).resolve().parents[1]


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.copy(BASE / 'data' / 'products.json', self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_cli(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main.main(['--data', self.tmp, *argv])
        return code, buf.getvalue()

    def test_catalog_lists_all_products(self):
        code, out = self.run_cli('catalog')
        self.assertEqual(code, 0)
        self.assertIn('Всего товаров: 8', out)
        self.assertIn('Бутсы Predator', out)

    def test_search_with_price_filter(self):
        code, out = self.run_cli('search', 'nike', '--max-price', '5000')
        self.assertEqual(code, 0)
        self.assertIn('Футболка DryFit', out)
        self.assertNotIn('Кроссовки RunFast', out)
        self.assertIn('Найдено: 1', out)

    def test_search_wrong_price_range_is_error(self):
        code, out = self.run_cli('search', '--min-price', '5000', '--max-price', '100')
        self.assertEqual(code, 1)
        self.assertIn('min_price не может быть больше max_price', out)

    def test_cart_is_saved_between_runs(self):
        self.run_cli('cart', 'add', '1', '40', '2')
        code, out = self.run_cli('cart', 'show')
        self.assertEqual(code, 0)
        self.assertIn('Итого: 17980 руб.', out)

    def test_cart_add_unknown_size_fails(self):
        code, out = self.run_cli('cart', 'add', '4', 'XL')
        self.assertEqual(code, 1)
        self.assertIn('Размер XL отсутствует', out)

    def test_checkout_saves_order_and_stock(self):
        self.run_cli('cart', 'add', '2', '5', '3')
        code, out = self.run_cli('checkout', '--client', 'Тестовый клиент')
        self.assertEqual(code, 0)
        self.assertIn('Итого: 7470 руб.', out)
        orders = json.loads((Path(self.tmp) / 'orders.json').read_text(encoding='utf-8'))
        self.assertEqual(len(orders), 1)
        products = json.loads((Path(self.tmp) / 'products.json').read_text(encoding='utf-8'))
        self.assertEqual(products[1]['sizes']['5'], 9)
        self.assertEqual(json.loads((Path(self.tmp) / 'cart.json').read_text(encoding='utf-8')), [])

    def test_order_numbers_continue_after_restart(self):
        for pid, size in (('2', '5'), ('8', 'M')):
            self.run_cli('cart', 'add', pid, size)
            self.run_cli('checkout', '--client', 'Клиент')
        code, out = self.run_cli('orders')
        self.assertIn('Заказ №1', out)
        self.assertIn('Заказ №2', out)

    def test_checkout_empty_cart_fails(self):
        code, out = self.run_cli('checkout', '--client', 'Клиент')
        self.assertEqual(code, 1)
        self.assertIn('Корзина пуста', out)

    def test_analytics_after_orders(self):
        self.run_cli('cart', 'add', '2', '5', '2')
        self.run_cli('checkout', '--client', 'Клиент')
        code, out = self.run_cli('analytics')
        self.assertIn('Выручка: 4980 руб.', out)
        self.assertIn('Хит продаж: Мяч Pro Match', out)

    def test_orders_export(self):
        self.run_cli('cart', 'add', '7', '183 см')
        self.run_cli('checkout', '--client', 'Клиент')
        target = Path(self.tmp) / 'backup.json'
        self.run_cli('orders', '--export', str(target))
        code, out = self.run_cli('orders', '--file', str(target))
        self.assertIn('Загружено заказов из backup.json: 1', out)


class TestNewApi(unittest.TestCase):
    def test_next_order_id(self):
        from src.orders import next_order_id
        self.assertEqual(next_order_id([]), 1)
        self.assertEqual(next_order_id([{'id': 3}, {'id': 7}]), 8)

    def test_create_order_requires_client(self):
        from src.orders import create_order
        from tests.helpers import catalog
        cart = [{'id': 2, 'name': 'Мяч Pro Match', 'size': 5, 'price': 2490, 'quantity': 1}]
        with self.assertRaises(ValueError):
            create_order(cart, '  ', catalog())

    def test_cart_roundtrip_keeps_size_types(self):
        from src.storage import load_cart, save_cart
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / 'cart.json'
            save_cart([{'id': 1, 'name': 'x', 'size': 40, 'price': 1, 'quantity': 1},
                       {'id': 4, 'name': 'y', 'size': 'M', 'price': 1, 'quantity': 1}], f)
            self.assertEqual([i['size'] for i in load_cart(f)], [40, 'M'])


if __name__ == '__main__':
    unittest.main()
