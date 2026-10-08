# my_os — StudyOS

Учебная операционная система на Python 3.10+ и SQLite (практические занятия 1–2).

```
my_os/
├── docs/   01_OS_Scope_and_NFR.md, 02_OS_Architecture.md, 02_component_diagram.png/.drawio
├── src/    kernel.py, syscalls.py, shell.py, db.py, config.py
├── db/     os.sqlite (создаётся при запуске)
├── tests/  test_prototype.py
└── logs/   kernel.log (журнал ядра)
```

## Запуск (из папки my_os)

```bash
python src/db.py                         # создать базу db/os.sqlite
python -m src.syscalls                   # самопроверка системных вызовов
python -m src.shell                      # командная оболочка
python -m unittest discover -s tests -v  # тесты
```

Команды оболочки: `help, echo, users, whoami, login, create, ls, ps, exit`.
Вход администратора: `admin` / `admin`.
