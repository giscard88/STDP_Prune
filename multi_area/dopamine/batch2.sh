#! /bin/bash



for ap in 1 2
do

for seed in $(seq 1 20)
do

python multi_dopamine2.py --random $seed --simtime 20000 --mod_config $ap

done
done


