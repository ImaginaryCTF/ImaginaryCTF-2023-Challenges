#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <seccomp.h>
#include <sys/types.h>
#include <string.h>

void (*code)();
unsigned char used[256];
unsigned char header[] = "H1\xffH1\xf6H1\xc0H1\xdbH1\xc9H1\xd2M1\xc0M1\xc9M1\xd2M1\xdbM1\xe4M1\xedM1\xf6M1\xffH1\xed";

void __attribute__ ((constructor)) setup() {
  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);
}

int main() {
  int count = 0;
  code = mmap(0, 0x1000, 3, MAP_SHARED | MAP_ANONYMOUS , 0, 0);

  memcpy(code, header, sizeof(header));

  puts("[*] Enter your shellcode below:");

  unsigned long size = read(0, ((char*)code)+sizeof(header)-1, 0x1000);

  if (size > 0x49) {
    puts("[*] Shellcode is too long!");
    _exit(0);
  }

  ((unsigned char*)code+sizeof(header)-1)[size-1] = '\x01';
  for (int i=0; i<size; i++) {
    used[(((unsigned char*)code)+sizeof(header)-1)[i]] = 1;
    if ((((unsigned char*)code)+sizeof(header)-1)[i] % 2 != 1) {
      puts("[*] Shellcode is too ordinary!");
      _exit(0);
    }
  }
  (((char*)code)+sizeof(header)-1)[size-1] = '\xcc';

  for (int i = 0; i<256; i++) {
    if (used[i] == 1) {
      count++;
    }
  }

  if (count > 20) {
    puts("[*] Shellcode is too complex!");
    _exit(0);
  }

  puts("[*] Protecting system...");

  mprotect(code, 0x1000, 5);
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
  seccomp_load(ctx);

  puts("[*] Executing code...");

  code();
}
