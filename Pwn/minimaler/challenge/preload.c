#include <stdio.h>
#include <seccomp.h>

__attribute__ ((constructor)) initialize() {
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_ALLOW);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(sigreturn), 0);
  seccomp_load(ctx);
}
