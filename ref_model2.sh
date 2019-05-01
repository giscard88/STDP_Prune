#/bin/bash




cd ref_model



for r in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do
for seed in $(seq 1 20)
do


python network.py --random $seed --top_down_pyr 1.25 --top_down_pv 1.25 --simtime 20000 --second_lgn $r

done
done

for r in 0.1 0.3 0.5  0.7  0.9 
do
for seed in $(seq 1 20)
do


python network.py --random $seed --top_down_pyr 1.0 --top_down_pv 1.0 --simtime 20000 --second_lgn $r

done
done


cd ..




cd model_bi



for r in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do
for seed in $(seq 1 20)
do


python network_bi.py --random $seed --top_down_pyr 1.25 --top_down_pv 1.25 --simtime 20000 --second_lgn $r

done
done

for r in 0.1 0.3 0.5  0.7  0.9 
do
for seed in $(seq 1 20)
do


python network_bi.py --random $seed --top_down_pyr 1.0 --top_down_pv 1.0 --simtime 20000 --second_lgn $r

done
done


