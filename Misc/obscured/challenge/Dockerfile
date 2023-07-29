FROM fedora

RUN dnf install polkit -y
RUN dnf install openssh-server -y

RUN useradd user
RUN bash -c "chpasswd <<< 'user:password'"

COPY 49-polkit-pkla-compat.rules /etc/polkit-1/rules.d/49-polkit-pkla-compat.rules
COPY flag.txt /root/flag.txt

RUN chmod 000 /root/flag.txt
RUN chmod -R 555 /etc/polkit-1/rules.d/

RUN ssh-keygen -A

CMD bash -c 'bash -c "chpasswd <<< 'user:$PASSWORD'"' && /sbin/init
