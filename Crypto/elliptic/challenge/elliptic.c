#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <openssl/sha.h>
#include <openssl/crypto.h>

#define ECC_CURVE secp128r1
#include "ecc.h"

struct signature {
  uint8_t r[NUM_ECC_DIGITS];
  uint8_t s[NUM_ECC_DIGITS];
  uint8_t hash[NUM_ECC_DIGITS+0x30]; // padding
  char msg[64];
};

struct signature *used[128];
EccPoint publicKey;
uint8_t privateKey[NUM_ECC_DIGITS];
uint8_t p_random[NUM_ECC_DIGITS];
struct signature *sigs[128];
int idx = 0;
int ox = 0;

void refreshNonce() {
  int fd = open("/dev/urandom", O_RDONLY);
  if (fd < 0) {
    perror("urandom");
    _exit(-1);
  }
  read(fd,(uint64_t*) p_random,sizeof(p_random));
  close(fd);
}

void signMessage() {
  refreshNonce();

  sigs[idx] = malloc(sizeof(struct signature));
  memset(sigs[idx], 0, sizeof(struct signature));

  puts("Enter the message to sign:");
  read(0, sigs[idx]->msg, sizeof(sigs[idx]->msg));
  SHA1(sigs[idx]->msg, sizeof(sigs[idx]->msg), sigs[idx]->hash);
  ecdsa_sign(sigs[idx]->r, sigs[idx]->s, privateKey, p_random, sigs[idx]->hash);

  printf("r = ");
  for (int i = 0; i < sizeof(sigs[idx]->r); i++) {
    printf("%02X", (unsigned char)sigs[idx]->r[i]);
  }
  printf("\n");
  printf("s = ");
  for (int i = 0; i < sizeof(sigs[idx]->s); i++) {
    printf("%02X", (unsigned char)sigs[idx]->s[i]);
  }
  printf("\n");

  idx++;
  idx %= 128;
}

void editMessage() {
  uint8_t r[NUM_ECC_DIGITS];
  uint8_t s[NUM_ECC_DIGITS];
  char tmp[1024];
  uint8_t hash[NUM_ECC_DIGITS+0x100]; // padding
  char msg[64];

  int ix = -1;

  refreshNonce();

  memset(r, 0, sizeof(r));
  memset(s, 0, sizeof(s));
  memset(tmp, 0, sizeof(tmp));
  memset(hash, 0, sizeof(hash));
  memset(msg, 0, sizeof(msg));

  puts("Enter the signature of the message you wish to edit:");
  printf("r = ");
  read(0, tmp, 1024);
  OPENSSL_hexstr2buf_ex(r, sizeof(r), 0, tmp, '\0');
  printf("s = ");
  read(0, tmp, 1024);
  OPENSSL_hexstr2buf_ex(s, sizeof(s), 0, tmp, '\0');
  puts("Enter the current contents of the message you wish to edit:");
  read(0, msg, sizeof(msg));
  SHA1(msg, sizeof(msg), hash);

  if (ecdsa_verify(&publicKey, hash, r, s) == 0) {
    puts("Signature verification failed.");
    return;
  }

  for (int i=0; i<128; i++) {
    if (used[i] != NULL) {
      if (memcmp(r, used[i]->r, sizeof(r)) == 0 && memcmp(s, used[i]->s, sizeof(s)) == 0) {
        puts("Invalid signed message!");
        _exit(-1);
        break;
      }
    }
  }

  for (int i=0; i<128; i++) {
    if (sigs[i] != NULL) {
      if (memcmp(r, sigs[i]->r, sizeof(r)) == 0 && memcmp(s, sigs[i]->s, sizeof(s)) == 0) {
        ix = i;
        break;
      }
    }
  }

  used[ox] = malloc(sizeof(struct signature));
  memcpy(used[ox]->r, r, sizeof(r));
  memcpy(used[ox]->s, s, sizeof(s));
  ox++;
  ox %= 128;
  sigs[ix] = malloc(sizeof(struct signature));
  memset(sigs[ix], 0, sizeof(struct signature));
  puts("Enter the new message to sign:");
  read(0, sigs[ix]->msg, sizeof(sigs[ix]->msg));
  SHA1(sigs[ix]->msg, sizeof(sigs[ix]->msg), sigs[ix]->hash);
  ecdsa_sign(sigs[ix]->r, sigs[ix]->s, privateKey, p_random, sigs[ix]->hash);

  printf("r = ");
  for (int i = 0; i < sizeof(sigs[ix]->r); i++) {
    printf("%02X", (unsigned char)sigs[ix]->r[i]);
  }
  printf("\n");
  printf("s = ");
  for (int i = 0; i < sizeof(sigs[ix]->s); i++) {
    printf("%02X", (unsigned char)sigs[ix]->s[i]);
  }
  printf("\n");
}

void getFlag() {
  uint8_t r[NUM_ECC_DIGITS];
  uint8_t s[NUM_ECC_DIGITS];
  char tmp[1024];
  uint8_t magic[NUM_ECC_DIGITS];
  char flag[1024];

  memset(r, 0, sizeof(r));
  memset(s, 0, sizeof(s));
  memset(tmp, 0, sizeof(tmp));
  memset(magic, 0, sizeof(magic));

  int fd = open("/dev/urandom", O_RDONLY);
  int* ptr = (int*) 0xffffffffffffffff; // safeguard

  if (fd < 0) {
    perror("urandom");
    _exit(-1);
  }
  read(fd,&magic,sizeof(magic));
  close(fd);

  printf("magic = ");
  for (int i = 0; i < sizeof(magic); i++) {
    printf("%02X", (unsigned char)magic[i]);
  }
  printf("\n");

  puts("Enter the signature of the magic number:");
  printf("r = ");
  read(0, tmp, 1024);
  OPENSSL_hexstr2buf_ex(r, sizeof(r), 0, tmp, '\0');
  printf("s = ");
  read(0, tmp, 1024);
  OPENSSL_hexstr2buf_ex(s, sizeof(s), 0, tmp, '\0');

  ptr = &fd;
  if (ecdsa_verify(&publicKey, magic, r, s) == 1) {
    puts("You win!");
    *ptr = open("flag.txt", O_RDONLY);
    read(fd, flag, 0x100);
    puts(flag);
    close(fd);
  }
  else {
    puts("Signature verification failed.");
    return;
  }
}

int main() {
  int choice;

  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  refreshNonce();
  while (ecc_make_key(&publicKey, privateKey, p_random) == 0) {
    refreshNonce();
  }
  refreshNonce();

  puts("--------------------------");
  puts("  Welcome to elliptical,  ");
  puts("     the world's best     ");
  puts("       signing app!       ");
  puts("--------------------------");

  puts("1. Sign a message");
  puts("2. Edit message");
  puts("3. Get flag");
  puts("4. Exit");
  for (int i=0; i<19; i++) {
    printf("> ");
    scanf("%d%*c", &choice);

    switch (choice) {
      case 1:
        signMessage();
        break;

      case 2:
        editMessage();
        break;

      case 3:
        getFlag();
        break;

      case 4:
        _exit(0);

      default:
        printf("Invalid choice.\n");
        break;
    }
  }
}
