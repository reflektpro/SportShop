# Практическая работа № 5. Основы Python в VS Code. Структуры данных «Чудо Обувь»
# Автор: Лаптев В.И., группа 3ИП7-24

# ===== Задание 1. Первая программа (шаг 6) =====
print("Приложение Чудо Обувь запущено")
print("Добро пожаловать!")

# ===== Задание 2. Переменные, print, for =====
# Шаг 8. Переменные разных типов
login = "admin"              # str
last_name = "Админов"        # str
price = 8990.0               # float
quantity = 5                 # int
in_stock = True              # bool

print("Логин:", login)
print("Фамилия:", last_name)
print("Цена:", price, "руб.")
print("Количество:", quantity)
print("В наличии:", in_stock)

# Шаг 9. Перебор списка циклом for
sizes = [36.0, 37.0, 38.0, 39.0]
print("\nДоступные размеры:")
for s in sizes:
    print("-", s)

# Шаг 10. for с range
print("\nНомера по порядку:")
for i in range(len(sizes)):
    print(i + 1, "—", sizes[i])

# Шаг 11. Условие if
if quantity <= 3:
    print("\nМало на складе")
else:
    print("\nДостаточно на складе")

# ===== Задание 3. Списки и словари =====
# Шаг 12. Пользователи системы
users = [
    {'login': 'admin',   'last_name': 'Админов',       'role': 'администратор'},
    {'login': 'manager', 'last_name': 'Менеджеров',    'role': 'менеджер'},
    {'login': 'user',    'last_name': 'Пользователев', 'role': 'авторизованный'},
]

print()
for u in users:
    print(f"Логин: {u['login']}, фамилия: {u['last_name']}, роль: {u['role']}")

# Шаг 13. Каталог товаров: sizes — словарь «размер: количество»
products = [
    {'id': 1, 'name': 'Air Max',   'price': 8990.0, 'sizes': {36.0: 5, 37.0: 2}},
    {'id': 2, 'name': 'Superstar', 'price': 7490.0, 'sizes': {37.0: 4, 38.0: 3}},
    {'id': 3, 'name': 'Runfalcon', 'price': 5590.0, 'sizes': {39.0: 2}},
]

print()
for p in products:
    total_qty = sum(p['sizes'].values())
    print(f"{p['name']} — {p['price']} руб., всего на складе: {total_qty} шт.")

# ===== Задание 4. Функции =====
# Шаг 14. Поиск пользователя по логину
def find_user(login):
    for u in users:
        if u['login'] == login:
            return u
    return None


result = find_user('admin')
if result:
    print(f"\nНайден пользователь: {result['last_name']}")
else:
    print("\nПользователь не найден")


# Шаг 15. Общая сумма
def total_sum(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total


cart = [
    {'name': 'Air Max',   'price': 8990.0, 'quantity': 2},
    {'name': 'Superstar', 'price': 7490.0, 'quantity': 1},
]

print(f"Итоговая сумма заказа: {total_sum(cart)} руб.")

# ===== Задание 5. Сортировка и фильтрация =====
# Шаг 16. Сортировка по цене
sorted_by_price = sorted(products, key=lambda p: p['price'])
print("\nТовары по возрастанию цены:")
for p in sorted_by_price:
    print(f"{p['name']} — {p['price']} руб.")

# Шаг 17. Товары с низким остатком (≤ 3 шт.)
low_stock = [p for p in products if sum(p['sizes'].values()) <= 3]
print("\nТовары с низким остатком (≤ 3 шт.):")
for p in low_stock:
    print(p['name'])


# ===== Задание 6. Поиск по каталогу =====
# Шаг 18. Поиск по названию
def search_products(query):
    query = query.lower()
    return [p for p in products if query in p['name'].lower()]


found = search_products('max')
print("\nРезультаты поиска 'max':")
for p in found:
    print(p['name'])


# Шаг 19. Фильтр по цене
def filter_by_price(products, min_price, max_price):
    return [p for p in products if min_price <= p['price'] <= max_price]


result = filter_by_price(products, 5000, 8000)
print("\nТовары от 5000 до 8000 руб.:")
for p in result:
    print(f"{p['name']} — {p['price']} руб.")


# ===== Задание 7. Мини-задача «Корзина» (шаг 20) =====
def add_to_cart(cart, product, size, quantity):
    cart.append({
        'product': product['name'],
        'price': product['price'],
        'size': size,
        'quantity': quantity
    })


def remove_from_cart(cart, name):
    cart[:] = [item for item in cart if item['product'] != name]


def change_quantity(cart, name, new_qty):
    for item in cart:
        if item['product'] == name:
            item['quantity'] = new_qty
            break


cart = []
add_to_cart(cart, products[0], 36.0, 2)
add_to_cart(cart, products[1], 37.0, 1)

print("\nКорзина:")
for item in cart:
    print(f"{item['product']}, размер {item['size']}, "
          f"{item['quantity']} шт. × {item['price']} = "
          f"{item['quantity'] * item['price']} руб.")

print(f"\nИтого: {total_sum(cart)} руб.")

change_quantity(cart, 'Air Max', 3)
remove_from_cart(cart, 'Superstar')

print("\nПосле изменений:")
for item in cart:
    print(f"{item['product']}, размер {item['size']}, {item['quantity']} шт.")
print(f"Итого: {total_sum(cart)} руб.")
