import os
import datetime


def process_command(command, current_dir, vfs_path, username):
    parts = command.split()
    if not parts:
        return "", False
    cmd = parts[0]
    args = parts[1:]

    if cmd == "ls":
        try:
            dir_path = os.path.normpath(os.path.join(vfs_path, current_dir.strip("/\\")))
            files = os.listdir(dir_path)
            output = "\n".join(files)
            return output, False
        except FileNotFoundError:
            return "ls: current directory not found", False
        except PermissionError:
            return "ls: permission denied", False

    elif cmd == "cd":
        if len(args) != 1:
            return "Usage: cd <directory>", False
        new_dir = os.path.normpath(os.path.join(current_dir, args[0]))
        target_path = os.path.normpath(os.path.join(vfs_path, new_dir.strip("/\\")))
        if os.path.isdir(target_path):
            return new_dir, True
        else:
            return f"cd: {args[0]}: No such directory", False

    elif cmd == "exit":
        return "Exiting shell...", False

    elif cmd == "date":
        now = datetime.datetime.now()
        return now.strftime("%c"), False

    elif cmd == "touch":
        if len(args) != 1:
            return "Usage: touch <filename>", False
        file_path = os.path.normpath(os.path.join(vfs_path, current_dir.strip("/\\"), args[0]))
        try:
            with open(file_path, "a"):
                os.utime(file_path, None)
            return f"touched {args[0]}", False
        except OSError as e:
            return f"touch: {e}", False

    elif cmd == "rev":
        if len(args) != 1:
            return "Usage: rev <filename>", False
        file_path = os.path.normpath(os.path.join(vfs_path, current_dir.strip("/\\"), args[0]))
        if not os.path.exists(file_path):
            return f"rev: cannot open '{args[0]}': No such file", False
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            reversed_lines = [line.rstrip()[::-1] for line in lines]
            return "\n".join(reversed_lines), False
        except OSError as e:
            return f"rev: {e}", False

    else:
        return f"{cmd}: command not found", False
