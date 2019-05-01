#/bin/bash

for r in 0.8 0.825 0.875 0.9 0.925 0.95 0.975 0.2 0.4 0.6
do
for seed in $(seq 1 20)
do


python network_no_bottom-up.py --random $seed --top_down_pyr 1 --top_down_pv 1 --simtime 20000 --second_lgn $r

done
done


