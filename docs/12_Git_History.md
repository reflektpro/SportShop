# 12. История коммитов (git log --oneline --graph --all)

```
* 75732a5 docs: описание hotfix cart-total
*   40b40f7 Merge hotfix/cart-total into develop
|\  
* \   44e8e26 Merge PR: feature/search-advanced → develop (US-2)
|\ \  
| * | 7440005 docs: описание Pull Request feature/search-advanced
| * | 00f6247 US-2: search_advanced — поиск по категории в запросе, проверка диапазона цен
|/ /  
* | 5cafbe2 docs: описание разрешения конфликта
* |   d0a8e86 Разрешён конфликт в total_sum
|\ \  
| * | 9a2d151 total_sum: сумма с учётом количества (v2)
* | | 2085b9a total_sum: сумма цен (v1)
|/ /  
* | b824e91 US-1: добавлена функция get_low_stock (учёт остатков по размерам)
* | 9fefb7b docs: схема ветвления Git Flow
| | * 52845ba Merge hotfix/cart-total into main
| |/| 
|/|/  
| * 3128ae4 hotfix: cart_total учитывает количество товара
|/  
* 5378a74 US-5: остатки по размерам и корзина покупателя
* 6e807b7 fix: корректный перевод строк в highlight_low_stock
* 00d813d fix: корректный перевод строк в highlight_low_stock
* b1b0398 fix: корректный перевод строк в highlight_low_stock
* edf8dc8 docs: Product Backlog, Sprint Backlog, Kanban, Standup, Retrospective
* ff3169d US-4: добавлены create_order и save_orders
* da484b2 US-3: добавлена функция count_by_category
* 4f97528 US-2: добавлена функция search_advanced
* 1bfc005 US-6: добавлена функция highlight_low_stock
* c0c218f US-1: добавлена функция get_low_stock
* 2a88488 init: каркас проекта СпортТовары
```

## Анализ графа

**Сколько веток было создано?** В рамках занятия создано 6 веток:
`develop`, `feature/low-stock`, `feature/total-v1`, `feature/total-v2`,
`feature/search-advanced`, `hotfix/cart-total` (плюс существующая `main`).
Постоянными остаются `main` и `develop`, временные ветки удалены после слияния.

**Какие слияния произошли?**
1. `feature/low-stock` → `develop` — fast-forward (коммит b824e91 встал на вершину develop).
2. `feature/total-v1` → `develop` — fast-forward (2085b9a).
3. `feature/total-v2` → `develop` — слияние с конфликтом, коммит d0a8e86.
4. `feature/search-advanced` → `develop` — слияние по PR через `--no-ff`, коммит 44e8e26.
5. `hotfix/cart-total` → `main` — коммит 52845ba.
6. `hotfix/cart-total` → `develop` — коммит 40b40f7.

**Был ли конфликт и как он разрешён?** Да: при слиянии `feature/total-v2`
в `develop` обе ветки изменили тело функции `total_sum`. Конфликт разрешён
вручную — оставлен вариант с учётом количества `p['price'] * p['quantity']`,
маркеры удалены, создан коммит «Разрешён конфликт в total_sum» (d0a8e86).
Подробно — в `docs/09_Conflict_Resolution.md`.
