"""Модульные тесты проекта SportShop (unittest)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shop import (get_low_stock, search_advanced, total_sum, cart_total,
                  add_to_cart, remove_from_cart, update_quantity)


def catalog():
    """Свежий тестовый каталог для каждого теста (тесты не влияют друг на друга)."""
    return [
        {'id': 1, 'name': 'Кроссовки RunFast', 'brand': 'Nike', 'category': 'Обувь',
         'price': 8990, 'sizes': {41: 1, 42: 1}},
        {'id': 2, 'name': 'Мяч Pro Match', 'brand': 'Adidas', 'category': 'Мячи',
         'price': 2490, 'sizes': {5: 12}},
        {'id': 3, 'name': 'Футболка DryFit', 'brand': 'Nike', 'category': 'Одежда',
         'price': 2990, 'sizes': {'M': 2, 'L': 1}},
        {'id': 4, 'name': 'Шорты Training', 'brand': 'Puma', 'category': 'Одежда',
         'price': 2490, 'sizes': {'S': 5, 'M': 6}},
    ]


class TestGetLowStock(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(get_low_stock([]), [])

    def test_no_low_stock(self):
        products = [{'name': 'A', 'sizes': {40: 10}}]
        self.assertEqual(get_low_stock(products), [])

    def test_one_low_stock(self):
        products = [
            {'name': 'A', 'sizes': {40: 1}},
            {'name': 'B', 'sizes': {40: 10}},
        ]
        result = get_low_stock(products)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'A')

    def test_sorted_by_stock(self):
        products = [{'name': 'A', 'sizes': {40: 3}}, {'name': 'B', 'sizes': {40: 0}}]
        self.assertEqual([p['name'] for p in get_low_stock(products)], ['B', 'A'])


class TestSearchAdvanced(unittest.TestCase):
    def test_by_name(self):
        result = search_advanced(catalog(), 'runfast')
        self.assertEqual([p['id'] for p in result], [1])

    def test_by_category(self):
        result = search_advanced(catalog(), '', category='одежда')
        self.assertEqual({p['id'] for p in result}, {3, 4})

    def test_by_price(self):
        result = search_advanced(catalog(), '', min_price=2500, max_price=9000)
        self.assertEqual({p['id'] for p in result}, {1, 3})

    def test_combined_filters(self):
        result = search_advanced(catalog(), 'nike', category='Одежда')
        self.assertEqual([p['id'] for p in result], [3])

    def test_invalid_price_range(self):
        with self.assertRaises(ValueError):
            search_advanced(catalog(), '', min_price=5000, max_price=1000)


class TestTotalSum(unittest.TestCase):
    def test_empty_cart(self):
        self.assertEqual(total_sum([]), 0)

    def test_cart_with_items(self):
        items = [{'price': 8990, 'quantity': 2}, {'price': 2490, 'quantity': 1}]
        self.assertEqual(total_sum(items), 20470)


class TestAddToCart(unittest.TestCase):
    def test_invalid_size(self):
        products = [{'id': 1, 'name': 'A', 'sizes': {40: 5}, 'price': 100}]
        cart = []
        result, message = add_to_cart(cart, products, 1, 99, 1)
        self.assertFalse(result)
        self.assertIn('размер', message.lower())

    def test_unknown_product(self):
        result, message = add_to_cart([], catalog(), 999, 41, 1)
        self.assertFalse(result)
        self.assertIn('не найден', message)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = 1 / 0


class TestCart(unittest.TestCase):
    def setUp(self):
        self.products = catalog()
        self.cart = []

    def test_add_success(self):
        ok, _ = add_to_cart(self.cart, self.products, 2, 5, 3)
        self.assertTrue(ok)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart[0]['quantity'], 3)

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
        self.assertTrue(update_quantity(self.cart, 4, 'S', 4))
        self.assertEqual(self.cart[0]['quantity'], 4)

    def test_update_quantity_zero_removes_item(self):
        add_to_cart(self.cart, self.products, 4, 'S', 2)
        update_quantity(self.cart, 4, 'S', 0)
        self.assertEqual(self.cart, [])

    def test_cart_total(self):
        add_to_cart(self.cart, self.products, 1, 42, 1)   # 8990
        add_to_cart(self.cart, self.products, 4, 'M', 2)  # 2 × 2490
        self.assertEqual(cart_total(self.cart), 13970)


if __name__ == '__main__':
    unittest.main()
