#!/bin/python3
import os
import sys
import time


def main():
    backup_dir = sys.argv[1]
    if not os.path.exists(backup_dir):
        print("Backup directory does not exist")
        return 1
    os.chdir(backup_dir)
    if not os.path.exists(".git"):
        os.system("git init")
        os.mkdir("__split_files__")
        repo_url = input("Enter the repository url: ")
    with open(".gitignore", "w") as f:
        for folder, subfolders, files in os.walk("."):
            for file in files:
                sz = os.path.getsize(os.path.join(folder, file))
                if sz > 1024 * 1024 * 100:
                    f.write(f"{os.path.join(folder, file)}\n")
                else:
                    os.system(f"rm {os.path.join(folder, "__split__files__", file)}.*")
    os.system("./bin/check_n_split")
    os.system("git add .")
    os.system(f"git commit -m '{time.ctime()}'")
    os.system("git push -u origin master")
    return 0

if __name__ == "__main__":
    main()

