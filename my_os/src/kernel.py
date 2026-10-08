"""Ядро StudyOS: загрузка, журнал ядра, безопасное выполнение системных вызовов."""
import hashlib
import logging
import time

from src import config
from src.db import init_db

config.LOG_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("studyos.kernel")
if not logger.handlers:
    handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def hash_password(password: str) -> str:
    """SHA-256 хэш пароля (пароли в открытом виде не хранятся — NFR-S1)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def boot() -> None:
    """Загрузка ядра: инициализация базы данных и журнала."""
    init_db()
    logger.info("%s %s: ядро загружено", config.OS_NAME, config.OS_VERSION)


def execute(name: str, func, *args):
    """Выполняет системный вызов: перехватывает ошибки и замеряет время (NFR-R1, NFR-P1).

    Возвращает (status, result): status — "OK" или "ERROR: <текст>".
    """
    start = time.perf_counter()
    try:
        result = func(*args)
        status = "OK"
    except Exception as e:  # ядро не должно падать из-за ошибки вызова
        result, status = None, f"ERROR: {e}"
        logger.error("%s%s -> %s", name, args, e)
    ms = (time.perf_counter() - start) * 1000
    if ms > config.MAX_SYSCALL_MS:
        logger.warning("%s выполнялся %.1f мс (> %d мс)", name, ms, config.MAX_SYSCALL_MS)
    return status, result


if __name__ == "__main__":
    boot()
    print(execute("sys_div", lambda a, b: a / b, 1, 0))
    print("Журнал ядра:", config.LOG_FILE)
