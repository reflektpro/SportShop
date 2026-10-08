"""Общие тестовые данные: свежий каталог для каждого теста."""


def catalog():
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
