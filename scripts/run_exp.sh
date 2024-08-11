#!/bin/bash

# $1: config name 1
# $2: config name 2

loop_count=10


for i in $(seq 1 $loop_count); do
    python main.py -c $1 -e $2
done
