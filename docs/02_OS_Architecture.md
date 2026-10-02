# Архитектура StudyOS

## 1. Модули

- shell.py – командная оболочка, читает команды пользователя
- syscalls.py – системные вызовы, интерфейс между оболочкой и ядром
- kernel.py – ядро, обрабатывает вызовы и координирует подсистемы
- scheduler.py – планировщик, управляет процессами
- memory.py – управление памятью
- fs.py – файловая система, работает с файлами
- auth.py – аутентификация и права доступа
- db.py – работа с SQLite

## 2. Системные вызовы

- `sys_login(login: str, password: str) -> bool`
- `sys_logout() -> bool`
- `sys_whoami() -> str`
- `sys_create_file(path: str, content: str) -> int`
- `sys_read_file(path: str) -> str`
- `sys_delete_file(path: str) -> bool`
- `sys_list_files(path: str) -> list`
- `sys_exec(name: str) -> int`
- `sys_ps() -> list`
- `sys_kill(pid: int) -> bool`
- `sys_mem_alloc(size: int) -> int`
- `sys_logs(limit: int) -> list`
- `sys_shutdown() -> bool`

### Контракты

**sys_login**
- Предварительное условие: пользователь с таким логином есть в базе.
- Постусловие: возвращено True или False.
- Побочный эффект: запись в журнал syscalls_log.

**sys_create_file**
- Предварительное условие: пользователь авторизован.
- Постусловие: файл создан, возвращён его id.
- Побочный эффект: запись в syscalls_log.

**sys_kill**
- Предварительное условие: процесс с указанным pid существует и принадлежит пользователю (или пользователь – admin).
- Постусловие: процесс завершён, возвращено True; если процесса нет – False.
- Побочный эффект: состояние процесса меняется на terminated, запись в syscalls_log.

## 3. Структуры данных

```python
process = {
    "pid": 1,
    "name": "shell",
    "state": "running",
    "owner": "admin",
    "memory": 120,
    "created_at": "2025-01-01 10:00:00",
}

file = {
    "id": 1,
    "path": "/home/test.txt",
    "content": "hello",
    "owner": "admin",
    "created_at": "2025-01-01 10:00:00",
}

user = {
    "id": 1,
    "login": "admin",
    "password_hash": "abc123...",
    "role": "admin",
}

log = {
    "id": 1,
    "syscall_name": "sys_login",
    "args": "admin",
    "user": "admin",
    "status": "OK",
    "timestamp": "2025-01-01 10:00:00",
}
```
