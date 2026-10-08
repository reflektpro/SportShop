# SportShop («СпортТовары»)

Учебный консольный магазин спортивных товаров (Python 3.8+, без внешних зависимостей).

## Структура

```
SportShop/
├── src/            модули: catalog, cart, orders, analytics, storage
├── tests/          модульные тесты + test_integration.py
├── data/           products.json (каталог), orders.json создаётся при запуске
├── docs/           документация практических работ (03–16)
├── main.py         точка входа
└── build.py        сборка: проверка Python и данных, тесты, запуск
```

## Запуск

```bash
python main.py                              # приложение
python -m unittest discover -s tests -v     # все тесты
python build.py                             # полная сборка
```
