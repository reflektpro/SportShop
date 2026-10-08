"""Модульные тесты src/cart.py."""
import unittest

from src.cart import add_to_cart, cart_total, remove_from_cart, total_sum, update_quantity
from tests.helpers import catalog


class TestTotalSum(unittest.TestCase):
    def test_empty_cart(self):
        self.assertEqual(total_sum([]), 0)

    def test_cart_with_items(self):
        items = [{'price': 8990, 'quantity': 2}, {'price': 2490, 'quantity': 1}]
        self.assertEqual(total_sum(items), 20470)


class TestCart(unittest.TestCase):
    def setUp(self):
        self.products = catalog()
        self.cart = []

    def test_invalid_size(self):
        ok, message = add_to_cart(self.cart, self.products, 1, 99, 1)
        self.assertFalse(ok)
        self.assertIn('размер', message.lower())

    def test_unknown_product(self):
        ok, message = add_to_cart(self.cart, self.products, 999, 41, 1)
        self.assertFalse(ok)
        self.assertIn('не найден', message)

    def test_add_success(self):
        ok, _ = add_to_cart(self.cart, self.products, 2, 5, 3)
        self.assertTrue(ok)
        self.assertEqual(self.cart[0]['quantity'], 3)
        self.assertEqual(self.cart[0]['name'], 'Мяч Pro Match')

    def test_add_again_increases_quantity(self):
        add_to_cart(self.cart, self.products, 2, 5, 2)
        add_to_cart(self.cart, self.products, 2, 5, 3)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart[0]['quantity'], 5)

    def test_add_more_than_stock(self):
        ok, message = add_to_cart(self.cart, self.products, 1, 41, 2)
        self.assertFalse(ok)
        self.assertIn('недостаточно', message.lower())
        self.assertEqual(self.cart, [])

    def test_remove_from_cart(self):
        add_to_cart(self.cart, self.products, 3, 'M', 1)
        self.assertTrue(remove_from_cart(self.cart, 3, 'M'))
        self.assertEqual(self.cart, [])
        self.assertFalse(remove_from_cart(self.cart, 3, 'M'))

    def test_update_quantity(self):
        add_to_cart(self.cart, self.products, 4, 'S', 1)
        self.assertTrue(update_quantity(self.cart, self.products, 4, 'S', 4))
        self.assertEqual(self.cart[0]['quantity'], 4)

    def test_update_quantity_over_stock(self):
        add_to_cart(self.cart, self.products, 4, 'S', 1)
        self.assertFalse(update_quantity(self.cart, self.products, 4, 'S', 50))
        self.assertEqual(self.cart[0]['quantity'], 1)

    def test_update_quantity_zero_removes_item(self):
        add_to_cart(self.cart, self.products, 4, 'S', 2)
        update_quantity(self.cart, self.products, 4, 'S', 0)
        self.assertEqual(self.cart, [])

    def test_cart_total(self):
        add_to_cart(self.cart, self.products, 1, 42, 1)   # 8990
        add_to_cart(self.cart, self.products, 4, 'M', 2)  # 2 × 2490
        self.assertEqual(cart_total(self.cart), 13970)


if __name__ == '__main__':
    unittest.main()
