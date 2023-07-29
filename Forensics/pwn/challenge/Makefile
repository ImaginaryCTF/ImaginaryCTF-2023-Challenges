all:
#	gcc vuln.c -o vuln
	patchelf vuln --set-interpreter ./ld-2.31.so --replace-needed libc.so.6 ./libc-2.31.so
