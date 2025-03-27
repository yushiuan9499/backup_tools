#!/bin/python3
import os
import sys


def main():
    exclude = [".git", "__split_files__"]
    backup_dir = sys.argv[1]
    if not os.path.exists(backup_dir):
        print("Backup directory does not exist")
        return 1
    os.chdir(backup_dir)
    for folder, subfolders, files in os.walk(".",topdown=True):
        if folder == ".":
            subfolders[:] = [d for d in subfolders if d not in exclude]
        for file in files:
            sz = os.path.getsize(os.path.join(folder, file))
            print(f"{os.path.join(folder, file)}: {sz}")
    return 0

if __name__ == "__main__":
    main()

