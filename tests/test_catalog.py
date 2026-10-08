"""Модульные тесты src/catalog.py."""
import unittest

from src.catalog import avg_price, count_by_category, get_low_stock, search_advanced
from tests.helpers import catalog


class TestGetLowStock(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(get_low_stock([]), [])

    def test_no_low_stock(self):
        self.assertEqual(get_low_stock([{'name': 'A', 'sizes': {40: 10}}]), [])

    def test_one_low_stock(self):
        result = get_low_stock([{'name': 'A', 'sizes': {40: 1}}, {'name': 'B', 'sizes': {40: 10}}])
        self.assertEqual([p['name'] for p in result], ['A'])

    def test_sorted_by_stock(self):
        products = [{'name': 'A', 'sizes': {40: 3}}, {'name': 'B', 'sizes': {40: 0}}]
        self.assertEqual([p['name'] for p in get_low_stock(products)], ['B', 'A'])


class TestSearchAdvanced(unittest.TestCase):
    def test_by_name(self):
        self.assertEqual([p['id'] for p in search_advanced(catalog(), 'runfast')], [1])

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


class TestStatistics(unittest.TestCase):
    def test_count_by_category(self):
        self.assertEqual(count_by_category(catalog()),
                         {'Обувь': 2, 'Мячи': 12, 'Одежда': 14})

    def test_avg_price(self):
        self.assertEqual(avg_price(catalog()), 4240)

    def test_avg_price_empty(self):
        self.assertEqual(avg_price([]), 0)


if __name__ == '__main__':
    unittest.main()
