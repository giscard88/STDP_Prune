#/bin/bash


cd extra

for r in 0.2 0.4 0.6 0.8 1.0
do
for seed in $(seq 1 20)
do


python network_2.py --random $seed --top_down_pyr 0 --top_down_pv 0 --simtime 20000 --second_lgn $r

done
done


