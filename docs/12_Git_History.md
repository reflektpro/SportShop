# 12. История коммитов (git log --oneline --graph --all)

```
* 5b5788c docs: описание hotfix cart-total
*   3a26794 Merge hotfix/cart-total into develop
|\  
* \   3ee8032 Merge PR: feature/search-advanced → develop (US-2)
|\ \  
| * | f71adfe docs: описание Pull Request feature/search-advanced
| * | 9a382ba US-2: search_advanced — поиск по категории в запросе, проверка диапазона цен
|/ /  
* | 6c2355d docs: описание разрешения конфликта
* |   497ce46 Разрешён конфликт в total_sum
|\ \  
| * | 8e6588c total_sum: сумма с учётом количества (v2)
* | | 430c4af total_sum: сумма цен (v1)
|/ /  
* | 17f1fea US-1: добавлена функция get_low_stock (учёт остатков по размерам)
* | ca76e0f docs: схема ветвления Git Flow
| | * 83d01fe Merge hotfix/cart-total into main
| |/| 
|/|/  
| * 787f46a hotfix: cart_total учитывает количество товара
|/  
* 90d4fc8 US-5: остатки по размерам и корзина покупателя
* 88e44fc fix: корректный перевод строк в highlight_low_stock
* aa1dc84 fix: корректный перевод строк в highlight_low_stock
* 9b8cd08 fix: корректный перевод строк в highlight_low_stock
* 76b8cf7 docs: Product Backlog, Sprint Backlog, Kanban, Standup, Retrospective
* bc36b1b US-4: добавлены create_order и save_orders
* 743a407 US-3: добавлена функция count_by_category
* dea9761 US-2: добавлена функция search_advanced
* fccf780 US-6: добавлена функция highlight_low_stock
* 1535498 US-1: добавлена функция get_low_stock
* 4fa15e3 init: каркас проекта СпортТовары
```

## Анализ графа

**Сколько веток было создано?** В рамках занятия создано 6 веток:
`develop`, `feature/low-stock`, `feature/total-v1`, `feature/total-v2`,
`feature/search-advanced`, `hotfix/cart-total` (плюс существующая `main`).
Постоянными остаются `main` и `develop`, временные ветки удалены после слияния.

**Какие слияния произошли?**
1. `feature/low-stock` → `develop` — fast-forward (коммит 17f1fea встал на вершину develop).
2. `feature/total-v1` → `develop` — fast-forward (430c4af).
3. `feature/total-v2` → `develop` — слияние с конфликтом, коммит 497ce46.
4. `feature/search-advanced` → `develop` — слияние по PR через `--no-ff`, коммит 3ee8032.
5. `hotfix/cart-total` → `main` — коммит 83d01fe.
6. `hotfix/cart-total` → `develop` — коммит 3a26794.

**Был ли конфликт и как он разрешён?** Да: при слиянии `feature/total-v2`
в `develop` обе ветки изменили тело функции `total_sum`. Конфликт разрешён
вручную — оставлен вариант с учётом количества `p['price'] * p['quantity']`,
маркеры удалены, создан коммит «Разрешён конфликт в total_sum» (497ce46).
Подробно — в `docs/09_Conflict_Resolution.md`.
