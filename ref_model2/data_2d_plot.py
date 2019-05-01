import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import argparse
import numpy
from collections import defaultdict
import os
#from network_param import w_bu_pyr

w_bu_pyr=40.0

parser = argparse.ArgumentParser(description='read out lfp signals from neuropixel')





parser.add_argument("--simtime", type=float, default=20000.0,
                        help="Simulation time (in terms of clock time) (default: 50000.0, 10 sec)")

parser.add_argument("--second_lgn", type=float, default=0.2,
                        help="fraction of lgn input to non-preferred column (default 0.2)")


args = parser.parse_args()


#msd=range(1,31)

sim_len=str(int(args.simtime))

fraction=args.second_lgn




test=[0.0,0.25,0.5,0.75,1.0,1.25,1.5]

test_pyr=numpy.array(test)*15.0
test_pv=numpy.array(test)*20.0

msd=range(1,21)



p_conns=defaultdict(list)
np_conns=defaultdict(list)

y_t=[]
x_t=[]
#fn_comm='model'+model+':'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+sim_len+'_'+str(conn_ratio)+str(str_ratio)+'.json'

plot_data_np=numpy.zeros((len(test),len(test)))
plot_data_p=numpy.zeros((len(test),len(test)))
plot_data_diff=numpy.zeros((len(test),len(test)))
for xi, xin in enumerate(test): # top_down_pyr
    x_t.append(xi)
    for yi, yin in enumerate(test): #top_down_pv
        if xi==0:
            y_t.append(yi)
        temp_np=[]
        temp_p=[]
        temp_diff=[]
    
        for zin in msd:

            fn_comm=str(xin)+'_'+str(yin)+'_'+str(zin)+'_'+str(fraction)+'_'+sim_len+'.json'

            fp=open('weights_'+fn_comm,'r')
            data=json.load(fp)
            temp=data['after_p_p']
            temp=numpy.array(temp)-w_bu_pyr
            temp_p.append(numpy.mean(temp))

            temp=data['after_np_p']
            temp=numpy.array(temp)-w_bu_pyr
            temp_np.append(numpy.mean(temp))
            
            temp_diff.append(temp_p[-1]-temp_np[-1])

        temp_p=numpy.array(temp_p)
        temp_np=numpy.array(temp_np)
        temp_diff=numpy.array(temp_diff)
        plot_data_p[yi,xi]=numpy.mean(temp_p)
        plot_data_np[yi,xi]=numpy.mean(temp_np)
        plot_data_diff[yi,xi]=numpy.mean(temp_diff) 


max_v=numpy.amax(plot_data_p)
min_v=numpy.amin(plot_data_np)



plt.figure(1)
plt.imshow(plot_data_p,cmap='jet',vmin=min_v, vmax=max_v)
plt.yticks(y_t, test_pv)
plt.xticks(x_t, test_pyr)
plt.ylabel('input_to_pv')
plt.xlabel('input_to_pyr')
plt.colorbar(cmap=plt.cm.jet)
plt.title('pref')
plt.savefig('../figs/2d_plot_pref.eps')
plt.figure(2)
plt.imshow(plot_data_np,cmap='jet',vmin=min_v, vmax=max_v)
plt.yticks(y_t, test_pv)
plt.xticks(x_t, test_pyr)
plt.ylabel('input_to_pv')
plt.xlabel('input_to_pyr')
plt.colorbar(cmap=plt.cm.jet)
plt.title('nonpref')
plt.savefig('../figs/2d_plot_nonpref.eps')
plt.figure(3)
plt.imshow(plot_data_diff,cmap='jet')
plt.yticks(y_t, test_pv)
plt.xticks(x_t, test_pyr)
plt.ylabel('input_to_pv')
plt.xlabel('input_to_pyr')
plt.colorbar(cmap=plt.cm.jet)
plt.title('diff')




plt.savefig('../figs2/2d_plot_diff.eps')
plt.show()    
     


        
        
     


    






