# 19. Руководство разработчика

Документ для разработчика, который продолжит проект **СпортТовары** (SportShop): как настроить
окружение, запустить тесты, добавить новую функцию, оформить ветку и Pull Request и собрать проект.

## 1. Настройка окружения

### 1.1. Что нужно установить

| Инструмент | Версия | Зачем |
|---|---|---|
| Python | 3.10+ (проект проверен на 3.13) | язык проекта; `str \| None` в аннотациях требует 3.10 |
| Git | 2.30+ | контроль версий, Git Flow |
| VS Code + расширение Python (ms-python) | актуальная | редактор, отладчик (`.vscode/launch.json`) |

Внешних библиотек нет, поэтому `requirements.txt` не нужен — используется только стандартная
библиотека (`json`, `pathlib`, `argparse`, `unittest`, `subprocess`).

### 1.2. Получение кода

```bash
git clone https://github.com/reflektpro/SportShop.git
cd SportShop
git checkout develop             # разработка ведётся в develop, не в main
git config user.name  "Фамилия И.О."
git config user.email "почта@example.com"
```

### 1.3. Виртуальное окружение (рекомендуется)

```bash
python -m venv .venv
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # Linux / macOS
python --version                 # 3.10+
```

В VS Code: `Ctrl+Shift+P` → «Python: Select Interpreter» → `.venv`. Конфигурация отладчика уже
лежит в `.vscode/launch.json` («Python: Current File»): откройте файл, поставьте точку останова
(F9) и нажмите F5.

### 1.4. Архитектура

```
main.py (CLI, демонстрация)
   │
   ├── src/analytics.py   ← работает с заказами
   ├── src/orders.py      → src/cart.py, src/catalog.py, src/storage.py
   ├── src/cart.py        → src/catalog.py
   ├── src/catalog.py     (нижний уровень, без зависимостей)
   └── src/storage.py     (нижний уровень: JSON-файлы data/)
build.py → проверка Python и данных → unittest → main.py
```

Правила зависимостей: модули нижнего уровня (`catalog`, `storage`) ни от кого не зависят;
циклических импортов нет; импорты всегда абсолютные (`from src.catalog import find_product`),
запуск — из корня проекта. Диаграмма: [architecture.png](architecture.png).

## 2. Запуск тестов

Тесты лежат в `tests/`, фреймворк — `unittest`:

| Файл | Что проверяет | Тестов |
|---|---|---|
| `test_catalog.py` | поиск, остатки, статистика каталога | 12 |
| `test_cart.py` | добавление, удаление, изменение количества, сумма корзины | 12 |
| `test_orders.py` | оформление, печать, сохранение/загрузка заказов и товаров | 6 |
| `test_analytics.py` | выручка, хит продаж, средний чек | 6 |
| `test_integration.py` | полный цикл модулей на реальном `data/products.json` | 3 |
| `test_cli.py` | команды `main.py` и новые функции API версии 1.0 | 13 |

```bash
python -m unittest discover -s tests            # все тесты (52)
python -m unittest discover -s tests -v         # подробный вывод
python -m unittest tests.test_cart              # один файл
python -m unittest tests.test_cart.TestCart.test_cart_total   # один тест
```

Тестовые данные берутся из `tests/helpers.py` (функция `catalog()` возвращает свежую копию
каталога для каждого теста), поэтому тесты не зависят друг от друга. Тесты, которые пишут файлы,
используют `tempfile` и удаляют за собой временные файлы.

## 3. Как добавить новую функцию

Пример: добавить в каталог функцию `get_by_brand(products, brand)`.

1. **Задача.** Добавьте User Story в `docs/03_Product_Backlog.md` и карточку на Kanban-доске.
2. **Ветка.** `git checkout develop && git pull && git checkout -b feature/by-brand`.
3. **Модуль.** Определите модуль по ответственности: каталог → `src/catalog.py`. Функция должна
   быть с аннотациями типов и docstring:

   ```python
   def get_by_brand(products: list[dict], brand: str) -> list[dict]:
       """Товары указанного бренда (без учёта регистра)."""
       return [p for p in products if p["brand"].lower() == brand.lower()]
   ```

4. **Тест.** Добавьте класс в `tests/test_catalog.py`: обычный случай, граничный (пустой
   каталог) и ошибочный (несуществующий бренд → пустой список).
5. **Интеграция.** Если функция нужна пользователю — добавьте команду в `build_parser()` в
   `main.py` и тест в `tests/test_cli.py`.
6. **Документация.** Опишите функцию в `docs/17_API_Reference.md` по шаблону (назначение,
   параметры, возвращаемое значение, пример, исключения), команду — в `docs/18_User_Guide.md`.
7. **Проверка.** `python build.py` должен завершиться строкой `СБОРКА УСПЕШНА`.

Соглашения по коду: PEP 8, отступ 4 пробела, имена функций `snake_case`; функции каталога не
изменяют переданный список (возвращают новый); функции, которые меняют данные (`add_to_cart`,
`create_order`), документируют это в docstring; ошибки пользователя возвращаются как
`(False, сообщение)` или `ValueError` — функции не вызывают `exit()` и не печатают (кроме `print_order`).

## 4. Ветки и Pull Request (Git Flow)

| Ветка | Откуда | Куда сливается | Назначение |
|---|---|---|---|
| `main` | — | — | только релизы, каждый отмечен тегом `vX.Y` |
| `develop` | `main` | `main` (релиз) | интеграция готовых функций |
| `feature/<имя>` | `develop` | `develop` | одна функция / одна задача |
| `hotfix/<имя>` | `main` | `main` и `develop` | срочное исправление релиза |

Работа с feature-веткой:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/by-brand
# ... код, тесты ...
git add src/catalog.py tests/test_catalog.py
git commit -m "feat: get_by_brand — фильтр каталога по бренду"
git push -u origin feature/by-brand
```

Сообщения коммитов: `feat:` — новая функция, `fix:` — исправление, `docs:` — документация,
`test:` — тесты, `refactor:` — переработка без изменения поведения, `build:` — сборка.
Один коммит — одно логическое изменение.

**Pull Request.** На GitHub: *Compare & pull request*, base — `develop`, compare — ваша ветка.
Описание PR (шаблон из `docs/10_Pull_Request.md`):

```markdown
## PR: feature/by-brand → develop
**Что сделано:** …
**Как проверить:** команды и ожидаемый результат
**Связанные задачи:** US-…
**Чек-лист:** [ ] тесты проходят  [ ] документация обновлена  [ ] нет конфликтов с develop
```

Ревьюер проверяет код и запускает `python build.py`. После одобрения ветка вливается с
сохранением истории: `git checkout develop && git merge --no-ff feature/by-brand && git push`,
затем удаляется: `git branch -d feature/by-brand`. Конфликты слияния разрешаются вручную (порядок —
в `docs/09_Conflict_Resolution.md`).

## 5. Сборка

```bash
python build.py
```

Шаги сборки (`build.py`):

1. `[1/4]` версия Python ≥ 3.10;
2. `[2/4]` наличие всех файлов `src/`, `main.py` и корректность `data/products.json` (обязательные поля `id, name, brand, category, price, sizes`);
3. `[3/4]` все тесты (`unittest discover -s tests -v`);
4. `[4/4]` запуск `main.py` в демонстрационном режиме.

Если любой шаг не прошёл — печатается `СБОРКА ПРЕРВАНА` и возвращается код 1 (удобно для CI).
Успешная сборка — `СБОРКА УСПЕШНА`, код 0.

## 6. Выпуск релиза

```bash
git checkout develop && python build.py              # всё зелёное
# обновить CHANGELOG.md и версию VERSION в main.py
git checkout main
git merge --no-ff develop -m "release vX.Y"
git tag -a vX.Y -m "Релиз версии X.Y"
git push origin main
git push origin vX.Y
```

Проверить, что тег есть на сервере: `git ls-remote --tags origin` или страница
*Releases/Tags* на GitHub.
