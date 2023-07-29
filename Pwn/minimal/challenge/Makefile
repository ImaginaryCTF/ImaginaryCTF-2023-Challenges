all:
	gcc vuln.c -o vuln -fno-stack-protector -no-pie
#	patchelf ./vuln --set-interpreter ./ld-linux-x86-64.so.2 --replace-needed libc.so.6 ./libc.so.6
