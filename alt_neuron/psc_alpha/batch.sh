#! /bin/bash



for seed in $(seq 1 20)
do

python psc_alpha.py --random $seed --simtime 20000 --show_graph False

done

