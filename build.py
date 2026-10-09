"""Скрипт сборки SportShop: проверка окружения, данных, запуск тестов и приложения."""
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
MIN_PYTHON = (3, 10)
REQUIRED_FILES = ["data/products.json", "main.py", "src/__init__.py", "src/catalog.py",
                  "src/cart.py", "src/orders.py", "src/analytics.py", "src/storage.py"]


def check_python_version() -> bool:
    """Шаг 1. Версия Python не ниже MIN_PYTHON."""
    ok = sys.version_info[:2] >= MIN_PYTHON
    print(f"[1/4] Python {sys.version.split()[0]} (нужен ≥ {MIN_PYTHON[0]}.{MIN_PYTHON[1]}): "
          + ("OK" if ok else "ОШИБКА"))
    return ok


def check_data() -> bool:
    """Шаг 2. Все файлы проекта на месте, products.json читается и содержит нужные поля."""
    missing = [f for f in REQUIRED_FILES if not (BASE / f).exists()]
    if missing:
        print(f"[2/4] Не найдены файлы: {', '.join(missing)} — ОШИБКА")
        return False
    try:
        products = json.loads((BASE / "data/products.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[2/4] products.json повреждён: {e} — ОШИБКА")
        return False
    keys = {"id", "name", "brand", "category", "price", "sizes"}
    bad = [p.get("id") for p in products if not keys <= p.keys()]
    if bad:
        print(f"[2/4] У товаров {bad} не хватает полей — ОШИБКА")
        return False
    print(f"[2/4] Данные: {len(products)} товаров, все файлы на месте: OK")
    return True


def run_tests() -> bool:
    """Шаг 3. Модульные и интеграционные тесты (unittest discover)."""
    print("[3/4] Запуск тестов...")
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                            cwd=BASE)
    ok = result.returncode == 0
    print("[3/4] Тесты: " + ("OK" if ok else "ОШИБКА"))
    return ok


def run_app() -> bool:
    """Шаг 4. Запуск приложения main.py."""
    print("[4/4] Запуск приложения...")
    result = subprocess.run([sys.executable, "main.py"], cwd=BASE)
    ok = result.returncode == 0
    print("[4/4] Приложение: " + ("OK" if ok else "ОШИБКА"))
    return ok


def main() -> int:
    print("=== Сборка SportShop ===")
    for step in (check_python_version, check_data, run_tests, run_app):
        if not step():
            print("СБОРКА ПРЕРВАНА")
            return 1
    print("СБОРКА УСПЕШНА")
    return 0


if __name__ == "__main__":
    sys.exit(main())
