# 09. Разрешение конфликта слияния — total_sum

## Как возник конфликт

1. От ветки `develop` созданы две ветки: `feature/total-v1` и `feature/total-v2`.
2. В обеих ветках в одно и то же место `shop.py` (перед `main()`) добавлена функция `total_sum`:
   - v1: `return sum(p['price'] for p in products)` — сумма цен без учёта количества;
   - v2: `return sum(p['price'] * p['quantity'] for p in products)` — цена × количество.
3. `feature/total-v1` слита в `develop` без проблем (fast-forward).
4. При `git merge feature/total-v2` Git сообщил:
   `CONFLICT (content): Merge conflict in shop.py`, статус файла — `UU`.

## Маркеры конфликта

```
<<<<<<< HEAD
    return sum(p['price'] for p in products)
=======
    return sum(p['price'] * p['quantity'] for p in products)
>>>>>>> feature/total-v2
```

- между `<<<<<<< HEAD` и `=======` — версия из текущей ветки `develop` (v1);
- между `=======` и `>>>>>>>` — версия из сливаемой ветки `feature/total-v2`.

## Решение

Оставлена версия **v2** (с учётом количества), так как корзина хранит поле `quantity`
и сумма без него неверна (2 пары кроссовок по 8 990 ₽ давали бы 8 990 вместо 17 980).
Маркеры `<<<<<<<`, `=======`, `>>>>>>>` удалены, добавлена строка документации.

Проверка: `total_sum([{'price': 8990, 'quantity': 2}, {'price': 2490, 'quantity': 1}])` → **20470**.

## Завершение слияния

```
git add shop.py
git commit -m "Разрешён конфликт в total_sum"
git branch -d feature/total-v1 feature/total-v2
```

## Вывод

Конфликт возникает, когда две ветки меняют одни и те же строки. Git не выбирает
версию сам — разработчик анализирует обе, оставляет правильную (или объединяет их),
удаляет маркеры и фиксирует результат отдельным коммитом.
