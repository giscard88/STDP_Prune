#! /bin/bash



for seed in $(seq 1 20)
do

python cond.py --randon $seed --simtime 100000 --show_graph False

done

