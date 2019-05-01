#/bin/bash




cd ref_model



for r in 1.0
do
for seed in $(seq 81 120)
do


python network.py --random $seed --top_down_pyr 1 --top_down_pv 1 --simtime 20000 --second_lgn $r

done
done


