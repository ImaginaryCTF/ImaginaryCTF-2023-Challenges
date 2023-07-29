
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get install docker.io python3 socat curl -y

RUN mkdir /root/instancer/
COPY cleanup.sh /root/instancer/
COPY run.py /root/instancer/

RUN chmod +x /root/instancer/run.py
RUN chmod +x /root/instancer/cleanup.sh

CMD bash /root/instancer/cleanup.sh & socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"python3 /root/instancer/run.py"
