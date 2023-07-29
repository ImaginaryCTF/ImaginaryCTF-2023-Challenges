FROM ubuntu:22.04@sha256:ac58ff7fe25edc58bdf0067ca99df00014dbd032e2246d30a722fa348fd799a5 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY flag.txt /home/user/flag.txt
COPY elliptic /home/user/chal
RUN chmod 555 /home/user/chal

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install socat -y

WORKDIR /home/user
CMD socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"/home/user/chal"
