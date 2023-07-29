obj-m += chall.o
MY_CFLAGS += -g -DDEBUG -Werror
ccflags-y += ${MY_CFLAGS}
CC += ${MY_CFLAGS}

run:
	../run.sh ../initramfs.cpio

debug:
	tmux split-window -h "sudo gdb ../vmlinux -x ../gdb.sh "
	$(MAKE) run

build_module:
	make -C /lib/modules/5.19.0-43-generic/build M=$(PWD) -Werror modules
	EXTRA_CFLAGS="$(MY_CFLAGS)"
	cp ./chall.ko ../initramfs/
	cd ../initramfs && find . | cpio -H newc -ov -F ../initramfs.cpio 2> /dev/null
