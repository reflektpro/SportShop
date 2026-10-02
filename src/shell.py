from src.syscalls import (
    sys_login, sys_logout, sys_whoami,
    sys_create_file, sys_list_files, sys_ps, sys_logs
)


def main():
    current_user = "guest"
    print("StudyOS 0.2. Введите help для списка команд.")
    while True:
        cmd = input(f"{current_user}@studyos:~$ ").strip()
        if cmd == "exit":
            break
        elif cmd == "help":
            print("Команды: help, whoami, login, create, ls, ps, exit")
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
