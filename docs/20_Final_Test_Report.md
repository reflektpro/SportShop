# 20. Итоговый отчёт о тестировании

**Проект:** СпортТовары — система управления магазином (SportShop)  
**Версия:** 1.0 (ветка `feature/final-docs` → `develop` → `main`, тег `v1.0`)  
**Дата:** 09.10.2026  
**Тестировщик:** Лаптев В.И., группа 3ИП7-24  
**Окружение:** Linux, Python 3.13.5, unittest (стандартная библиотека)

## 1. Цель

Перед выпуском версии 1.0 убедиться, что все автоматические тесты проходят, проект собирается
скриптом `build.py`, а основные пользовательские сценарии (каталог, поиск, корзина, заказ,
аналитика, сохранение и загрузка заказов) работают в собранном приложении.

## 2. Шаг 12–13. Автоматические тесты

Команда: `python -m unittest discover -s tests`

```text
$ python --version
Python 3.13.5
$ python -m unittest discover -s tests
....................................................
----------------------------------------------------------------------
Ran 52 tests in 0.055s

OK
```

| Файл | Тестов | Пройдено | Провалено | Ошибок |
|---|---|---|---|---|
| `tests/test_analytics.py` | 6 | 6 | 0 | 0 |
| `tests/test_cart.py` | 12 | 12 | 0 | 0 |
| `tests/test_catalog.py` | 12 | 12 | 0 | 0 |
| `tests/test_cli.py` | 13 | 13 | 0 | 0 |
| `tests/test_integration.py` | 3 | 3 | 0 | 0 |
| `tests/test_orders.py` | 6 | 6 | 0 | 0 |
| **Итого** | **52** | **52** | **0** | **0** |

Динамика числа тестов по занятиям: 8-е — 21 (модульные), 9-е — 39 (+ интеграционные и тесты
хранилища), 10-е — 52 (+ 13 тестов консольного интерфейса и новых функций API).

Подробный вывод (`-v`):

```text
$ python -m unittest discover -s tests -v
test_average_order_total (test_analytics.TestAnalytics.test_average_order_total) ... ok
test_average_order_total_empty (test_analytics.TestAnalytics.test_average_order_total_empty) ... ok
test_best_selling_empty (test_analytics.TestAnalytics.test_best_selling_empty) ... ok
test_best_selling_product (test_analytics.TestAnalytics.test_best_selling_product) ... ok
test_total_revenue (test_analytics.TestAnalytics.test_total_revenue) ... ok
test_total_revenue_empty (test_analytics.TestAnalytics.test_total_revenue_empty) ... ok
test_add_again_increases_quantity (test_cart.TestCart.test_add_again_increases_quantity) ... ok
test_add_more_than_stock (test_cart.TestCart.test_add_more_than_stock) ... ok
test_add_success (test_cart.TestCart.test_add_success) ... ok
test_cart_total (test_cart.TestCart.test_cart_total) ... ok
test_invalid_size (test_cart.TestCart.test_invalid_size) ... ok
test_remove_from_cart (test_cart.TestCart.test_remove_from_cart) ... ok
test_unknown_product (test_cart.TestCart.test_unknown_product) ... ok
test_update_quantity (test_cart.TestCart.test_update_quantity) ... ok
test_update_quantity_over_stock (test_cart.TestCart.test_update_quantity_over_stock) ... ok
test_update_quantity_zero_removes_item (test_cart.TestCart.test_update_quantity_zero_removes_item) ... ok
test_cart_with_items (test_cart.TestTotalSum.test_cart_with_items) ... ok
test_empty_cart (test_cart.TestTotalSum.test_empty_cart) ... ok
test_empty_list (test_catalog.TestGetLowStock.test_empty_list) ... ok
test_no_low_stock (test_catalog.TestGetLowStock.test_no_low_stock) ... ok
test_one_low_stock (test_catalog.TestGetLowStock.test_one_low_stock) ... ok
test_sorted_by_stock (test_catalog.TestGetLowStock.test_sorted_by_stock) ... ok
test_by_category (test_catalog.TestSearchAdvanced.test_by_category) ... ok
test_by_name (test_catalog.TestSearchAdvanced.test_by_name) ... ok
test_by_price (test_catalog.TestSearchAdvanced.test_by_price) ... ok
test_combined_filters (test_catalog.TestSearchAdvanced.test_combined_filters) ... ok
test_invalid_price_range (test_catalog.TestSearchAdvanced.test_invalid_price_range) ... ok
test_avg_price (test_catalog.TestStatistics.test_avg_price) ... ok
test_avg_price_empty (test_catalog.TestStatistics.test_avg_price_empty) ... ok
test_count_by_category (test_catalog.TestStatistics.test_count_by_category) ... ok
test_analytics_after_orders (test_cli.TestCli.test_analytics_after_orders) ... ok
test_cart_add_unknown_size_fails (test_cli.TestCli.test_cart_add_unknown_size_fails) ... ok
test_cart_is_saved_between_runs (test_cli.TestCli.test_cart_is_saved_between_runs) ... ok
test_catalog_lists_all_products (test_cli.TestCli.test_catalog_lists_all_products) ... ok
test_checkout_empty_cart_fails (test_cli.TestCli.test_checkout_empty_cart_fails) ... ok
test_checkout_saves_order_and_stock (test_cli.TestCli.test_checkout_saves_order_and_stock) ... ok
test_order_numbers_continue_after_restart (test_cli.TestCli.test_order_numbers_continue_after_restart) ... ok
test_orders_export (test_cli.TestCli.test_orders_export) ... ok
test_search_with_price_filter (test_cli.TestCli.test_search_with_price_filter) ... ok
test_search_wrong_price_range_is_error (test_cli.TestCli.test_search_wrong_price_range_is_error) ... ok
test_cart_roundtrip_keeps_size_types (test_cli.TestNewApi.test_cart_roundtrip_keeps_size_types) ... ok
test_create_order_requires_client (test_cli.TestNewApi.test_create_order_requires_client) ... ok
test_next_order_id (test_cli.TestNewApi.test_next_order_id) ... ok
test_analytics_on_saved_orders (test_integration.TestIntegration.test_analytics_on_saved_orders)
analytics корректно считает заказы, прочитанные из файла. ... ok
test_full_cycle (test_integration.TestIntegration.test_full_cycle)
Каталог → корзина → заказ → сохранение → загрузка. ... ok
test_order_updates_stock_for_catalog (test_integration.TestIntegration.test_order_updates_stock_for_catalog)
После заказа catalog видит уменьшившийся остаток. ... ok
test_empty_cart_raises (test_orders.TestCreateOrder.test_empty_cart_raises) ... ok
test_order_decreases_stock_and_clears_cart (test_orders.TestCreateOrder.test_order_decreases_stock_and_clears_cart) ... ok
test_print_order (test_orders.TestCreateOrder.test_print_order) ... ok
test_load_orders_missing_file (test_orders.TestStorage.test_load_orders_missing_file) ... ok
test_products_sizes_keep_type (test_orders.TestStorage.test_products_sizes_keep_type) ... ok
test_save_and_load_orders (test_orders.TestStorage.test_save_and_load_orders) ... ok

----------------------------------------------------------------------
Ran 52 tests in 0.056s

OK
```

Дополнительно проверена учебная ОС StudyOS (занятия 1–2), которая хранится в этом же репозитории:

```text
$ cd my_os && python -m unittest discover -s tests -v
test_echo_logged (test_prototype.TestPrototype.test_echo_logged) ... ok
test_four_tables (test_prototype.TestPrototype.test_four_tables) ... ok
test_get_users (test_prototype.TestPrototype.test_get_users) ... ok
test_kernel_survives_error (test_prototype.TestPrototype.test_kernel_survives_error) ... ok
test_password_is_hashed (test_prototype.TestPrototype.test_password_is_hashed) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.030s

OK
```

## 3. Шаг 14. Сборка

Команда: `python build.py`

```text
$ python build.py
=== Сборка SportShop ===
[1/4] Python 3.13.5 (нужен ≥ 3.10): OK
[2/4] Данные: 8 товаров, все файлы на месте: OK
[3/4] Запуск тестов...
test_average_order_total (test_analytics.TestAnalytics.test_average_order_total) ... ok
test_average_order_total_empty (test_analytics.TestAnalytics.test_average_order_total_empty) ... ok
test_best_selling_empty (test_analytics.TestAnalytics.test_best_selling_empty) ... ok
test_best_selling_product (test_analytics.TestAnalytics.test_best_selling_product) ... ok
test_total_revenue (test_analytics.TestAnalytics.test_total_revenue) ... ok
test_total_revenue_empty (test_analytics.TestAnalytics.test_total_revenue_empty) ... ok
test_add_again_increases_quantity (test_cart.TestCart.test_add_again_increases_quantity) ... ok
test_add_more_than_stock (test_cart.TestCart.test_add_more_than_stock) ... ok
test_add_success (test_cart.TestCart.test_add_success) ... ok
test_cart_total (test_cart.TestCart.test_cart_total) ... ok
test_invalid_size (test_cart.TestCart.test_invalid_size) ... ok
test_remove_from_cart (test_cart.TestCart.test_remove_from_cart) ... ok
test_unknown_product (test_cart.TestCart.test_unknown_product) ... ok
test_update_quantity (test_cart.TestCart.test_update_quantity) ... ok
test_update_quantity_over_stock (test_cart.TestCart.test_update_quantity_over_stock) ... ok
test_update_quantity_zero_removes_item (test_cart.TestCart.test_update_quantity_zero_removes_item) ... ok
test_cart_with_items (test_cart.TestTotalSum.test_cart_with_items) ... ok
test_empty_cart (test_cart.TestTotalSum.test_empty_cart) ... ok
test_empty_list (test_catalog.TestGetLowStock.test_empty_list) ... ok
test_no_low_stock (test_catalog.TestGetLowStock.test_no_low_stock) ... ok
test_one_low_stock (test_catalog.TestGetLowStock.test_one_low_stock) ... ok
test_sorted_by_stock (test_catalog.TestGetLowStock.test_sorted_by_stock) ... ok
test_by_category (test_catalog.TestSearchAdvanced.test_by_category) ... ok
test_by_name (test_catalog.TestSearchAdvanced.test_by_name) ... ok
test_by_price (test_catalog.TestSearchAdvanced.test_by_price) ... ok
test_combined_filters (test_catalog.TestSearchAdvanced.test_combined_filters) ... ok
test_invalid_price_range (test_catalog.TestSearchAdvanced.test_invalid_price_range) ... ok
test_avg_price (test_catalog.TestStatistics.test_avg_price) ... ok
test_avg_price_empty (test_catalog.TestStatistics.test_avg_price_empty) ... ok
test_count_by_category (test_catalog.TestStatistics.test_count_by_category) ... ok
test_analytics_after_orders (test_cli.TestCli.test_analytics_after_orders) ... ok
test_cart_add_unknown_size_fails (test_cli.TestCli.test_cart_add_unknown_size_fails) ... ok
test_cart_is_saved_between_runs (test_cli.TestCli.test_cart_is_saved_between_runs) ... ok
test_catalog_lists_all_products (test_cli.TestCli.test_catalog_lists_all_products) ... ok
test_checkout_empty_cart_fails (test_cli.TestCli.test_checkout_empty_cart_fails) ... ok
test_checkout_saves_order_and_stock (test_cli.TestCli.test_checkout_saves_order_and_stock) ... ok
test_order_numbers_continue_after_restart (test_cli.TestCli.test_order_numbers_continue_after_restart) ... ok
test_orders_export (test_cli.TestCli.test_orders_export) ... ok
test_search_with_price_filter (test_cli.TestCli.test_search_with_price_filter) ... ok
test_search_wrong_price_range_is_error (test_cli.TestCli.test_search_wrong_price_range_is_error) ... ok
test_cart_roundtrip_keeps_size_types (test_cli.TestNewApi.test_cart_roundtrip_keeps_size_types) ... ok
test_create_order_requires_client (test_cli.TestNewApi.test_create_order_requires_client) ... ok
test_next_order_id (test_cli.TestNewApi.test_next_order_id) ... ok
test_analytics_on_saved_orders (test_integration.TestIntegration.test_analytics_on_saved_orders)
analytics корректно считает заказы, прочитанные из файла. ... ok
test_full_cycle (test_integration.TestIntegration.test_full_cycle)
Каталог → корзина → заказ → сохранение → загрузка. ... ok
test_order_updates_stock_for_catalog (test_integration.TestIntegration.test_order_updates_stock_for_catalog)
После заказа catalog видит уменьшившийся остаток. ... ok
test_empty_cart_raises (test_orders.TestCreateOrder.test_empty_cart_raises) ... ok
test_order_decreases_stock_and_clears_cart (test_orders.TestCreateOrder.test_order_decreases_stock_and_clears_cart) ... ok
test_print_order (test_orders.TestCreateOrder.test_print_order) ... ok
test_load_orders_missing_file (test_orders.TestStorage.test_load_orders_missing_file) ... ok
test_products_sizes_keep_type (test_orders.TestStorage.test_products_sizes_keep_type) ... ok
test_save_and_load_orders (test_orders.TestStorage.test_save_and_load_orders) ... ok

----------------------------------------------------------------------
Ran 52 tests in 0.050s

OK
[3/4] Тесты: OK
[4/4] Запуск приложения...
=== СпортТовары ===
Загружено товаров: 8, средняя цена: 4627.5 руб.
Товары с остатком ≤ 3:
  [5] Ракетка Power (Wilson) — 0 шт.
  [3] Гантели 5 кг (Torneo) — 1 шт.
  [4] Футболка DryFit (Nike) — 3 шт.
  [7] Коврик YogaPro (Torneo) — 3 шт.
Поиск «nike»: ['Кроссовки RunFast', 'Футболка DryFit']
Остатки по категориям: {'Обувь': 12, 'Мячи': 12, 'Тренажёры': 1, 'Одежда': 18, 'Ракетки': 0, 'Йога': 3}
[+] «Кроссовки RunFast» (размер 40) добавлен в корзину
[+] «Мяч Pro Match» (размер 5) добавлен в корзину
[+] «Шорты Training» (размер M) добавлен в корзину
Сумма корзины: 27940 руб.
Заказ №1 от 2026-10-09 09:39, клиент: Лаптев В.И.
  Кроссовки RunFast (размер 40) × 2 = 17980 руб.
  Мяч Pro Match (размер 5) × 1 = 2490 руб.
  Шорты Training (размер M) × 3 = 7470 руб.
  Итого: 27940 руб.
Заказов в data/orders.json: 1
Выручка: 27940 руб., средний чек: 27940.0 руб., хит продаж: Шорты Training
[4/4] Приложение: OK
СБОРКА УСПЕШНА
```

Результат: все четыре шага сборки — **OK**, итог — **СБОРКА УСПЕШНА**, код возврата 0.

## 4. Шаг 15. Проверка основных сценариев в приложении

Сценарии выполнены вручную на копии данных (`--data demo_data`), чтобы не менять основной склад.
Полный вывод каждого сценария приведён в [руководстве пользователя](18_User_Guide.md).

| № | Сценарий | Команда | Ожидаемый результат | Фактический результат | Статус |
|---|---|---|---|---|---|
| 1 | Просмотр каталога | `catalog` | 8 товаров, средняя цена 4627.5 | 8 товаров, 4627.5 руб. | ✅ |
| 2 | Поиск по строке | `search nike` | Кроссовки RunFast, Футболка DryFit | 2 товара, совпадает | ✅ |
| 3 | Поиск с фильтрами | `search --category Обувь --max-price 10000` | только Кроссовки RunFast | 1 товар, совпадает | ✅ |
| 4 | Неверный диапазон цен | `search --min-price 5000 --max-price 100` | сообщение об ошибке, код 1 | `[!] Ошибка: min_price не может быть больше max_price` | ✅ |
| 5 | Низкий остаток | `low-stock` | 4 товара, первым — Ракетка Power (0 шт.) | совпадает | ✅ |
| 6 | Добавление в корзину | `cart add 1 40 2` | позиция 17980 руб. | 17980 руб. | ✅ |
| 7 | Несуществующий размер | `cart add 4 XL` | отказ, корзина не меняется | `[!] Размер XL отсутствует…` | ✅ |
| 8 | Больше, чем на складе | `cart add 1 40 5` | отказ | `[!] Недостаточно товара размера 40: есть 2 шт.` | ✅ |
| 9 | Изменение количества | `cart set 8 M 1` | итог 20470 руб. | 20470 руб. | ✅ |
| 10 | Оформление заказа | `checkout --client "Лаптев В.И."` | заказ №1, склад уменьшен, корзина пуста | совпадает, остаток размера 40 = 0 | ✅ |
| 11 | Заказ с пустой корзиной | `checkout --client …` | отказ, код 1 | `[!] Заказ не оформлен: Корзина пуста` | ✅ |
| 12 | Нумерация заказов | второй `checkout` | заказ №2 | №2 | ✅ |
| 13 | Сохранение/загрузка | `orders --export …`, `orders --file …` | 2 заказа в обоих файлах | совпадает | ✅ |
| 14 | Аналитика | `analytics` | выручка 27940, средний чек 13970, хит — Мяч Pro Match | совпадает | ✅ |
| 15 | Демонстрация | `python main.py` | полный цикл без ошибок | см. вывод сборки | ✅ |

Контрольный прогон на чистой копии данных:

```text
$ python main.py --version
СпортТовары 1.0
$ python main.py --data demo_data search adidas
 ID  Название             Бренд    Категория     Цена  Остаток  Размеры
  2  Мяч Pro Match        Adidas   Мячи          2490       12  5: 12
  6  Бутсы Predator       Adidas   Обувь        10990        8  40: 2, 41: 3, 42: 3
Найдено: 2
$ python main.py --data demo_data cart add 6 42 2
[+] «Бутсы Predator» (размер 42) добавлен в корзину
Корзина:
  [6] Бутсы Predator (размер 42) × 2 = 21980 руб.
  Итого: 21980 руб.
$ python main.py --data demo_data checkout --client "Сидоров С.С."
Заказ №1 от 2026-10-09 09:39, клиент: Сидоров С.С.
  Бутсы Predator (размер 42) × 2 = 21980 руб.
  Итого: 21980 руб.
Заказ сохранён в orders.json, остатки на складе обновлены.
$ python main.py --data demo_data analytics
Заказов: 1
Выручка: 21980 руб.
Средний чек: 21980.0 руб.
Хит продаж: Бутсы Predator
```

## 5. Дефекты, найденные при подготовке релиза

| № | Дефект | Как найден | Исправление | Тест |
|---|---|---|---|---|
| 1 | Номера заказов начинались с 1 при каждом запуске программы — в `orders.json` появлялись два заказа №1 | при проектировании консольного режима: каждый запуск — новый процесс, и счётчик `_next_id` в `src/orders.py` сбрасывается | `create_order(..., order_id=None)` и `next_order_id(orders)` | `test_order_numbers_continue_after_restart`, `test_next_order_id` |
| 2 | Заказ можно было оформить с пустым именем клиента | ревью кода `create_order` при написании API Reference | `ValueError("Не указано имя клиента")` | `test_create_order_requires_client` |
| 3 | После сохранения корзины в JSON размер `40` превращался в строку `"40"` и не находился на складе (та же проблема, что в занятии 9 для каталога) | при разработке команды `cart` | `load_cart` приводит размеры к исходным типам | `test_cart_roundtrip_keeps_size_types`, `test_cart_is_saved_between_runs` |

Открытых дефектов нет.

## 6. Готовность к сдаче (чек-лист)

- [x] Все 52 автоматических теста проходят (`OK`).
- [x] `python build.py` → `СБОРКА УСПЕШНА`.
- [x] 15 ручных сценариев выполнены, фактический результат совпадает с ожидаемым.
- [x] Документация: README.md, 17_API_Reference, 18_User_Guide, 19_Developer_Guide, 20_Final_Test_Report, 21_Presentation.
- [x] Ветки слиты по Git Flow, рабочее дерево чистое, изменения отправлены на GitHub.
- [x] Создан тег `v1.0`, он есть в удалённом репозитории.

**Вывод:** версия 1.0 готова к выпуску.
