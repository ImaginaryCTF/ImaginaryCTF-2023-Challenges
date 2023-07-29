#!/bin/bash

while [[ 1 ]]
do
  sleep 15m
  docker kill $(cat /root/instancer/instances)
  echo > /root/instancer/instances
done
