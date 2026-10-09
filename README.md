# СпортТовары — система управления магазином

[![version](https://img.shields.io/badge/version-1.0-blue)](https://github.com/reflektpro/SportShop/releases/tag/v1.0)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![tests](https://img.shields.io/badge/tests-52%20passed-brightgreen)

## Описание

**СпортТовары** (SportShop) — консольное приложение для небольшого магазина спортивных товаров.
Оно хранит каталог с остатками по размерам, ищет товары, ведёт корзину покупателя, оформляет
заказы со списанием остатков со склада, сохраняет и загружает заказы в JSON и считает аналитику
продаж (выручка, средний чек, хит продаж).

Проект выполнен в рамках учебной практики (УП.02 «Осуществление интеграции программных модулей»)
и развивался от занятия к занятию: Scrum/Kanban (занятие 6) → Git Flow (7) → модульные тесты и
отладка (8) → разделение на модули, интеграция и сборка (9) → документация и релиз v1.0 (10).

## Требования

- Python **3.10+** (проверено на Python 3.13);
- внешних зависимостей нет — только стандартная библиотека;
- SQLite в SportShop **не используется**: данные хранятся в JSON-файлах папки `data/`
  (SQLite используется только в учебной ОС `my_os/`, занятия 1–2);
- Git — для получения кода и работы с ветками.

## Установка

```bash
git clone https://github.com/reflektpro/SportShop.git
cd SportShop
python --version          # должно быть 3.10 или новее
```

Чтобы получить ровно версию релиза: `git checkout v1.0`.

## Использование

```bash
python main.py                                   # демонстрация: каталог → корзина → заказ → аналитика
python main.py --help                            # список команд
python main.py catalog                           # весь каталог
python main.py search nike --max-price 9000      # поиск
python main.py low-stock                         # товары с низким остатком
python main.py cart add 1 40 2                   # положить в корзину: товар 1, размер 40, 2 шт.
python main.py cart show                         # корзина
python main.py checkout --client "Иванов И.И."   # оформить заказ
python main.py orders                            # загрузить и показать заказы
python main.py analytics                         # выручка, средний чек, хит продаж
```

Команды `cart` и `checkout` изменяют файлы в `data/`. Для экспериментов укажите копию данных:
`python main.py --data demo_data catalog`. Подробно — в [руководстве пользователя](docs/18_User_Guide.md).

## Структура проекта

```
SportShop/
├── src/
│   ├── __init__.py
│   ├── catalog.py      # каталог: поиск, остатки, статистика
│   ├── cart.py         # корзина покупателя
│   ├── orders.py       # оформление, вывод, сохранение и загрузка заказов
│   ├── analytics.py    # аналитика продаж
│   └── storage.py      # чтение/запись JSON (товары, заказы, корзина)
├── tests/              # 52 теста unittest: модульные, интеграционные, CLI
├── docs/               # документация 03–21 (см. ниже)
├── data/
│   └── products.json   # каталог товаров
├── my_os/              # StudyOS — учебная ОС (занятия 1–2)
├── main.py             # точка входа: демонстрация и консольные команды
├── build.py            # сборка: Python, данные, тесты, запуск
└── README.md
```

## Тестирование

```bash
python -m unittest discover -s tests        # все тесты
python -m unittest discover -s tests -v     # с именами тестов
python -m unittest tests.test_integration   # только интеграционные
```

## Сборка

```bash
python build.py
```

Скрипт проверяет версию Python (≥ 3.10), наличие файлов и корректность `data/products.json`,
запускает все тесты и приложение. При успехе печатает `СБОРКА УСПЕШНА` и возвращает код 0.

## Документация

| Файл | Содержание |
|---|---|
| [docs/17_API_Reference.md](docs/17_API_Reference.md) | справочник API: 26 публичных функций |
| [docs/18_User_Guide.md](docs/18_User_Guide.md) | руководство пользователя (сценарии с командами) |
| [docs/19_Developer_Guide.md](docs/19_Developer_Guide.md) | руководство разработчика (окружение, тесты, ветки, PR, сборка) |
| [docs/20_Final_Test_Report.md](docs/20_Final_Test_Report.md) | итоговый отчёт о тестировании |
| [docs/21_Presentation.md](docs/21_Presentation.md) | презентация проекта (7 слайдов) |
| [docs/architecture.png](docs/architecture.png) | диаграмма архитектуры |
| [CHANGELOG.md](CHANGELOG.md) | история версий |

## Практические работы

Состояние кода на конец каждой работы зафиксировано тегом `practice-N`.

| № | Тема | Где смотреть | Код на момент сдачи |
|---|---|---|---|
| 1 | Границы ОС и нефункциональные требования (StudyOS) | [my_os/docs/01_OS_Scope_and_NFR.md](my_os/docs/01_OS_Scope_and_NFR.md), [my_os/src](my_os/src) | [my_os/](my_os) |
| 2 | Архитектура и API ядра (StudyOS) | [my_os/docs/02_OS_Architecture.md](my_os/docs/02_OS_Architecture.md), [диаграмма компонентов](my_os/docs/02_component_diagram.png), [syscalls.py](my_os/src/syscalls.py) | [my_os/](my_os) |
| 6 | Agile/Scrum/Kanban: Backlog, Sprint, Kanban, Standup, Retro | [docs/03–07](docs) | [practice-6](https://github.com/reflektpro/SportShop/tree/practice-6) |
| 7 | Git Flow, конфликты, Pull Request, Hotfix | [docs/08–12](docs) | [practice-7](https://github.com/reflektpro/SportShop/tree/practice-7) |
| 8 | Отладка и модульное тестирование (unittest) | [docs/13_Debugging.md](docs/13_Debugging.md), [docs/14_Test_Report.md](docs/14_Test_Report.md) | [practice-8](https://github.com/reflektpro/SportShop/tree/practice-8) |
| 9 | Интеграция модулей и сборка | [src/](src), [tests/test_integration.py](tests/test_integration.py), [build.py](build.py), [docs/15](docs/15_Integration_Errors.md), [docs/16](docs/16_Integration_Report.md) | [practice-9](https://github.com/reflektpro/SportShop/tree/practice-9) |
| 10 | Документация приложения, итоговый проект, релиз v1.0 | README, [docs/17–21](docs), [CHANGELOG.md](CHANGELOG.md) | [practice-10](https://github.com/reflektpro/SportShop/tree/practice-10), релиз [v1.0](https://github.com/reflektpro/SportShop/releases/tag/v1.0) |

Ветки по Git Flow: `main` — релизы, `develop` — разработка, `feature/*`, `hotfix/*`.

## StudyOS (my_os)

```bash
cd my_os
python src/db.py         # создать базу
python -m src.shell      # оболочка: help, echo, users, whoami, login, create, ls, ps, exit
```

## Авторы

- **Лаптев Василий Иванович** (Лаптев В.И.), группа 3ИП7-24 — разработка, тестирование, документация.

Учебный проект, 2026.
