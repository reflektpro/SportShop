# Kanban-доска — Спринт 1 («СпортТовары»)

**WIP-лимит:** в колонке *In Progress* одновременно не более **2** задач.

Правило перемещения: Backlog → To Do → In Progress → Review → Done.

---

## Доска (итог занятия)

| Backlog | To Do | In Progress | Review | Done |
|---------|-------|-------------|--------|------|
| US-5 Журнал действий | | | | US-1 `get_low_stock` |
| US-7 Импорт CSV | | | | US-6 `highlight_low_stock` |
| US-8 Экспорт отчёта | | | | US-2 `search_advanced` |
| US-9 Промокоды | | | | US-3 `count_by_category` |
| US-10 История заказов | | | | US-4 `create_order` + `save_orders` |

---

## История перемещений

1. Старт: все задачи спринта в **To Do**.
2. Взяты в работу (In Progress, соблюдая WIP ≤ 2): US-1, затем US-6.
3. После самопроверки и коммита — **Review** → **Done**.
4. Аналогично: US-2 и US-3 (параллельно, WIP = 2) → Done.
5. US-4 (create_order + save_orders) → Done.
6. Не вошедшие в спринт истории остаются в **Backlog**.

---

## WIP

| Колонка | Лимит | Сейчас |
|---------|-------|--------|
| In Progress | 2 | 0 |
| Review | — | 0 |
| Done | — | 5 (задачи спринта) |
