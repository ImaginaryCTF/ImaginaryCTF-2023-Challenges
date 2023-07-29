#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define CBC 1
#include "aes.h"

#define AES 0
#define XOR 1
#define NOP 2

struct aes_cipher {
  unsigned long type;
  char key[16];
};

struct xor_cipher {
  unsigned long type;
  char key;
};

struct nop_cipher {
  unsigned long type;
};

struct ciphertext {
  unsigned long type;
  char buf[64];
};

struct aes_cipher *aes = 0;
struct xor_cipher *xor = 0;
struct nop_cipher *nop = 0;
struct ciphertext *ciphertexts[16];
int status[16];

void xor_encrypt(struct ciphertext* ciphertext, char key) {
  for (int i = 0; i < sizeof(ciphertext->buf); i++) {
    ciphertext->buf[i] = ciphertext->buf[i] ^ key;
  }
}

void nop_encrypt(struct ciphertext* ciphertext) {
  return;
}

void aes_encrypt(struct ciphertext* ciphertext, char* key) {
  char* aeskey = calloc(1, 16);
  char* iv = calloc(1, 16);
  struct AES_ctx ctx;
  memcpy(aeskey, key, 8);
  memcpy(iv, key+8, 8);
  AES_init_ctx_iv(&ctx, aeskey, iv);
  AES_CBC_encrypt_buffer(&ctx, ciphertext->buf, 64);
}

void encrypt(struct ciphertext* ciphertext) {
  int choice;
  printf("Select a cipher for encryption:\n");
  printf("0. AES\n");
  printf("1. XOR\n");
  printf("2. NOP\n");
  printf("Enter your choice: ");
  scanf("%d%*c", &choice);

  switch (choice) {
    case XOR:
      if (xor != NULL) {
        ciphertext->type = XOR;
        xor_encrypt(ciphertext, xor->key);
        printf("Ciphertext encrypted using XOR cipher.\n");
      } else {
        printf("XOR cipher is not created.\n");
      }
      break;

    case NOP:
      if (nop != NULL) {
        ciphertext->type = NOP;
        nop_encrypt(ciphertext);
        printf("Ciphertext encrypted using NOP cipher.\n");
      } else {
        printf("NOP cipher is not created.\n");
      }
      break;

    case AES:
      if (aes != NULL) {
        ciphertext->type = AES;
        aes_encrypt(ciphertext, aes->key);
        printf("Ciphertext encrypted using AES cipher.\n");
      } else {
        printf("AES cipher is not created.\n");
      }
      break;

    default:
      printf("Invalid choice.\n");
      break;
  }
}

void create_cipher() {
  int choice;
  printf("Select a cipher type:\n");
  printf("0. AES\n");
  printf("1. XOR\n");
  printf("2. NOP\n");
  printf("Enter your choice: ");
  scanf("%d%*c", &choice);

  switch (choice) {
    case AES:
      if (aes == NULL) {
        aes = malloc(sizeof(struct aes_cipher));
        aes->type = AES;
        printf("Enter the AES key (16 characters): ");
        fgets(aes->key, 16, stdin);
      }
      else {
        printf("Cipher already created.\n");
      }
      break;

    case XOR:
      if (xor == NULL) {
        xor = malloc(sizeof(struct xor_cipher));
        xor->type = XOR;
        printf("Enter the XOR key (a single character): ");
        scanf("%c%*c", &xor->key);
      }
      else {
        printf("Cipher already created.\n");
      }
      break;

    case NOP:
      if (nop == NULL) {
        nop = malloc(sizeof(struct nop_cipher));
        nop->type = NOP;
      }
      else {
        printf("Cipher already created.\n");
      }
      break;

    default:
      printf("Invalid cipher.\n");
      break;
  }
}

void delete_cipher() {
  int choice;
  printf("Select a cipher type:\n");
  printf("0. AES\n");
  printf("1. XOR\n");
  printf("2. NOP\n");
  printf("Enter your choice: ");
  scanf("%d%*c", &choice);

  switch (choice) {
    case AES:
      free(aes);
      printf("AES cipher deleted.\n");
      break;

    case XOR:
      free(xor);
      printf("XOR cipher deleted.\n");
      break;

    case NOP:
      free(nop);
      printf("NOP cipher deleted.\n");
      break;

    default:
      printf("Invalid choice.\n");
      break;
  }
}

void create_ciphertext() {
  int index;
  printf("Enter the index for the new ciphertext (0-15): ");
  scanf("%d%*c", &index);

  if (index < 0 || index >= 16) _exit(-1);
  if (ciphertexts[index] != NULL) _exit(-1);

  ciphertexts[index] = malloc(sizeof(struct ciphertext));
  memset(ciphertexts[index]->buf, 0, sizeof(ciphertexts[index]->buf));

  printf("Enter the secret: ");
  fgets(ciphertexts[index]->buf, 64, stdin);

  encrypt(ciphertexts[index]);

  printf("Ciphertext created at index %d.\n", index);
}

void delete_ciphertext() {
  int index;
  printf("Enter the index of the ciphertext to delete (0-15): ");
  scanf("%d%*c", &index);

  if (status[index] >= 1) _exit(-1);

  if (index < 0 || index >= 16) _exit(-1);

  if (ciphertexts[index] != NULL) {
    free(ciphertexts[index]);
    status[index] = 1;
    printf("Ciphertext at index %d deleted.\n", index);
  } else {
    printf("Ciphertext at index %d does not exist.\n", index);
  }
}

void view_ciphertext() {
  int index;
  printf("Enter the index of the ciphertext to view (0-15): ");
  scanf("%d%*c", &index);

  if (index < 0 || index >= 16) _exit(-1);

  if (ciphertexts[index] != NULL) {
    for (int i = 0; i < sizeof(ciphertexts[index]->buf); i++) {
      printf("%02X ", (unsigned char)ciphertexts[index]->buf[i]);
    }
    printf("\n");
  }
}

void encrypt_flag() {
  int index;
  printf("Enter the index of the ciphertext to encrypt the flag in (0-15): ");
  scanf("%d%*c", &index);

  if (index < 0 || index >= 16) _exit(-1);

  ciphertexts[index] = malloc(sizeof(struct ciphertext));
  FILE* flag = fopen("flag.txt", "rb");
  if (flag == NULL) {
    puts("Flag file not found!");
    _exit(-1);
  }
  fread(ciphertexts[0]->buf, 1, 64, flag);
  aes_encrypt(ciphertexts[0], aes->key);
  fclose(flag);
}

void initialize() {
  size_t bytesRead;

  setbuf(stdin, NULL);
  setbuf(stdout, NULL);

  aes = malloc(sizeof(struct aes_cipher));
  aes->type = AES;

  FILE* urandom = fopen("/dev/urandom", "rb");
  if (urandom == NULL) _exit(-1);
  bytesRead = fread(aes->key, 1, 16, urandom);
  if (bytesRead < 16) _exit(-1);
  fclose(urandom);
}

int main() {
  int choice;

  initialize();

  puts("\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\n\x20\x20\x20\x20\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\n\x20\x20\u2588\u2588\x20\x20\x20\x20\x20\x20\x20\x20\u2588\u2588\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\n\u2588\u2588\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\n\u2588\u2588\x20\x20\u2588\u2588\u2588\u2588\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\u2588\u2588\n\u2588\u2588\x20\x20\u2588\u2588\u2588\u2588\x20\x20\x20\x20\x20\x20\u2591\u2591\u2591\u2591\u2588\u2588\u2591\u2591\u2588\u2588\u2591\u2591\u2588\u2588\u2591\u2591\u2588\u2588\n\u2588\u2588\u2591\u2591\x20\x20\x20\x20\x20\x20\x20\x20\u2591\u2591\u2588\u2588\u2588\u2588\x20\x20\u2588\u2588\x20\x20\u2588\u2588\x20\x20\u2588\u2588\x20\x20\n\x20\x20\u2588\u2588\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2588\u2588\x20\x20\x20\x57\x65\x6c\x63\x6f\x6d\x65\x20\x74\x6f\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\n\x20\x20\x20\x20\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\x20\x20\x20\x20\x20\x74\x68\x65\x20\x76\x61\x75\x6c\x74\n\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d");

  printf("Select an option:\n");
  printf("1. Create cipher\n");
  printf("2. Delete cipher\n");
  printf("3. Create secret\n");
  printf("4. Delete secret\n");
  printf("5. View encrypted secret\n");
  printf("6. Encrypt flag\n");
  printf("7. Exit\n");

  while (1) {
    printf("> ");
    scanf("%d%*c", &choice);

    switch (choice) {
      case 1:
        create_cipher();
        break;

      case 2:
        delete_cipher();
        break;

      case 3:
        create_ciphertext();
        break;

      case 4:
        delete_ciphertext();
        break;

      case 5:
        view_ciphertext();
        break;

      case 6:
        encrypt_flag();
        break;

      case 7:
        _exit(0);

      default:
        printf("Invalid choice.\n");
        break;
    }
  }
}
