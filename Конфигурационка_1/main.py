import argparse
import tarfile
import os
import sys
import tempfile
from commands import process_command

current_dir = "/"

def extract_vfs(archive_path, extract_path):
    """Извлечение виртуальной файловой системы из tar-архива."""
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    with tarfile.open(archive_path, "r") as tar:
        tar.extractall(path=extract_path)

def execute_command(username, hostname, vfs_path):
    """Основной цикл выполнения команд."""
    global current_dir
    while True:
        try:
            command = input(f"{username}@{hostname}:{current_dir}$ ")
            result, change_dir = process_command(command, current_dir, vfs_path, username)
            if not change_dir:
                print(f"{result}")
            else:
                current_dir = result
        except KeyboardInterrupt:
            print("\nExiting shell...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Основная функция программы."""
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--username", required=True, help="User name for prompt")
    parser.add_argument("--hostname", required=True, help="Host name for prompt")
    parser.add_argument("--vfs", required=True, help="Path to virtual filesystem archive")
    args = parser.parse_args()

    # Создаем временную директорию для виртуальной файловой системы
    with tempfile.TemporaryDirectory() as temp_dir:
        vfs_path = os.path.join(temp_dir, "vfs")
        extract_vfs(args.vfs, vfs_path)
        execute_command(args.username, args.hostname, vfs_path)

if __name__ == "__main__":
    main()
