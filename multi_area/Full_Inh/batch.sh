!#/bin/bash


for v1 in 0 1.0
do
for v2 in 0 1.0
do

for seed in $(seq 1 20)
do

python multi_area.py --random $seed --simtime 20000 --vip1_i $v1 --vip2_i $v2

done
done
done

