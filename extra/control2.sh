#/bin/bash

for r in 0.8 0.85 0.9 0.95 #0.2 0.4 0.6 0.8 1.0
do
for seed in $(seq 11 20)
do


python network_no_bottom-up.py --random $seed --top_down_pyr 1 --top_down_pv 1 --simtime 20000 --second_lgn $r

done
done


