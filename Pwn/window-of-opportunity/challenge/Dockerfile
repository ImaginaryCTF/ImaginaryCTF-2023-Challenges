FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install qemu-system-x86 socat -y
RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY ./bzImage /home/user/
COPY ./initramfs.cpio /home/user/
COPY run.sh /home/user/
COPY run.py /home/user/

WORKDIR "/home/user"

RUN chmod 555 bzImage initramfs.cpio run.sh run.py
RUN chmod +x /home/user/run.sh

USER user

CMD socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"python3 /home/user/run.py"
