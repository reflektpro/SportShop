# 11. Hotfix — hotfix/cart-total

## Проблема

В стабильной ветке `main` обнаружена критическая ошибка: функция `cart_total`
возвращала неверную сумму корзины — складывались только цены, без учёта количества.

Воспроизведение:
```
c = []; add_to_cart(c, PRODUCTS, 6, 41, 2)   # 2 пары бутс Predator по 10 990 ₽
cart_total(c)  →  10990   # ожидалось 21980
```

## Порядок действий

1. `git checkout main` — hotfix всегда создаётся от стабильной ветки.
2. `git checkout -b hotfix/cart-total`.
3. Исправление в `shop.py`:
   ```diff
   -    return sum(item["price"] for item in cart)
   +    return sum(item["price"] * item["quantity"] for item in cart)
   ```
4. Проверка: `cart_total(c)` → **21980** ✅
5. `git commit -m "hotfix: cart_total учитывает количество товара"`.
6. Слияние в `main`: `git merge --no-ff hotfix/cart-total` — исправление сразу попадает в рабочую версию.
7. Слияние в `develop`: `git merge --no-ff hotfix/cart-total` — чтобы ошибка не вернулась при следующем релизе.
8. Удаление ветки: `git branch -d hotfix/cart-total`.

## Почему именно hotfix

Ошибка находилась в `main` (у «пользователей»), ждать следующего релиза из `develop` нельзя.
Hotfix-ветка позволяет исправить только одну проблему, не затягивая в `main`
незавершённые функции из `develop`.
