#include <stdio.h>
#include <seccomp.h>

void __attribute__ ((constructor)) setup() {
  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_load(ctx);
}

int main() {
  puts("Welcome to the generic rop challenge");
  vuln();
}

int vuln() {
  char buf[64];
  puts("Enter your payload below");
  gets(buf);
}
