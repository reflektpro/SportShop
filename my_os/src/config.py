"""Настройки StudyOS: пути и лимиты из нефункциональных требований (docs/01)."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "os.sqlite"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "kernel.log"

OS_NAME = "StudyOS"
OS_VERSION = "0.2"

MAX_SYSCALL_MS = 50        # NFR-P1: время обработки системного вызова
MAX_PROCESSES = 10         # NFR-P2: одновременных процессов
MAX_MEMORY_KB = 64 * 1024  # NFR-R2: лимит памяти учебной ОС (64 МБ)
PAGE_SIZE = 4096           # размер страницы памяти, байт

DEFAULT_ADMIN = ("admin", "admin")  # логин и пароль администратора (хранится только хэш)
