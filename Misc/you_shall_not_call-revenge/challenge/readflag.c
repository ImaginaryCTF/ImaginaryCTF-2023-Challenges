#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *check[] = {"yes", "please", "give", "me", "the", "flag"};
int main(int argc, char **argv) {
	if (argc != 7) {
		printf("Usage: %s yes please give me the flag\n", argv[0]);
		exit(1);
	}
	for (int i = 1; i < argc; i++) {
		if (strcmp(argv[i], check[i - 1])) {
			printf("Usage: %s yes please give me the flag\n", argv[0]);
			exit(1);
		}
	}
	puts("ictf{I_h0p3_y0ur_c4ll_f1ll3d_7h3_r3g1str4t10n_f0rm}");
	return 0;
}
// musl-gcc readflag.c -o readflag -static -Os && strip readflag
