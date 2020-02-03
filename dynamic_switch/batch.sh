!# /bin/bash


for si in 0.0 0.5 1.0
do
for vi in 0.0 0.5 1.0
do
for seed in $(seq 1 20)
do

python switch.py --random $seed  --simtime 20000 --sst_i $si --vip_i $vi

done
done
done


