#! /bin/bash



for seed in $(seq 1 20)
do

python cond.py --random $seed --simtime 100000 --show_graph False

done

