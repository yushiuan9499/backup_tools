// This program is use to check the file is change or not
// If the file is change, it will split the change chunk of file
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
using namespace std;

const int MAX_FILE_NAME = 256;
const int SZ_100MB = 100 * 1024 * 1024;

void check_n_split(char filename[]) {
  FILE *file = fopen(filename, "r");
  for (int i = 0; 1; i++) {
    char chunk_name[MAX_FILE_NAME] = {0};
    bool diff = false;
    sprintf(chunk_name, "__split_file__/%s.%09d", filename, i);
    FILE *chunk = fopen(chunk_name, "r");
    if (chunk == NULL) {
      // File not exist
      // Create new file
      diff = true;
    } else {
      // File exist
      // Check the content
      fseek(file, i * SZ_100MB, SEEK_SET);
      while (1) {
        unsigned char buffer1[8], buffer2[8];
        unsigned long *p1 = (unsigned long *)buffer1;
        unsigned long *p2 = (unsigned long *)buffer2;
        size_t read1 = fread(buffer1, 1, 8, file);
        size_t read2 = fread(buffer2, 1, 8, chunk);
        if (read1 != read2 || *p1 != *p2) {
          diff = true;
          break;
        } else if (read1 == 0) {
          break;
        }
      }
    }
    fclose(chunk);
    if (diff) {
      // File is different
      // Create new file
      chunk = fopen(chunk_name, "w");
      if (chunk == NULL) {
        printf("Cannot create file %s\n", chunk_name);
        return;
      }
      fseek(file, i * SZ_100MB, SEEK_SET);
      for (int j = 0; j < SZ_100MB; j += 8) {
        unsigned char buffer[8];
        size_t read = fread(buffer, 1, 8, file);
        if (read == 0) {
          break;
        }
        fwrite(buffer, 1, 8, chunk);
      }
      fclose(chunk);
    }
  }
  fclose(file);
  return;
}

int main() {
  if (sizeof(unsigned long) != 8) {
    printf("this program assumes unsigned long is 8 bytes\n");
    return -1;
  }
  ifstream ignore_file(".gitignore");
  string ignore_file_name;
  while (getline(ignore_file, ignore_file_name)) {
    if (ignore_file_name.size() > MAX_FILE_NAME) {
      printf("File name is too long\n");
      return -1;
    }
    check_n_split((char *)ignore_file_name.c_str());
  }
  return 0;
}
