#!/bin/python3
# A simple script to backup files to a git repository
# Usage: backup.py <backup_dir> [--no-push]
import os
import sys
import time

class Args:
    def __init__(self):
        self.backup_dir:str = None
        self.no_push:bool = False

def read_args():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: backup.py <backup_dir> [--no-push]")
        return None
    args = Args()
    for arg in sys.argv[1:]:
        if arg == "--no-push":
            args.no_push = True
        else:
            if args.backup_dir:
                print("Backup directory already specified")
                return None
            args.backup_dir = arg
    if not args.backup_dir:
        print("Backup directory not specified")
        return None
    return args

def main():
    exclude = [".git", "__split_files__"]
    args = read_args()
    if not args:
        return 1
    if not os.path.exists(args.backup_dir):
        print("Backup directory does not exist")
        return 1
    os.chdir(args.backup_dir)
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
            if not os.path.exists(file):
                os.system(f"rm -f {os.path.join('__split_files__', file)}.*")
            else:
                sz = os.stat(file).st_size
                i = sz // (1024 * 1024 * 100) + 1
                while True:
                    if not os.path.exists(f"{os.path.join('__split_files__', file)}.%09d" % i):
                        break
                    os.system(f"rm -f {os.path.join('__split_files__', file)}.%09d" % i)

    with open(".gitignore", "w") as f:
        for folder, subfolders, files in os.walk(".",topdown=True):
            if folder == ".":
                subfolders[:] = [d for d in subfolders if d not in exclude]
            for file in files:
                sz = os.path.getsize(os.path.join(folder, file))
                if sz > 1024 * 1024 * 100:
                    f.write(f"{os.path.join(folder, file)[2:]}\n")
    os.system("check_n_split")
    os.system("git add .")
    os.system(f"git commit -m '{time.ctime()}'")
    if not args.no_push:
        os.system("git push -u origin master")
    return 0

if __name__ == "__main__":
    main()

