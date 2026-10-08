from src.db import get_connection


def log_syscall(name, args="", user="system", status="OK"):
    """Записывает системный вызов в таблицу syscalls_log."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO syscalls_log (syscall_name, args, user, status) VALUES (?, ?, ?, ?)",
        (name, args, user, status),
    )
    conn.commit()
    conn.close()


def sys_echo(message, current_user="guest"):
    """Возвращает переданное сообщение (проверка связи с ядром)."""
    log_syscall("sys_echo", message, current_user)
    return message


def sys_get_users(current_user="guest"):
    """Список пользователей из таблицы users: [(login, role), ...]."""
    conn = get_connection()
    rows = conn.execute("SELECT login, role FROM users ORDER BY id").fetchall()
    conn.close()
    log_syscall("sys_get_users", "", current_user)
    return rows


def sys_login(login, password, current_user="guest"):
    log_syscall("sys_login", login, current_user)
    return True


def sys_logout(current_user="guest"):
    log_syscall("sys_logout", "", current_user)
    return True


def sys_whoami(current_user="guest"):
    log_syscall("sys_whoami", "", current_user)
    return current_user


def sys_create_file(path, content, current_user="guest"):
    log_syscall("sys_create_file", path, current_user)
    return 1


def sys_read_file(path, current_user="guest"):
    log_syscall("sys_read_file", path, current_user)
    return ""


def sys_delete_file(path, current_user="guest"):
    log_syscall("sys_delete_file", path, current_user)
    return True


def sys_list_files(path, current_user="guest"):
    log_syscall("sys_list_files", path, current_user)
    return ["test.txt"]


def sys_exec(name, current_user="guest"):
    log_syscall("sys_exec", name, current_user)
    return 42


def sys_ps(current_user="guest"):
    log_syscall("sys_ps", "", current_user)
    return []


def sys_kill(pid, current_user="guest"):
    log_syscall("sys_kill", str(pid), current_user)
    return True


def sys_mem_alloc(size, current_user="guest"):
    log_syscall("sys_mem_alloc", str(size), current_user)
    return 4096


def sys_logs(limit, current_user="guest"):
    log_syscall("sys_logs", str(limit), current_user)
    return []


def sys_shutdown(current_user="guest"):
    log_syscall("sys_shutdown", "", current_user)
    return True


if __name__ == "__main__":
    from src.db import init_db
    init_db()
    print(sys_login("admin", "secret"))
    print(sys_whoami("admin"))
    print(sys_create_file("/test.txt", "hello", "admin"))
    print(sys_ps("admin"))
