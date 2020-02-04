import nest
import pylab
import numpy
import json
from json import encoder
encoder.FLOAT_REPR=lambda o: format(o,'.2f') # this is to enforce JSON to write the data in the two significant digits 
import nest.raster_plot
from collections import defaultdict
import nest.topology as topp
import math
import sys
import argparse

from dopamine_param import *

'''

derived from multi_area.py. The difference is that V2_1 received strong LGN input. 
'''






pop=[]
nest.ResetKernel()
numpy.random.seed(msd)
vp=nest.Rank()
nest.SetKernelStatus({"total_num_virtual_procs": cpn,"resolution": h,"overwrite_files":True,"print_time":True})
N_vp = nest.GetKernelStatus(['total_num_virtual_procs'])[0]
pyrngs = [numpy.random.RandomState(s) for s in range(msd, msd+N_vp)]

nest.SetKernelStatus({"grng_seed": msd+N_vp})
nest.SetKernelStatus({"rng_seeds" : range(msd+N_vp+1, msd+2*N_vp+1)})


nest.CopyModel('iaf_psc_exp_multisynapse','pyr', Pyr_params) 
nest.CopyModel('iaf_psc_exp_multisynapse','pv', PV_params)
nest.CopyModel('iaf_psc_exp_multisynapse','sst', SST_params)
nest.CopyModel('iaf_psc_exp_multisynapse','vip', VIP_params)


celltypes=['pyr','pv']
receptors={'pyr':1,'pv':2,'sst':3,'vip':4} #Make sure they are correct synaptic ports/receptor types
for xin in celltypes:
	ModelName='From'+xin
	nest.CopyModel('static_synapse',ModelName,{"receptor_type":receptors[xin]})




p_rate=500.0



LGN_pref_rate=p_rate
LGN_nonpref_rate=p_rate*fraction

LGN_bg_rate=0.0


populations=['V1_1','V1_2','V2_1','V2_2','LM'] # two low areas (V1 and V2), each of which includes 2 populations. 
layers=['l23','l4']
celltypes=['pyr','pv']
All_cells=defaultdict(list)
external_list=defaultdict(list)
sd_list=defaultdict(list)
alltypes=[]

for xin in layers:
    for yin in celltypes:
        alltypes.append(xin+yin)


mm=nest.Create('multimeter', params={'record_from': ['I_syn_1','I_syn_2','I_syn_3','I_syn_4'],'to_accumulator':True})




vol1=nest.Create('volume_transmitter')
vol2=nest.Create('volume_transmitter')
pool1=nest.Create('iaf_psc_exp',100)
pool2=nest.Create('iaf_psc_exp',100)


if active_pool==1:
    neuro_mod1=nest.Create('poisson_generator',1,{'rate':950.0})
    neuro_mod2=nest.Create('poisson_generator',1,{'rate':0.0})
    ap='1'
else:
    neuro_mod1=nest.Create('poisson_generator',1,{'rate':0.0})
    neuro_mod2=nest.Create('poisson_generator',1,{'rate':950.0})
    ap='2'

conn_dict = {'rule': 'all_to_all'}
syn_dict={'weight':100.,'delay':1.0} #50,
nest.Connect(neuro_mod1,pool1,conn_spec=conn_dict,syn_spec=syn_dict)
nest.Connect(neuro_mod2,pool2,conn_spec=conn_dict,syn_spec=syn_dict)


nest.Connect(pool1,vol1)
nest.Connect(pool2,vol2)

print vol1, vol2
nest.CopyModel('stdp_dopamine_synapse','IC1',{"receptor_type":1,"vt":vol1[0]})
nest.CopyModel('stdp_dopamine_synapse','IC2',{"receptor_type":1,"vt":vol2[0]})

#sd_test=nest.Create('spike_detector',1,{"label":'pool', "withtime":True,"withgid":True,"to_file": False})
#nest.Connect(pool1, sd_test)

 
for xin in populations:
    area=xin[:2]
    for yin in layers:
        for zin in celltypes:
            key1=xin+yin+zin #e.g., V1_1l23pyr
            key2=yin+zin #e.g., l23pyr
            cell_n=Neuron_nums[key2]
            temp=nest.Create(zin,cell_n)
            All_cells[key1].append(temp)
            ext_key=xin[:2]+yin+zin
            temp_d=nest.Create('poisson_generator',1,{'rate':Ext[ext_key]})
            external_list[ext_key].append(temp_d)
            temp_sd=nest.Create('spike_detector',1,{"label":key1, "withtime":True,"withgid":True,"to_file": False})
            sd_list[key1].append(temp_sd)
            conn_dict = {'rule': 'all_to_all'}
            syn_dict={'model':'Frompyr','weight':100,'delay':1.0} #50,
            nest.Connect(temp_d,temp,conn_spec=conn_dict,syn_spec=syn_dict)
            nest.Connect(temp,temp_sd)


    for yin in alltypes:  
        sourcetypes=xin+yin
        source_list=list(All_cells[xin+yin][0])
        for zin in alltypes:
            targettypes=xin+zin
            target_list=list(All_cells[xin+zin][0])
            conn_keys=yin+'_'+zin 
            if area=='V1':
                exception=V1_exceptions
                weights=V1_weights
            elif area=='LM':
                exception=LM_exceptions
                weights=LM_weights
            
            if yin[:2]=='l2':
                pre_i=3
            else:
                pre_i=2

            if zin[:2]=='l2':
                post_i=3
            else:
                post_i=2
 
            
            pair=yin[pre_i:]+'_'+zin[post_i:] #pyr_pyr
            #print pair, yin[:1], pre_i
            key_layers=yin[:pre_i]+'_'+zin[:post_i] #l23_l23
            if pair in P_conn[key_layers]:
                if conn_keys in exception:
                    wv=exception[conn_keys]
                else:
                    wv=weights[pair]
               
                conn_dict={'rule':'pairwise_bernoulli','p':P_conn[key_layers][pair]}
                syn_dict={'model':'From'+yin[pre_i:],'weight':wv,'delay':1.0}
                nest.Connect(source_list,target_list,conn_spec=conn_dict, syn_spec=syn_dict)

# Let's implement lateral inhibition across two population in the same area





lateral_conn_pr=0.0
lateral_conn_w=0.0
#V1_1-V1_2
conn_dict={'rule':'pairwise_bernoulli','p':lateral_conn_pr}
syn_dict={'model':'Frompyr','weight':lateral_conn_w,'delay':1.0}


source_list=All_cells['V1_1l23pyr'][0]
target_list=All_cells['V1_2l23pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)
source_list=All_cells['V1_2l23pyr'][0]
target_list=All_cells['V1_1l23pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

#V2_1-V1_2

source_list=All_cells['V2_1l23pyr'][0]
target_list=All_cells['V2_2l23pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)
source_list=All_cells['V2_2l23pyr'][0]
target_list=All_cells['V2_1l23pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)



IC_delay=5.0



# IC 
conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pyr}
syn_dict={'model':'IC1','weight':w_bu_pyr,'delay':IC_delay}



reduction_factor=0.5
#bottom-up: pref_LM
source_list=All_cells['V1_1l23pyr'][0]
target_list=All_cells['LMl4pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pv*reduction_factor}
syn_dict={'model':'IC1','weight':w_bu_pv,'delay':IC_delay}
source_list=All_cells['V1_1l23pyr'][0]
target_list=All_cells['LMl4pv'][0]
nest.Connect(source_list,target_list,conn_spec=conn_dict, syn_spec=syn_dict)

#bottom-up: nonpref-LM

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pyr*reduction_factor}
syn_dict={'model':'IC1','weight':w_bu_pyr,'delay':IC_delay}
source_list=All_cells['V1_2l23pyr'][0]
target_list=All_cells['LMl4pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pv*reduction_factor}
syn_dict={'model':'IC1','weight':w_bu_pv,'delay':IC_delay}
source_list=All_cells['V1_2l23pyr'][0]
target_list=All_cells['LMl4pv'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

#bottom-up: V2_1-LM

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pyr*reduction_factor}
syn_dict={'model':'IC2','weight':w_bu_pyr,'delay':IC_delay}
source_list=All_cells['V2_1l23pyr'][0]
target_list=All_cells['LMl4pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pv}
syn_dict={'model':'IC2','weight':w_bu_pv,'delay':IC_delay}
source_list=All_cells['V2_1l23pyr'][0]
target_list=All_cells['LMl4pv'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

#bottom-up: V2_2-LM

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pyr}
syn_dict={'model':'IC2','weight':w_bu_pyr,'delay':IC_delay}
source_list=All_cells['V2_2l23pyr'][0]
target_list=All_cells['LMl4pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pv}
syn_dict={'model':'IC2','weight':w_bu_pv,'delay':IC_delay}
source_list=All_cells['V2_2l23pyr'][0]
target_list=All_cells['LMl4pv'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)









#top-down targeting layer 2/3 # Now, it is 

conn_dict={'rule':'pairwise_bernoulli','p':0.3}
syn_dict={'model':'Frompyr','weight':td_super_pyr,'delay':IC_delay}
target_list=[]
source_list=All_cells['LMl23pyr'][0]
target_list.extend(All_cells['V1_1l23pyr'][0])
target_list.extend(All_cells['V1_2l23pyr'][0])
target_list.extend(All_cells['V2_1l23pyr'][0])
target_list.extend(All_cells['V2_2l23pyr'][0])
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

conn_dict={'rule':'pairwise_bernoulli','p':0.3}
syn_dict={'model':'Frompyr','weight':td_super_pv,'delay':IC_delay}
target_list=[]
source_list=All_cells['LMl23pyr'][0]
target_list.extend(All_cells['V1_1l23pv'][0])
target_list.extend(All_cells['V1_2l23pv'][0])
target_list.extend(All_cells['V2_1l23pv'][0])
target_list.extend(All_cells['V2_2l23pv'][0])
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)






# connect to multimeter
source_list=All_cells['V1_1l23pyr'][0]
nest.Connect(mm,source_list)




# introduce the LGN inputs

pref_lgn=nest.Create('poisson_generator',1,{'rate':LGN_pref_rate})
nonpref_lgn=nest.Create('poisson_generator',1,{'rate':LGN_nonpref_rate})
# to pyr
target_list1=All_cells['V1_1l4pyr'][0]
target_list2=All_cells['V1_2l4pyr'][0]
target_list3=All_cells['V2_1l4pyr'][0]
target_list4=All_cells['V2_2l4pyr'][0]
conn_dict={'rule':'pairwise_bernoulli','p':0.3}
syn_dict={'model':'Frompyr','weight':w_lgn_pyr,'delay':1.0}
nest.Connect(pref_lgn,list(target_list1),conn_spec=conn_dict, syn_spec=syn_dict)
nest.Connect(nonpref_lgn,list(target_list2),conn_spec=conn_dict, syn_spec=syn_dict)
nest.Connect(pref_lgn,list(target_list3),conn_spec=conn_dict, syn_spec=syn_dict)
nest.Connect(nonpref_lgn,list(target_list4),conn_spec=conn_dict, syn_spec=syn_dict)

# to pv
target_list1=All_cells['V1_1l4pv'][0]
target_list2=All_cells['V1_2l4pv'][0]
target_list3=All_cells['V2_1l4pv'][0]
target_list4=All_cells['V2_2l4pv'][0]
conn_dict={'rule':'pairwise_bernoulli','p':0.3}
syn_dict={'model':'Frompyr','weight':w_lgn_pv,'delay':1.0}
nest.Connect(pref_lgn,list(target_list1),conn_spec=conn_dict, syn_spec=syn_dict)
nest.Connect(nonpref_lgn,list(target_list2),conn_spec=conn_dict, syn_spec=syn_dict)
nest.Connect(pref_lgn,list(target_list3),conn_spec=conn_dict, syn_spec=syn_dict)
nest.Connect(nonpref_lgn,list(target_list4),conn_spec=conn_dict, syn_spec=syn_dict)

source_list1=list(All_cells['V1_1l23pyr'][0])
source_list2=list(All_cells['V1_2l23pyr'][0])
source_list3=list(All_cells['V2_1l23pyr'][0])
source_list4=list(All_cells['V2_2l23pyr'][0])
target_list=list(All_cells['LMl4pyr'][0])

pref_pref_bu=nest.GetConnections(source_list1,target_list)
nonpref_pref_bu=nest.GetConnections(source_list2,target_list)
V2_1_bu=nest.GetConnections(source_list3,target_list)
V2_2_bu=nest.GetConnections(source_list4,target_list)


#print pref_pref_bu

weights={}

pref_pref_bu_weight=nest.GetStatus(pref_pref_bu)
nonpref_pref_bu_weight=nest.GetStatus(nonpref_pref_bu)
V2_1_bu_weight=nest.GetStatus(V2_1_bu)
V2_2_bu_weight=nest.GetStatus(V2_2_bu)

p_p=[]
np_p=[]
V2_1=[]
V2_2=[]
for xin in pref_pref_bu_weight:
    p_p.append(xin['weight'])
for xin in nonpref_pref_bu_weight:
    np_p.append(xin['weight'])
for xin in V2_1_bu_weight:
    V2_1.append(xin['weight'])
for xin in V2_2_bu_weight:
    V2_2.append(xin['weight'])


print 'initial weights'
print 'pref_pref', numpy.mean(numpy.array(p_p))
print 'nonpref_pref', numpy.mean(numpy.array(np_p))
print 'V2_1', numpy.mean(numpy.array(V2_1))
print 'V2_2', numpy.mean(numpy.array(V2_2))

weights['before_p_p']=p_p
weights['before_np_p']=np_p
weights['before_V2_1']=V2_1
weights['before_V2_2']=V2_2


nest.Simulate(simtime)

source_list1=list(All_cells['V1_1l23pyr'][0])
source_list2=list(All_cells['V1_2l23pyr'][0])
source_list3=list(All_cells['V2_1l23pyr'][0])
source_list4=list(All_cells['V2_2l23pyr'][0])
target_list=list(All_cells['LMl4pyr'][0])

pref_pref_bu_weight=nest.GetStatus(pref_pref_bu)
nonpref_pref_bu_weight=nest.GetStatus(nonpref_pref_bu)
V2_1_bu_weight=nest.GetStatus(V2_1_bu)
V2_2_bu_weight=nest.GetStatus(V2_2_bu)

p_p=[]
np_p=[]
V2_1=[]
V2_2=[]
for xin in pref_pref_bu_weight:
    p_p.append(xin['weight'])
for xin in nonpref_pref_bu_weight:
    np_p.append(xin['weight'])
for xin in V2_1_bu_weight:
    V2_1.append(xin['weight'])
for xin in V2_2_bu_weight:
    V2_2.append(xin['weight'])


print 'updated weights'
print 'pref_pref', numpy.mean(numpy.array(p_p))
print 'nonpref_pref', numpy.mean(numpy.array(np_p))
print 'V2_1', numpy.mean(numpy.array(V2_1))
print 'V2_2', numpy.mean(numpy.array(V2_2))

weights['after_p_p']=p_p
weights['after_np_p']=np_p
weights['after_V2_1']=V2_1
weights['after_V2_2']=V2_2





colors={'pyr':'r','pv':'b','sst':'g','vip':'k'}

spikes={}
for xin in populations:
    area=xin[:2]
    for yin in layers:
        for zin in celltypes:
            key1=xin+yin+zin #e.g., V1_1l23pyr
            target=sd_list[key1][0][0] # due to a formatting... ugly coding style, 
            
            events=nest.GetStatus([target],'events')[0]
            senders=events['senders']
            times=events['times']
            spikes[key1]=(list(times),list(senders))








# now plot the lfp
events = nest.GetStatus(mm)[0]['events']

#print events, len(events)

t = events['times']
i1=events['I_syn_1']
i2=events['I_syn_2']
i3=events['I_syn_3']
i4=events['I_syn_4']


lfp={}
lfp_raw=numpy.abs(i1)+numpy.abs(i2)+numpy.abs(i3)+numpy.abs(i4)
lfp['time']=list(t)
lfp['lfp']=list(lfp_raw) # no vip cells


if show_graph:
    sub_fig_num=len(layers)
    pylab.figure(1)

    for xi, xin in enumerate(layers):
        pylab.subplot(sub_fig_num,1,xi+1)
        if xi==0:
            pylab.title('V1_1')
        for yin in celltypes:
            spks=spikes['V1_1'+xin+yin]
            pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
            pylab.xlim([0.0,simtime])
        pylab.ylabel(xin)

    pylab.figure(2)

    for xi, xin in enumerate(layers):
        pylab.subplot(sub_fig_num,1,xi+1)
        if xi==0:
            pylab.title('V1_2')
        for yin in celltypes:
            spks=spikes['V1_2'+xin+yin]
            pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
            pylab.xlim([0.0,simtime])
        pylab.ylabel(xin)

    pylab.figure(3)

    for xi, xin in enumerate(layers):
        pylab.subplot(sub_fig_num,1,xi+1)
        if xi==0:
            pylab.title('V2_1')
        for yin in celltypes:
            spks=spikes['V2_1'+xin+yin]
            pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
            pylab.xlim([0.0,simtime])
        pylab.ylabel(xin)

    pylab.figure(4)

    for xi, xin in enumerate(layers):
        pylab.subplot(sub_fig_num,1,xi+1)
        if xi==0:
            pylab.title('V2_2')
        for yin in celltypes:
            spks=spikes['V2_2'+xin+yin]
            pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
            pylab.xlim([0.0,simtime])
        pylab.ylabel(xin)

    pylab.figure(5)

    for xi, xin in enumerate(layers):
        pylab.subplot(sub_fig_num,1,xi+1)
        if xi==0:
            pylab.title('LM')
        for yin in celltypes:
            spks=spikes['LM'+xin+yin]
            pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
            pylab.xlim([0.0,simtime])
        pylab.ylabel(xin)

    pylab.figure(6)
    pylab.plot(t,lfp_raw)

    pylab.show()


sim_len=str(int(simtime))

fn_comm='multi_dopamine2-'+ap+'-'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+str(fraction)+'_'+sim_len+'.json'



fp=open('spikes_'+fn_comm,'w')
json.dump(spikes,fp)
fp.close()

fp=open('weights_'+fn_comm,'w')
json.dump(weights,fp)
fp.close()

fp=open('lfp_'+fn_comm,'w')
json.dump(lfp,fp)
fp.close()

#events=nest.GetStatus(sd_test,'events')[0]
#senders=events['senders']
#print ('pool activity',len(senders))        
        



