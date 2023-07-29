all:
	gcc vuln.c -o vuln -fno-stack-protector -no-pie
	gcc -Wall -fPIC -shared -o preload.so preload.c -lseccomp
