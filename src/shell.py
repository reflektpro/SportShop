from src.syscalls import sys_whoami


def main():
    current_user = "guest"
    print("StudyOS 0.1. Введите help для списка команд.")
    while True:
        cmd = input(f"{current_user}@studyos:~$ ").strip()
        if cmd == "exit":
            break
        elif cmd == "help":
            print("Команды: help, whoami, exit")
        elif cmd == "whoami":
            print(sys_whoami(current_user))
        elif cmd:
            print(f"Неизвестная команда: {cmd}")


if __name__ == "__main__":
    main()
