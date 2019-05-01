#/bin/bash

#mkdir extra

#cp *.py extra
cd extra

#for r in 0.2 0.4 0.6 0.8 1.0
#do
#for seed in $(seq 1 20)
#do


#python network_2.py --random $seed --top_down_pyr 1 --top_down_pv 1 --simtime 20000 --second_lgn $r

#done
#done

for r in 0.8 0.825 0.875 0.9 0.925 0.95 0.975
do
for seed in $(seq 1 20)
do


python network_2.py --random $seed --top_down_pyr 1 --top_down_pv 1 --simtime 20000 --second_lgn $r
python network_2.py --random $seed --top_down_pyr 0 --top_down_pv 0 --simtime 20000 --second_lgn $r

done
done

