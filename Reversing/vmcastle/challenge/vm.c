#include <stdio.h>
#include <stdlib.h>

struct program_state {
  int stack[1024];
  int ip;
  int sp;
  unsigned short *program;
  int registers[4];
} state;

void popr(unsigned char reg) {
  state.registers[reg%4] = state.stack[state.sp--];
  state.sp %= 1024;
}

void pushr(unsigned char reg) {
  state.stack[++state.sp] = state.registers[reg%4];
  state.sp %= 1024;
}

void pushi(char imm) {
  state.stack[++state.sp] = imm;
}

void add(char arg) {
  state.registers[3] = state.registers[0] + state.registers[1];
}

void shs(unsigned char arg) {
  state.stack[state.sp] <<= arg%2;
}

void ads(unsigned char arg) {
  state.stack[state.sp] += arg%2;
}

void sub(char arg) {
  state.registers[3] = state.registers[0] - state.registers[1];
}

void mul(char arg) {
  state.registers[3] = state.registers[0] * state.registers[1];
}

void idiv(char arg) {
  state.registers[3] = state.registers[0] / state.registers[1];
}

void mod(char arg) {
  state.registers[3] = state.registers[0] % state.registers[1];
}

void jmp(unsigned char reg) {
  state.ip += state.registers[reg%4];
}

void jmpc(char arg) {
  if (state.registers[3] == 0)
    state.ip += state.registers[1];
  else if (state.registers[3] < 0)
    state.ip += state.registers[0];
  else if (state.registers[3] > 0)
    state.ip += state.registers[2];
}

void cmp(char arg) {
  if (state.registers[0] == state.registers[1])
    state.registers[3] = 0;
  else if (state.registers[0] < state.registers[1])
    state.registers[3] = -1;
  else if (state.registers[0] > state.registers[1])
    state.registers[3] = 1;
}

void pr(unsigned char reg) {
  printf("%c", state.registers[reg%4]);
}

void in(unsigned char reg) {
    state.registers[reg%4] = (int) getchar();
}

void ex(char reg) {
  exit(0);
}

void nop(char arg) {

}

void (*table[256])(char) = {nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,nop,popr,pushr,pushi,add,sub,mul,idiv,mod,jmp,jmpc,cmp,pr,in,shs,ads,ex};

int main(int argc, char* argv[]) {
  FILE *f;
  char instr;
  char arg;

  char aaa[256];
///  memset(aaa, 0, 256);

  state.program = malloc(0x1000000);

  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  if (!argv[1]) { printf("Usage: %s [PROGRAM_FILE]\n", argv[0]); exit(-1); }
  if (strcmp(argv[1], "-") == 0) {
    fgets(state.program, 0x1000000, stdin);
  }
  else {
    f = fopen(argv[1], "r");
    fread(state.program, 0x1000000, 1, f);
  }

  while (1) {
    arg = (char) (state.program[state.ip]>>8);
    instr = (char) (state.program[state.ip] % 256);
//    printf("%d: %d %d\n", state.ip, instr, arg);
    table[(unsigned char)instr](arg);
    state.ip++;
  }
}
