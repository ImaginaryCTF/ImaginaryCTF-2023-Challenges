FROM pwn.red/jail

COPY --from=ubuntu:22.04 / /srv

COPY run.sh /srv/app/run
COPY vuln /srv/app/vuln
COPY preload.so /srv/app/preload.so
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run /srv/app/vuln

ENV JAIL_TIME=120
