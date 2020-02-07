#! /bin/bash



for seed in $(seq 1 20)
do

python cond.py --random $seed --simtime 50000 --show_graph False

done

