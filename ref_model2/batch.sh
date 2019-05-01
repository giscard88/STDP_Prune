
for r in 0.5 0.6 0.7 0.8 0.9
do
for seed in $(seq 1 20)
do


python network.py --random $seed --top_down_pyr 1 --top_down_pv 1 --simtime 20000 --second_lgn $r

done
done

