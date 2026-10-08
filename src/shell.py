from src.kernel import boot
from src.syscalls import (
    sys_echo, sys_get_users, sys_login, sys_whoami,
    sys_create_file, sys_list_files, sys_ps
)

BANNER = """
==============================
  StudyOS 0.2 — учебная ОС
  help — список команд
==============================
"""

HELP = """Команды:
  help          справка
  echo <текст>  ответ ядра (sys_echo)
  users         список пользователей (sys_get_users)
  whoami        текущий пользователь
  login         вход в систему
  create        создать файл
  ls            список файлов
  ps            список процессов
  exit          выход"""


def main():
    boot()
    current_user = "guest"
    print(BANNER)
    while True:
        cmd = input(f"{current_user}@studyos:~$ ").strip()
        if cmd == "exit":
            print("Завершение работы StudyOS.")
            break
        elif cmd == "help":
            print(HELP)
        elif cmd.startswith("echo"):
            print(sys_echo(cmd[4:].strip(), current_user))
        elif cmd == "users":
            for login, role in sys_get_users(current_user):
                print(f"{login} ({role})")
        elif cmd == "whoami":
            print(sys_whoami(current_user))
        elif cmd == "login":
            login = input("Логин: ")
            password = input("Пароль: ")
            if sys_login(login, password, current_user):
                current_user = login
                print(f"Вы вошли как {login}")
            else:
                print("Ошибка входа")
        elif cmd == "create":
            path = input("Путь: ")
            content = input("Содержимое: ")
            fid = sys_create_file(path, content, current_user)
            print(f"Создан файл с id={fid}")
        elif cmd == "ls":
            for f in sys_list_files("/", current_user):
                print(f)
        elif cmd == "ps":
            for p in sys_ps(current_user):
                print(p)
        elif cmd:
            print(f"Неизвестная команда: {cmd}")


if __name__ == "__main__":
    main()
