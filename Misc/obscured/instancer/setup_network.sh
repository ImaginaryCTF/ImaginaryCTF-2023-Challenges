#!/bin/bash

docker network create --subnet 10.42.0.0/16 no-internet
iptables --insert DOCKER-USER -s 10.42.0.0/16 -j REJECT --reject-with icmp-port-unreachable
iptables --insert DOCKER-USER -s 10.42.0.0/16 -m state --state RELATED,ESTABLISHED -j RETURN
