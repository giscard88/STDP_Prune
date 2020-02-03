!# /bin/bash

cd alt_neuron

cd cond
chmod 755 batch.sh
./batch.sh
cd ..

cd psc_alpha
chmod 755 batch.sh
./batch.sh
cd ..

cd ..

cd dynamic_switch

chmod 755 batch.sh
./batch.sh

cd ..

cd multi_area
cd Full_Inh
chmod 755 batch.sh
./batch.sh
cd ..

cd dopamine
chmod 755 batch.sh
./batch.sh

