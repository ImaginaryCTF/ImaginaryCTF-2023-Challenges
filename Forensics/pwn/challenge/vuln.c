#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>

char *mem[16];

void __attribute__ ((constructor)) setup() {
  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);
}

int main() {
  char c;
  int index;
  size_t bytes_read, size;
  puts("How much wood could a woodchuck chuck if a woodchuck could chuck wood?");
  while (1) {
    puts("(b)irth a woodchuck");
    puts("(k)ill a woodchuck");
    puts("(s)ee a woodchuck");
    puts("(m)utilate a woodchuck");
    scanf("%c%*c", &c);
    if (c=='b') {
      puts("idx:");
      scanf("%d%*c", &index);
      if ((index < 0) || (index >= 16)) {exit(0);}
      puts("size:");
      scanf("%d%*c", &size);
      mem[index] = malloc(size);
      puts("internal organs:");
      read(0, mem[index], size);
    }
    else if (c=='k') {
      puts("idx:");
      scanf("%d%*c", &index);
      if ((index < 0) || (index >= 16)) {exit(0);}
      free(mem[index]);
    }
    else if (c=='s') {
      puts("idx:");
      scanf("%d%*c", &index);
      if ((index < 0) || (index >= 16)) {exit(0);}
      puts(mem[index]);
    }
    else if (c=='m') {
      puts("idx:");
      scanf("%d%*c", &index);
      if ((index < 0) || (index >= 16)) {exit(0);}
      puts("internal organs:");
      read(0, mem[index], size);
    }
  }
}
