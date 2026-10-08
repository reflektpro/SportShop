# 16. Отчёт об интеграции модулей

## Модули проекта

| Модуль | Назначение | Основные функции |
|---|---|---|
| `src/catalog.py` | каталог товаров | `get_low_stock`, `search_advanced`, `count_by_category`, `avg_price`, `find_product` |
| `src/cart.py` | корзина покупателя | `add_to_cart`, `remove_from_cart`, `update_quantity`, `cart_total` |
| `src/orders.py` | заказы | `create_order`, `print_order`, `save_orders`, `load_orders` |
| `src/analytics.py` | аналитика продаж | `total_revenue`, `best_selling_product`, `average_order_total` |
| `src/storage.py` | работа с JSON | `load_products`, `save_products`, `read_json`, `write_json` |

Монолитный `shop.py` из практик 6–8 удалён: его функции разнесены по модулям,
модульные тесты `tests/test_shop.py` разделены на `test_catalog.py`,
`test_cart.py`, `test_orders.py`, `test_analytics.py`.

## Связи (импорты)

```
main.py ──► catalog, cart, orders, analytics, storage
cart    ──► catalog   (find_product)
orders  ──► cart      (cart_total), catalog (find_product), storage (read_json, write_json)
analytics — работает только с данными заказов, импортов нет
storage   — нижний уровень, импортов модулей проекта нет
```

Циклических зависимостей нет. Интеграция выполнялась снизу вверх:
`storage` → `catalog` → `cart` → `orders` → `analytics` → `main.py`.

## Интеграционные тесты (`tests/test_integration.py`)

| Тест | Что проверяет |
|---|---|
| `test_full_cycle` | каталог из `data/products.json` → корзина → заказ → сохранение в `data/test_orders.json` → загрузка, суммы совпадают |
| `test_order_updates_stock_for_catalog` | после заказа остаток уменьшился и товар попал в `get_low_stock` |
| `test_analytics_on_saved_orders` | `analytics` правильно считает выручку и хит продаж по заказам, прочитанным из файла |

Временный файл `data/test_orders.json` удаляется в `tearDown`.
Всего тестов в проекте: 39, все проходят.

## Найденные ошибки

1. Ключ `product` вместо `name` в позиции корзины — `KeyError` в `orders.create_order`.
2. Числовые размеры становятся строками после JSON — исправлено в `storage.load_products`.

Подробно — в [15_Integration_Errors.md](15_Integration_Errors.md).

## Сборка (`build.py`)

`python build.py` выполняет четыре шага и останавливается на первой ошибке:

1. `check_python_version()` — Python не ниже 3.8;
2. `check_data()` — все файлы проекта на месте, `data/products.json` читается и у каждого товара есть поля `id, name, brand, category, price, sizes`;
3. `run_tests()` — `python -m unittest discover -s tests -v`;
4. `run_app()` — запуск `main.py`.

При успехе выводится `СБОРКА УСПЕШНА` (код возврата 0), иначе `СБОРКА ПРЕРВАНА` (код 1).
