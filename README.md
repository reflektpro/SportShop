# Практические работы — Лаптев Василий, группа 3ИП7-24

Репозиторий со всеми практическими работами. Состояние кода на конец каждой
работы зафиксировано тегом `practice-N` — по ссылке «код на момент сдачи».

| № | Тема | Где смотреть | Код на момент сдачи |
|---|---|---|---|
| 1 | Границы ОС и нефункциональные требования (StudyOS) | [my_os/docs/01_OS_Scope_and_NFR.md](my_os/docs/01_OS_Scope_and_NFR.md), [my_os/src](my_os/src) | [my_os/](my_os) |
| 2 | Архитектура и API ядра (StudyOS) | [my_os/docs/02_OS_Architecture.md](my_os/docs/02_OS_Architecture.md), [диаграмма компонентов](my_os/docs/02_component_diagram.png), [syscalls.py](my_os/src/syscalls.py) | [my_os/](my_os) |
| 6 | Agile/Scrum/Kanban: Backlog, Sprint, Kanban, Standup, Retro | [docs/03–07](docs) | [practice-6](https://github.com/reflektpro/SportShop/tree/practice-6) |
| 7 | Git Flow, конфликты, Pull Request, Hotfix | [docs/08–12](docs) | [practice-7](https://github.com/reflektpro/SportShop/tree/practice-7) |
| 8 | Отладка и модульное тестирование (unittest) | [docs/13_Debugging.md](docs/13_Debugging.md), [docs/14_Test_Report.md](docs/14_Test_Report.md) | [practice-8](https://github.com/reflektpro/SportShop/tree/practice-8) |
| 9 | Интеграция модулей и сборка | [src/](src), [tests/test_integration.py](tests/test_integration.py), [build.py](build.py), [docs/15](docs/15_Integration_Errors.md), [docs/16](docs/16_Integration_Report.md) | [practice-9](https://github.com/reflektpro/SportShop/tree/practice-9) |

## Структура

```
├── my_os/          StudyOS — учебная ОС (работы 1–2), см. my_os/README.md
├── src/            SportShop — модули магазина: catalog, cart, orders, analytics, storage
├── tests/          модульные и интеграционные тесты SportShop
├── data/           products.json
├── docs/           документация работ 6–9 (03–16)
├── main.py         точка входа SportShop
└── build.py        сборка SportShop
```

## SportShop («СпортТовары»)

Консольный магазин спортивных товаров (Python 3.8+, без внешних зависимостей).

```bash
python main.py                              # приложение
python -m unittest discover -s tests -v     # тесты (39)
python build.py                             # сборка: Python, данные, тесты, запуск
```

Ветки по Git Flow: `main` — релизы, `develop` — разработка, `feature/*`, `hotfix/*`.

## StudyOS (my_os)

```bash
cd my_os
python src/db.py         # создать базу
python -m src.shell      # оболочка: help, echo, users, whoami, login, create, ls, ps, exit
```
