import sys
import os
import hashlib
import shutil

# Шляхи до системних файлів VCS
VCS_DIR = "vcs"
COMMITS_DIR = os.path.join(VCS_DIR, "commits")
CONFIG_FILE = os.path.join(VCS_DIR, "config.txt")
INDEX_FILE = os.path.join(VCS_DIR, "index.txt")
LOG_FILE = os.path.join(VCS_DIR, "log.txt")

def init_vcs():
    """Створює необхідну структуру папок та файлів."""
    if not os.path.exists(VCS_DIR):
        os.makedirs(VCS_DIR)
    if not os.path.exists(COMMITS_DIR):
        os.makedirs(COMMITS_DIR)
    for file in [CONFIG_FILE, INDEX_FILE, LOG_FILE]:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                pass

def get_help():
    return (
        "These are VCS commands:\n"
        "config    Get and set a username.\n"
        "add       Add a file to the index.\n"
        "log       Show commit logs.\n"
        "commit    Save changes.\n"
        "checkout  Switch between commits and restore a previous file state."
    )

def handle_config(args):
    if not args:
        with open(CONFIG_FILE, 'r') as f:
            name = f.read().strip()
            print(f"The username is {name}." if name else "Please, tell me who you are.")
    else:
        name = args[0]
        with open(CONFIG_FILE, 'w') as f:
            f.write(name)
        print(f"The username is {name}.")

def handle_add(args):
    if not args:
        with open(INDEX_FILE, 'r') as f:
            lines = f.readlines()
            if not lines:
                print("Add a file to the index.")
            else:
                print("Tracked files:")
                for line in lines:
                    print(line.strip())
    else:
        filename = args[0]
        if os.path.exists(filename):
            with open(INDEX_FILE, 'r') as f:
                tracked = [line.strip() for line in f.readlines()]
            if filename not in tracked:
                with open(INDEX_FILE, 'a') as f:
                    f.write(filename + '\n')
            print(f"The file '{filename}' is tracked.")
        else:
            print(f"Can't find '{filename}'.")

def get_hash(files):
    """Створює хеш вмісту всіх відстежуваних файлів."""
    combined_content = b""
    for filename in sorted(files):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                combined_content += f.read()
    return hashlib.sha1(combined_content).hexdigest()

def handle_commit(args):
    if not args:
        print("Message was not passed.")
        return

    with open(CONFIG_FILE, 'r') as f:
        author = f.read().strip()

    with open(INDEX_FILE, 'r') as f:
        tracked_files = [line.strip() for line in f.readlines()]

    if not tracked_files:
        print("Nothing to commit.")
        return

    current_hash = get_hash(tracked_files)
    
    # Перевірка на зміни (порівняння з останнім записом у лозі)
    last_hash = None
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            if lines:
                last_hash = lines[0].split()[1] # Перший рядок логу: commit <hash>

    if current_hash == last_hash:
        print("Nothing to commit.")
        return

    # Створення папки коміту та копіювання файлів
    commit_path = os.path.join(COMMITS_DIR, current_hash)
    os.makedirs(commit_path, exist_ok=True)
    for file in tracked_files:
        shutil.copy(file, commit_path)

    # Запис у лог (в початок файлу)
    message = args[0]
    log_entry = f"commit {current_hash}\nAuthor: {author}\n{message}\n\n"
    with open(LOG_FILE, 'r') as f:
        old_content = f.read()
    with open(LOG_FILE, 'w') as f:
        f.write(log_entry + old_content)
    
    print("Changes are committed.")

def handle_log():
    with open(LOG_FILE, 'r') as f:
        content = f.read().strip()
        print(content if content else "No commits yet.")

def handle_checkout(args):
    if not args:
        print("Commit id was not passed.")
        return
    
    commit_id = args[0]
    commit_path = os.path.join(COMMITS_DIR, commit_id)
    
    if not os.path.exists(commit_path):
        print("Commit does not exist.")
        return

    # Відновлення файлів з папки коміту
    for filename in os.listdir(commit_path):
        shutil.copy(os.path.join(commit_path, filename), ".")
    
    print(f"Switched to commit {commit_id}.")

def main():
    init_vcs()
    args = sys.argv[1:]
    
    if not args or args[0] == "--help":
        print(get_help())
        return

    command = args[0]
    cmd_args = args[1:]
    
    commands = {
        "config": lambda: handle_config(cmd_args),
        "add": lambda: handle_add(cmd_args),
        "commit": lambda: handle_commit(cmd_args),
        "log": lambda: handle_log(),
        "checkout": lambda: handle_checkout(cmd_args)
    }

    if command in commands:
        commands[command]()
    else:
        # Виведення опису конкретної команди, якщо вона введена без параметрів
        # або повідомлення про помилку
        valid_commands = ["config", "add", "log", "commit", "checkout"]
        if command in valid_commands:
            # Для Етапу 1: якщо команда існує, вивести опис
            help_lines = get_help().split('\n')
            for line in help_lines:
                if line.startswith(command):
                    print(line.replace(command, "").strip())
                    return
        print(f"'{command}' is not a VCS command.")

if __name__ == "__main__":
    main()