#include <stdio.h>

int main() {
  char *flag = malloc(0x20);
  char *buf = malloc(0x20);
  FILE *fptr;

  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  fptr = fopen("flag.txt", "r");
  fgets(flag, 0x20, fptr);
  fgets(buf, 0x20, stdin);
  flag = &buf;

  if (strlen(flag) <= 23) printf(buf);
  _exit(0);
}
