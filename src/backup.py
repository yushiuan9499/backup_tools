#!/bin/python3
import os
import sys
import time


def main():
    exclude = [".git", "__split_files__"]
    if len(sys.argv) != 2:
        print("Usage: backup.py <backup_dir>")
        return 1
    backup_dir = sys.argv[1]
    if not os.path.exists(backup_dir):
        print("Backup directory does not exist")
        return 1
    os.chdir(backup_dir)
    if not os.path.exists(".git"):
        os.system("git init")
        os.mkdir("__split_files__")
        os.system("touch .gitignore")
        repo_url = input("Enter the repository url: ")
        os.system(f"git remote add origin {repo_url}")
    old_ignore = set()
    with open(".gitignore", "r") as f:
        while True:
            file = f.readline().strip()
            if not file:
                break
            old_ignore.add(file)
            print(file)
    with open(".gitignore", "w") as f:
        for folder, subfolders, files in os.walk(".",topdown=True):
            if folder == ".":
                subfolders[:] = [d for d in subfolders if d not in exclude]
            for file in files:
                sz = os.path.getsize(os.path.join(folder, file))
                if sz > 1024 * 1024 * 100:
                    f.write(f"{os.path.join(folder, file)}\n")
                elif file in old_ignore:
                    os.system(f"rm -f {os.path.join(folder, '__split__files__', file)}.*")
    os.system("check_n_split")
    os.system("git add .")
    os.system(f"git commit -m '{time.ctime()}'")
    os.system("git push -u origin master")
    return 0

if __name__ == "__main__":
    main()

