"""Модульные тесты src/analytics.py."""
import unittest

from src.analytics import average_order_total, best_selling_product, total_revenue

ORDERS = [
    {'total': 17980, 'items': [{'name': 'Кроссовки RunFast', 'quantity': 2}]},
    {'total': 7470, 'items': [{'name': 'Мяч Pro Match', 'quantity': 3}]},
    {'total': 4980, 'items': [{'name': 'Шорты Training', 'quantity': 2}]},
]


class TestAnalytics(unittest.TestCase):
    def test_total_revenue(self):
        self.assertEqual(total_revenue(ORDERS), 30430)

    def test_total_revenue_empty(self):
        self.assertEqual(total_revenue([]), 0)

    def test_best_selling_product(self):
        self.assertEqual(best_selling_product(ORDERS), 'Мяч Pro Match')

    def test_best_selling_empty(self):
        self.assertIsNone(best_selling_product([]))

    def test_average_order_total(self):
        self.assertEqual(average_order_total(ORDERS), round(30430 / 3, 2))

    def test_average_order_total_empty(self):
        self.assertEqual(average_order_total([]), 0)


if __name__ == '__main__':
    unittest.main()
