# 13. Отладка в VS Code

Конфигурация запуска: **Python: Current File** (`.vscode/launch.json`), запуск — F5.

## Сеанс 1. Точка останова в get_low_stock

**Где была точка останова?** `shop.py`, строка 43 — `return sorted(low, key=stock_of)`
внутри функции `get_low_stock`. Программа запускалась через `main()` → `highlight_low_stock()`.

**Стек вызовов (Call Stack):** `get_low_stock` (shop.py:43) ← `highlight_low_stock` (shop.py:48) ← `main`.

**Значения переменных (панель Variables):**

| Переменная | Значение |
|---|---|
| `threshold` | `3` |
| `products` | `list` из 8 товаров |
| `low` | `list` из 5 товаров (до сортировки): RunFast (2), Гантели (1), DryFit (3), Ракетка (0), YogaPro (3) |
| `low[0]['sizes']` | `{41: 1, 42: 1, 43: 0}` → `stock_of = 2` |

Шаги: **Step Over (F10)** — выполнение `return` без захода в `stock_of`;
**Step Into (F11)** — заход внутрь `stock_of(product)` и проверка суммы по размерам;
**Step Out (Shift+F11)** — возврат в `highlight_low_stock`.

После `return` порядок стал по возрастанию остатка:
Ракетка (0) → Гантели (1) → RunFast (2) → DryFit (3) → YogaPro (3). Функция работает верно.

## Сеанс 2. Поиск причины падения теста update_quantity

Тест `test_update_quantity_zero_removes_item` упал. Точка останова поставлена в
`update_quantity`, строка 166 (`item["quantity"] = quantity`), вызов `update_quantity(cart, 4, 'S', 0)`.

| Переменная | Значение |
|---|---|
| `product_id` | `4` |
| `size` | `'S'` |
| `quantity` | `0` |
| `item` | `{'id': 4, 'name': 'Шорты Training', 'size': 'S', 'price': 2490, 'quantity': 0}` |
| `len(cart)` | `1` |

**Какая ошибка была найдена?** При количестве `0` функция просто записывала `quantity = 0`,
а позиция оставалась в корзине (`len(cart) == 1`). Исправление: при `quantity <= 0`
позиция удаляется (`del cart[i]`). Коммит:
«fix: update_quantity удаляет позицию при количестве 0 (найдено тестом)».
