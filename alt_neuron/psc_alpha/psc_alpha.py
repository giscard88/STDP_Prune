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

from psc_alpha_param import *

'''

model 1 tests a selective activation V1 population (V1_1). It assume the equivalent connections from V1 to a HVA (e.g., LM).
model 2 tests the asymmetric connectons from V1 to a HVA (e.g., LM). It assumes the equal inputs to the two populations of V1. 

One of the two model can be selected by setting up model flag (--model 1 or 2).

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


nest.CopyModel('iaf_psc_alpha','pyr', Pyr_params) 
nest.CopyModel('iaf_psc_alpha','pv', PV_params)


celltypes=['pyr','pv']
receptors={'pyr':1,'pv':2} #Make sure they are correct synaptic ports/receptor types
for xin in celltypes:
	ModelName='From'+xin
	nest.CopyModel('static_synapse',ModelName) # this class does not have syanpse port


nest.CopyModel('stdp_synapse','IC',{'alpha':1.5})

p_rate=500.0



LGN_pref_rate=p_rate
LGN_nonpref_rate=p_rate*fraction

LGN_bg_rate=0.0


populations=['V1_1','V1_2','LM']
layers=['l23','l4']
celltypes=['pyr','pv']
All_cells=defaultdict(list)
external_list=defaultdict(list)
sd_list=defaultdict(list)
alltypes=[]

for xin in layers:
    for yin in celltypes:
        alltypes.append(xin+yin)


#mm=nest.Create('multimeter', params={'record_from': ['I_syn_1','I_syn_2'],'to_accumulator':True})





 
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
            syn_dict={'model':'Frompyr','weight':100.0,'delay':1.0} #50,
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
            if conn_keys in exception:
                wv=exception[conn_keys]
            else:
                wv=weights[pair]
               
            conn_dict={'rule':'pairwise_bernoulli','p':P_conn[key_layers][pair]}
            syn_dict={'model':'From'+yin[pre_i:],'weight':wv,'delay':1.0}
            nest.Connect(source_list,target_list,conn_spec=conn_dict, syn_spec=syn_dict)



IC_delay=5.0



# IC 
conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pyr}
syn_dict={'model':'IC','weight':w_bu_pyr,'delay':IC_delay}


#bottom-up: pref_pref
source_list=All_cells['V1_1l23pyr'][0]
target_list=All_cells['LMl4pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pv}
syn_dict={'model':'IC','weight':w_bu_pv,'delay':IC_delay}
source_list=All_cells['V1_1l23pyr'][0]
target_list=All_cells['LMl4pv'][0]
nest.Connect(source_list,target_list,conn_spec=conn_dict, syn_spec=syn_dict)

#bottom-up: nonpref-pref

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pyr}
syn_dict={'model':'IC','weight':w_bu_pyr,'delay':IC_delay}
source_list=All_cells['V1_2l23pyr'][0]
target_list=All_cells['LMl4pyr'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

conn_dict={'rule':'pairwise_bernoulli','p':P_pref_pref_pv}
syn_dict={'model':'IC','weight':w_bu_pv,'delay':IC_delay}
source_list=All_cells['V1_2l23pyr'][0]
target_list=All_cells['LMl4pv'][0]
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)







#top-down targeting layer 2/3

conn_dict={'rule':'pairwise_bernoulli','p':0.3}
syn_dict={'model':'Frompyr','weight':td_super_pyr,'delay':IC_delay}
target_list=[]
source_list=All_cells['LMl23pyr'][0]
target_list.extend(All_cells['V1_1l23pyr'][0])
target_list.extend(All_cells['V1_2l23pyr'][0])
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)

conn_dict={'rule':'pairwise_bernoulli','p':0.3}
syn_dict={'model':'Frompyr','weight':td_super_pv,'delay':IC_delay}
target_list=[]
source_list=All_cells['LMl23pyr'][0]
target_list.extend(All_cells['V1_1l23pv'][0])
target_list.extend(All_cells['V1_2l23pv'][0])
nest.Connect(list(source_list),list(target_list),conn_spec=conn_dict, syn_spec=syn_dict)






# connect to multimeter
#source_list=All_cells['V1_1l23pyr'][0]
#nest.Connect(mm,source_list)




# introduce the LGN inputs

pref_lgn=nest.Create('poisson_generator',1,{'rate':LGN_pref_rate})
nonpref_lgn=nest.Create('poisson_generator',1,{'rate':LGN_nonpref_rate})
# to pyr
target_list1=All_cells['V1_1l4pyr'][0]
target_list2=All_cells['V1_2l4pyr'][0]
conn_dict={'rule':'pairwise_bernoulli','p':0.3}
syn_dict={'model':'Frompyr','weight':w_lgn_pyr,'delay':1.0}
nest.Connect(pref_lgn,list(target_list1),conn_spec=conn_dict, syn_spec=syn_dict)
nest.Connect(nonpref_lgn,list(target_list2),conn_spec=conn_dict, syn_spec=syn_dict)

# to pv
target_list1=All_cells['V1_1l4pv'][0]
target_list2=All_cells['V1_2l4pv'][0]
conn_dict={'rule':'pairwise_bernoulli','p':0.3}
syn_dict={'model':'Frompyr','weight':w_lgn_pv,'delay':1.0}
nest.Connect(pref_lgn,list(target_list1),conn_spec=conn_dict, syn_spec=syn_dict)
nest.Connect(nonpref_lgn,list(target_list2),conn_spec=conn_dict, syn_spec=syn_dict)

source_list1=list(All_cells['V1_1l23pyr'][0])
source_list2=list(All_cells['V1_2l23pyr'][0])
target_list=list(All_cells['LMl4pyr'][0])

pref_pref_bu=nest.GetConnections(source_list1,target_list)
nonpref_pref_bu=nest.GetConnections(source_list2,target_list)



#print pref_pref_bu

weights={}

pref_pref_bu_weight=nest.GetStatus(pref_pref_bu)
nonpref_pref_bu_weight=nest.GetStatus(nonpref_pref_bu)
p_p=[]
np_p=[]
for xin in pref_pref_bu_weight:
    p_p.append(xin['weight'])
for xin in nonpref_pref_bu_weight:
    np_p.append(xin['weight'])


print 'initial weights'
print 'pref_pref', numpy.mean(numpy.array(p_p))
print 'nonpref_pref', numpy.mean(numpy.array(np_p))

weights['before_p_p']=p_p
weights['before_np_p']=np_p



nest.Simulate(simtime)

source_list1=list(All_cells['V1_1l23pyr'][0])
source_list2=list(All_cells['V1_2l23pyr'][0])
target_list=list(All_cells['LMl4pyr'][0])

pref_pref_bu=nest.GetConnections(source_list1,target_list)
nonpref_pref_bu=nest.GetConnections(source_list2,target_list)
pref_pref_bu_weight=nest.GetStatus(pref_pref_bu)
nonpref_pref_bu_weight=nest.GetStatus(nonpref_pref_bu)

p_p=[]
np_p=[]
for xin in pref_pref_bu_weight:
    p_p.append(xin['weight'])
for xin in nonpref_pref_bu_weight:
    np_p.append(xin['weight'])

print 'updated weights'
print 'pref_pref', numpy.mean(numpy.array(p_p))
print 'nonpref_pref', numpy.mean(numpy.array(np_p))

weights['after_p_p']=p_p
weights['after_np_p']=np_p



colors={'pyr':'r','pv':'b'}

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
#events = nest.GetStatus()[0]['events']

#print events, len(events)

#t = events['times']
#i1=events['I_syn_1']
#i2=events['I_syn_2']

#lfp={}
#lfp_raw=numpy.abs(i1)+numpy.abs(i2)
#lfp['time']=list(t)
#lfp['lfp']=list(lfp_raw) # no vip cells


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
            pylab.title('LM')
        for yin in celltypes:
            spks=spikes['LM'+xin+yin]
            pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
            pylab.xlim([0.0,simtime])
        pylab.ylabel(xin)
    pylab.show()


sim_len=str(int(simtime))

fn_comm='psc_alpha'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+str(fraction)+'_'+sim_len+'.json'



fp=open('spikes_'+fn_comm,'w')
json.dump(spikes,fp)
fp.close()

fp=open('weights_'+fn_comm,'w')
json.dump(weights,fp)
fp.close()


        
        
        



