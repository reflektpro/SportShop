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
