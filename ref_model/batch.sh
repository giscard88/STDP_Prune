
for r in 0.825 0.85 0.875 0.9 0.925 0.95 0.975
do
for seed in $(seq 1 20)
do


python network.py --random $seed --top_down_pyr 1 --top_down_pv 1 --simtime 20000 --second_lgn $r

done
done

