#/bin/bash


mkdir model_bi
cp *.py model_bi

cd model_bi

for pyr in 0.0 0.25 0.5 0.75 1.0 1.25 1.5
do
for pv in 0.0 0.25 0.5 0.75 1.0 1.25 1.5
do
for seed in $(seq 1 20)
do


python network_bi.py --random $seed --top_down_pyr $pyr --top_down_pv $pv --simtime 20000

done
done
done

for r in 0.2 0.4 0.6 0.8 1.0
do
for seed in $(seq 1 20)
do


python network_bi.py --random $seed --top_down_pyr 1 --top_down_pv 1 --simtime 20000 --second_lgn $r

done
done



