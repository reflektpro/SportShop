# 17. Справочник API (API Reference)

Проект: **СпортТовары — система управления магазином** (SportShop), версия 1.0.  
Автор: Лаптев В.И., группа 3ИП7-24.

Описаны все публичные функции пакета `src` (функции, имя которых начинается с `_`, внутренние и не описываются). Для каждой функции приведены назначение, параметры, возвращаемое значение, пример и исключения. Примеры выполнены из корня проекта; вывод под примером — реальный результат запуска (в примерах, где нужен каталог, он предварительно загружен: `products = load_products('data/products.json')`; `TMP` — временная папка).

## Содержание

- **`src.catalog`** — каталог товаров: [`stock_of`](#stock_of), [`find_product`](#find_product), [`get_low_stock`](#get_low_stock), [`highlight_low_stock`](#highlight_low_stock), [`search_advanced`](#search_advanced), [`count_by_category`](#count_by_category), [`avg_price`](#avg_price)
- **`src.cart`** — корзина покупателя: [`add_to_cart`](#add_to_cart), [`remove_from_cart`](#remove_from_cart), [`update_quantity`](#update_quantity), [`cart_total`](#cart_total), [`total_sum`](#total_sum)
- **`src.orders`** — заказы: [`create_order`](#create_order), [`print_order`](#print_order), [`save_orders`](#save_orders), [`load_orders`](#load_orders), [`next_order_id`](#next_order_id)
- **`src.analytics`** — аналитика продаж: [`total_revenue`](#total_revenue), [`best_selling_product`](#best_selling_product), [`average_order_total`](#average_order_total)
- **`src.storage`** — хранение данных в JSON: [`read_json`](#read_json), [`write_json`](#write_json), [`load_products`](#load_products), [`save_products`](#save_products), [`load_cart`](#load_cart), [`save_cart`](#save_cart)

Всего функций: **26**.

## Структуры данных

**Товар** (`data/products.json`):

```json
{"id": 1, "name": "Кроссовки RunFast", "brand": "Nike", "category": "Обувь", "price": 8990,
 "sizes": {"40": 2, "41": 1, "42": 1, "43": 0}}
```

**Позиция корзины**: `{"id": 1, "name": "Кроссовки RunFast", "size": 40, "price": 8990, "quantity": 2}`.

**Заказ** (`data/orders.json`): `{"id": 1, "client": "Лаптев В.И.", "date": "2026-10-09 10:00", "items": [позиции], "total": 17980}`.

## Модуль `src.catalog`

Модуль catalog — работа с каталогом товаров: поиск, остатки, статистика.

### `stock_of`

```python
stock_of(product: dict) -> int
```

**Назначение.** Возвращает общий остаток товара на складе: сумму остатков по всем размерам (`sizes`). Для товаров старого формата без размеров берётся поле `qty`.

**Параметры:**

- `product` (`dict`) — товар из каталога.

**Возвращает:** `int` — количество единиц товара.

**Пример:**

```python
from src.catalog import stock_of
print(stock_of(products[0]))  # Кроссовки RunFast: 2 + 1 + 1 + 0
```

Результат:

```text
4
```

**Исключения:** Не выбрасывает (у товара без `sizes` и `qty` остаток 0).

### `find_product`

```python
find_product(products: list[dict], product_id: int) -> dict | None
```

**Назначение.** Ищет товар по идентификатору.

**Параметры:**

- `products` (`list[dict]`) — каталог товаров.
- `product_id` (`int`) — id товара.

**Возвращает:** `dict | None` — найденный товар или `None`.

**Пример:**

```python
from src.catalog import find_product
print(find_product(products, 6)['name'])
print(find_product(products, 99))
```

Результат:

```text
Бутсы Predator
None
```

**Исключения:** Не выбрасывает.

### `get_low_stock`

```python
get_low_stock(products: list[dict], threshold: int = 3) -> list[dict]
```

**Назначение.** Возвращает товары, суммарный остаток которых по всем размерам не больше порога. Список отсортирован по возрастанию остатка — первыми идут товары, которые закончились.

**Параметры:**

- `products` (`list[dict]`) — каталог товаров.
- `threshold` (`int`, по умолчанию `3`) — порог остатка.

**Возвращает:** `list[dict]` — товары с низким остатком (новый список, каталог не изменяется).

**Пример:**

```python
from src.catalog import get_low_stock
low = get_low_stock(products)
for p in low:
    print(p['name'])
```

Результат:

```text
Ракетка Power
Гантели 5 кг
Футболка DryFit
Коврик YogaPro
```

**Исключения:** Не выбрасывает.

### `highlight_low_stock`

```python
highlight_low_stock(products: list[dict], threshold: int = 3) -> str
```

**Назначение.** Формирует текстовый отчёт о товарах с низким остатком (для вывода в консоль).

**Параметры:**

- `products` (`list[dict]`) — каталог товаров.
- `threshold` (`int`, по умолчанию `3`) — порог остатка.

**Возвращает:** `str` — многострочный отчёт или строка «Нет товаров с низким остатком.».

**Пример:**

```python
from src.catalog import highlight_low_stock
print(highlight_low_stock(products, threshold=1))
```

Результат:

```text
Товары с остатком ≤ 1:
  [5] Ракетка Power (Wilson) — 0 шт.
  [3] Гантели 5 кг (Torneo) — 1 шт.
```

**Исключения:** Не выбрасывает.

### `search_advanced`

```python
search_advanced(products: list[dict], query: str = , category: str | None = None, min_price: float | None = None, max_price: float | None = None) -> list[dict]
```

**Назначение.** Комбинированный поиск: подстрока в названии, бренде или категории (без учёта регистра), точная категория и диапазон цен. Пустой запрос и `None` в фильтрах означают «без ограничения».

**Параметры:**

- `products` (`list[dict]`) — каталог товаров.
- `query` (`str`, по умолчанию `""`) — строка поиска.
- `category` (`str | None`, по умолчанию `None`) — категория (без учёта регистра).
- `min_price` (`float | None`, по умолчанию `None`) — минимальная цена.
- `max_price` (`float | None`, по умолчанию `None`) — максимальная цена.

**Возвращает:** `list[dict]` — подходящие товары в порядке каталога.

**Пример:**

```python
from src.catalog import search_advanced
print([p['name'] for p in search_advanced(products, 'nike')])
print([p['name'] for p in search_advanced(products, category='обувь', max_price=10000)])
```

Результат:

```text
['Кроссовки RunFast', 'Футболка DryFit']
['Кроссовки RunFast']
```

**Исключения:** `ValueError` — если `min_price > max_price`.

### `count_by_category`

```python
count_by_category(products: list[dict]) -> dict[str, int]
```

**Назначение.** Подсчитывает суммарное количество единиц на складе по каждой категории.

**Параметры:**

- `products` (`list[dict]`) — каталог товаров.

**Возвращает:** `dict[str, int]` — словарь `{категория: количество}`.

**Пример:**

```python
from src.catalog import count_by_category
print(count_by_category(products))
```

Результат:

```text
{'Обувь': 12, 'Мячи': 12, 'Тренажёры': 1, 'Одежда': 18, 'Ракетки': 0, 'Йога': 3}
```

**Исключения:** Не выбрасывает.

### `avg_price`

```python
avg_price(products: list[dict]) -> float
```

**Назначение.** Вычисляет среднюю цену товаров каталога с округлением до копеек.

**Параметры:**

- `products` (`list[dict]`) — каталог товаров.

**Возвращает:** `float` — средняя цена; `0` для пустого каталога.

**Пример:**

```python
from src.catalog import avg_price
print(avg_price(products))
print(avg_price([]))
```

Результат:

```text
4627.5
0
```

**Исключения:** Не выбрасывает.

## Модуль `src.cart`

Модуль cart — корзина покупателя.

### `add_to_cart`

```python
add_to_cart(cart: list[dict], products: list[dict], product_id: int, size: Any, quantity: int = 1) -> tuple[bool, str]
```

**Назначение.** Добавляет товар нужного размера в корзину. Если такая позиция уже есть — увеличивает количество. Проверяет существование товара и размера и достаточность остатка с учётом уже лежащего в корзине.

**Параметры:**

- `cart` (`list[dict]`) — корзина (изменяется на месте).
- `products` (`list[dict]`) — каталог.
- `product_id` (`int`) — id товара.
- `size` (`int | str`) — размер: `40`, `"M"`, `"5 кг"`.
- `quantity` (`int`, по умолчанию `1`) — количество.

**Возвращает:** `tuple[bool, str]` — признак успеха и сообщение для пользователя.

**Пример:**

```python
from src.cart import add_to_cart
cart = []
print(add_to_cart(cart, products, 1, 40, 2))
print(add_to_cart(cart, products, 1, 40, 1))
print(add_to_cart(cart, products, 4, 'XL'))
```

Результат:

```text
(True, '«Кроссовки RunFast» (размер 40) добавлен в корзину')
(False, 'Недостаточно товара размера 40: есть 2 шт.')
(False, 'Размер XL отсутствует у товара «Футболка DryFit»')
```

**Исключения:** Не выбрасывает: ошибки возвращаются как `(False, сообщение)`.

### `remove_from_cart`

```python
remove_from_cart(cart: list[dict], product_id: int, size: Any) -> bool
```

**Назначение.** Удаляет позицию (товар + размер) из корзины.

**Параметры:**

- `cart` (`list[dict]`) — корзина.
- `product_id` (`int`) — id товара.
- `size` (`int | str`) — размер.

**Возвращает:** `bool` — `True`, если позиция была найдена и удалена.

**Пример:**

```python
from src.cart import add_to_cart, remove_from_cart
cart = []
add_to_cart(cart, products, 2, 5)
print(remove_from_cart(cart, 2, 5), cart)
print(remove_from_cart(cart, 2, 5))
```

Результат:

```text
True []
False
```

**Исключения:** Не выбрасывает.

### `update_quantity`

```python
update_quantity(cart: list[dict], products: list[dict], product_id: int, size: Any, new_qty: int) -> bool
```

**Назначение.** Меняет количество позиции в корзине. Значение `≤ 0` удаляет позицию (ошибка, найденная модульным тестом на занятии 8).

**Параметры:**

- `cart` (`list[dict]`) — корзина.
- `products` (`list[dict]`) — каталог.
- `product_id` (`int`) — id товара.
- `size` (`int | str`) — размер.
- `new_qty` (`int`) — новое количество.

**Возвращает:** `bool` — `False`, если позиции нет или на складе не хватает товара.

**Пример:**

```python
from src.cart import add_to_cart, update_quantity
cart = []
add_to_cart(cart, products, 8, 'M')
print(update_quantity(cart, products, 8, 'M', 4), cart[0]['quantity'])
print(update_quantity(cart, products, 8, 'M', 100))
print(update_quantity(cart, products, 8, 'M', 0), cart)
```

Результат:

```text
True 4
False
True []
```

**Исключения:** Не выбрасывает.

### `cart_total`

```python
cart_total(cart: list[dict]) -> int
```

**Назначение.** Итоговая сумма корзины: сумма «цена × количество» по всем позициям (исправлено в hotfix/cart-total на занятии 7).

**Параметры:**

- `cart` (`list[dict]`) — корзина.

**Возвращает:** `int` — сумма в рублях.

**Пример:**

```python
from src.cart import add_to_cart, cart_total
cart = []
add_to_cart(cart, products, 1, 40, 2)
add_to_cart(cart, products, 2, 5)
print(cart_total(cart))
```

Результат:

```text
20470
```

**Исключения:** Не выбрасывает.

### `total_sum`

```python
total_sum(items: list[dict]) -> int
```

**Назначение.** Сумма позиций с учётом количества. Функция появилась при разрешении конфликта слияния (занятие 7) и оставлена для совместимости; для корзины используйте `cart_total`.

**Параметры:**

- `items` (`list[dict]`) — позиции с полями `price` и `quantity`.

**Возвращает:** `int` — сумма.

**Пример:**

```python
from src.cart import total_sum
print(total_sum([{'price': 100, 'quantity': 3}, {'price': 50, 'quantity': 1}]))
```

Результат:

```text
350
```

**Исключения:** Не выбрасывает.

## Модуль `src.orders`

Модуль orders — оформление, вывод, сохранение и загрузка заказов.

### `create_order`

```python
create_order(cart: list[dict], client_name: str, products: list[dict], order_id: int | None = None) -> dict
```

**Назначение.** Оформляет заказ из корзины: проверяет остатки, списывает товар со склада, формирует заказ и очищает корзину. Проверка остатков выполняется до списания, поэтому при ошибке склад не меняется.

**Параметры:**

- `cart` (`list[dict]`) — корзина (очищается).
- `client_name` (`str`) — ФИО клиента.
- `products` (`list[dict]`) — каталог (остатки уменьшаются).
- `order_id` (`int | None`, по умолчанию `None`) — номер заказа; по умолчанию — следующий номер счётчика.

**Возвращает:** `dict` — заказ с полями `id`, `client`, `date`, `items`, `total`.

**Пример:**

```python
from src.cart import add_to_cart
from src.orders import create_order
cart = []
add_to_cart(cart, products, 2, 5, 2)
order = create_order(cart, 'Лаптев В.И.', products, order_id=7)
print(order['id'], order['client'], order['total'], cart, products[1]['sizes'][5])
```

Результат:

```text
7 Лаптев В.И. 4980 [] 10
```

**Исключения:** `ValueError` — корзина пуста, не указано имя клиента или товара на складе не хватает.

### `print_order`

```python
print_order(order: dict) -> str
```

**Назначение.** Печатает заказ в консоль в читаемом виде и возвращает тот же текст (удобно для тестов).

**Параметры:**

- `order` (`dict`) — заказ из `create_order`.

**Возвращает:** `str` — текст заказа.

**Пример:**

```python
from src.orders import print_order
order = {'id': 1, 'date': '2026-10-09 10:00', 'client': 'Лаптев В.И.',
         'items': [{'name': 'Мяч Pro Match', 'size': 5, 'price': 2490, 'quantity': 2}], 'total': 4980}
text = print_order(order)
```

Результат:

```text
Заказ №1 от 2026-10-09 10:00, клиент: Лаптев В.И.
  Мяч Pro Match (размер 5) × 2 = 4980 руб.
  Итого: 4980 руб.
```

**Исключения:** Не выбрасывает.

### `save_orders`

```python
save_orders(orders: list[dict], filename: str | Path = data/orders.json) -> Path
```

**Назначение.** Сохраняет список заказов в JSON-файл (UTF-8, с отступами). Папка создаётся при необходимости.

**Параметры:**

- `orders` (`list[dict]`) — заказы.
- `filename` (`str | Path`, по умолчанию `"data/orders.json"`) — путь к файлу.

**Возвращает:** `Path` — путь к записанному файлу.

**Пример:**

```python
from src.orders import save_orders
path = save_orders([{'id': 1, 'total': 4980}], TMP + '/orders.json')
print(path.name, path.exists())
```

Результат:

```text
orders.json True
```

**Исключения:** `OSError` — нет прав на запись.

### `load_orders`

```python
load_orders(filename: str | Path = data/orders.json) -> list[dict]
```

**Назначение.** Загружает заказы из JSON-файла.

**Параметры:**

- `filename` (`str | Path`, по умолчанию `"data/orders.json"`) — путь к файлу.

**Возвращает:** `list[dict]` — заказы; пустой список, если файла нет.

**Пример:**

```python
from src.orders import save_orders, load_orders
save_orders([{'id': 1, 'total': 4980}], TMP + '/orders.json')
print(load_orders(TMP + '/orders.json'))
print(load_orders(TMP + '/nothing.json'))
```

Результат:

```text
[{'id': 1, 'total': 4980}]
[]
```

**Исключения:** `json.JSONDecodeError` — файл повреждён.

### `next_order_id`

```python
next_order_id(orders: list[dict]) -> int
```

**Назначение.** Вычисляет номер следующего заказа по уже сохранённым заказам (нужно, чтобы номера не повторялись между запусками программы).

**Параметры:**

- `orders` (`list[dict]`) — загруженные заказы.

**Возвращает:** `int` — максимальный `id` + 1, либо 1.

**Пример:**

```python
from src.orders import next_order_id
print(next_order_id([]), next_order_id([{'id': 3}, {'id': 7}]))
```

Результат:

```text
1 8
```

**Исключения:** Не выбрасывает.

## Модуль `src.analytics`

Модуль analytics — аналитика продаж по оформленным заказам.

### `total_revenue`

```python
total_revenue(orders: list[dict]) -> int
```

**Назначение.** Общая выручка по всем заказам.

**Параметры:**

- `orders` (`list[dict]`) — заказы.

**Возвращает:** `int` — сумма полей `total`.

**Пример:**

```python
from src.analytics import total_revenue
print(total_revenue([{'total': 20470}, {'total': 7470}]))
```

Результат:

```text
27940
```

**Исключения:** Не выбрасывает.

### `best_selling_product`

```python
best_selling_product(orders: list[dict]) -> str | None
```

**Назначение.** Определяет самый продаваемый товар по количеству проданных единиц.

**Параметры:**

- `orders` (`list[dict]`) — заказы.

**Возвращает:** `str | None` — название товара или `None`, если заказов нет.

**Пример:**

```python
from src.analytics import best_selling_product
orders = [{'items': [{'name': 'Кроссовки RunFast', 'quantity': 2}]},
          {'items': [{'name': 'Мяч Pro Match', 'quantity': 3}]}]
print(best_selling_product(orders), best_selling_product([]))
```

Результат:

```text
Мяч Pro Match None
```

**Исключения:** Не выбрасывает.

### `average_order_total`

```python
average_order_total(orders: list[dict]) -> float
```

**Назначение.** Средний чек — средняя сумма заказа с округлением до копеек.

**Параметры:**

- `orders` (`list[dict]`) — заказы.

**Возвращает:** `float` — средний чек; `0` при отсутствии заказов.

**Пример:**

```python
from src.analytics import average_order_total
print(average_order_total([{'total': 20470}, {'total': 7470}]))
```

Результат:

```text
13970.0
```

**Исключения:** Не выбрасывает.

## Модуль `src.storage`

Модуль storage — чтение и запись данных магазина в JSON-файлы.

### `read_json`

```python
read_json(filename: str | Path, default: Any = None) -> Any
```

**Назначение.** Читает JSON-файл в кодировке UTF-8.

**Параметры:**

- `filename` (`str | Path`) — путь.
- `default` (`Any`, по умолчанию `None`) — значение, если файла нет.

**Возвращает:** Прочитанные данные или `default`.

**Пример:**

```python
from src.storage import read_json
print(read_json(TMP + '/none.json', default=[]))
```

Результат:

```text
[]
```

**Исключения:** `json.JSONDecodeError` — некорректный JSON.

### `write_json`

```python
write_json(data: Any, filename: str | Path) -> Path
```

**Назначение.** Записывает данные в JSON (UTF-8, `ensure_ascii=False`, отступ 2), создавая папки.

**Параметры:**

- `data` (`Any`) — сериализуемые данные.
- `filename` (`str | Path`) — путь.

**Возвращает:** `Path` — путь к файлу.

**Пример:**

```python
from src.storage import write_json
print(write_json({'ok': True}, TMP + '/a/b.json').read_text(encoding='utf-8'))
```

Результат:

```text
{
  "ok": true
}
```

**Исключения:** `TypeError` — данные не сериализуются в JSON.

### `load_products`

```python
load_products(filename: str | Path = data/products.json) -> list[dict]
```

**Назначение.** Загружает каталог из JSON и восстанавливает типы размеров: в JSON ключи всегда строки, числовые размеры (`"40"`) превращаются обратно в `int` (ошибка интеграции, найденная на занятии 9).

**Параметры:**

- `filename` (`str | Path`, по умолчанию `"data/products.json"`) — путь к каталогу.

**Возвращает:** `list[dict]` — товары; пустой список, если файла нет.

**Пример:**

```python
from src.storage import load_products
products = load_products('data/products.json')
print(len(products), products[0]['sizes'])
```

Результат:

```text
8 {40: 2, 41: 1, 42: 1, 43: 0}
```

**Исключения:** `json.JSONDecodeError` — файл повреждён.

### `save_products`

```python
save_products(products: list[dict], filename: str | Path = data/products.json) -> Path
```

**Назначение.** Сохраняет каталог (например, после списания остатков при оформлении заказа).

**Параметры:**

- `products` (`list[dict]`) — каталог.
- `filename` (`str | Path`, по умолчанию `"data/products.json"`) — путь.

**Возвращает:** `Path` — путь к файлу.

**Пример:**

```python
from src.storage import save_products, load_products
save_products(products, TMP + '/p.json')
print(load_products(TMP + '/p.json') == products)
```

Результат:

```text
True
```

**Исключения:** `OSError` — нет прав на запись.

### `load_cart`

```python
load_cart(filename: str | Path = data/cart.json) -> list[dict]
```

**Назначение.** Загружает сохранённую корзину (корзина хранится между запусками консольного приложения) и восстанавливает типы размеров.

**Параметры:**

- `filename` (`str | Path`, по умолчанию `"data/cart.json"`) — путь.

**Возвращает:** `list[dict]` — позиции корзины; пустой список, если файла нет.

**Пример:**

```python
from src.storage import save_cart, load_cart
save_cart([{'id': 1, 'name': 'Кроссовки RunFast', 'size': 40, 'price': 8990, 'quantity': 2}], TMP + '/cart.json')
print(load_cart(TMP + '/cart.json')[0]['size'] == 40)
```

Результат:

```text
True
```

**Исключения:** `json.JSONDecodeError` — файл повреждён.

### `save_cart`

```python
save_cart(cart: list[dict], filename: str | Path = data/cart.json) -> Path
```

**Назначение.** Сохраняет корзину в JSON.

**Параметры:**

- `cart` (`list[dict]`) — корзина.
- `filename` (`str | Path`, по умолчанию `"data/cart.json"`) — путь.

**Возвращает:** `Path` — путь к файлу.

**Пример:**

```python
from src.storage import save_cart
print(save_cart([], TMP + '/cart.json').read_text(encoding='utf-8'))
```

Результат:

```text
[]
```

**Исключения:** `OSError` — нет прав на запись.
