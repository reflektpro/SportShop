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
