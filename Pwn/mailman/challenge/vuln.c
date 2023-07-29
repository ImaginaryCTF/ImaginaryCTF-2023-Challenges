#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <seccomp.h>

char* mem[16];

unsigned long inidx() {
  unsigned long idx;
  printf("idx: ");
  scanf("%lu%*c", &idx);
  if (idx < 0 || idx >= 16) {
    _exit(-1);
  }
  return idx;
}

int main() {
  int choice;
  unsigned long idx;
  unsigned long size;

  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
  seccomp_load(ctx);

  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  puts("Welcome to the post office.");
  puts("Enter your choice below:");
  puts("1. Write a letter");
  puts("2. Send a letter");
  puts("3. Read a letter");

  while (1) {
    printf("> ");
    scanf("%d%*c", &choice);
    switch (choice) {
      case 1:
        idx = inidx();
        printf("letter size: ");
        scanf("%lu%*c", &size);
        mem[idx] = malloc(size);
        printf("content: ");
        fgets(mem[idx], size, stdin);
        break;
      case 2:
        idx = inidx();
        free(mem[idx]);
        break;
      case 3:
        idx = inidx();
        puts(mem[idx]);
        break;
      default:
        puts("Invalid choice!");
        _exit(0);
    }
  }
}
