import pylab
import json
import argparse
import numpy
from collections import defaultdict
from scipy import signal
#from network_param import w_bu_pyr



parser = argparse.ArgumentParser(description='read out lfp signals from neuropixel')


parser.add_argument("--top_down_pv", type=float, default=1.0,
                        help="Scale of top-down signals to pv (default: 1)")

parser.add_argument("--top_down_pyr", type=float, default=1.0,
                        help="Scale of top-down signals to pyr (default: 1)")

parser.add_argument("--simtime", type=float, default=20000.0,
                        help="Simulation time (in terms of clock time) (default: 200000.0, 10 sec)")


parser.add_argument("--second_lgn", type=float, default=0.2,
                        help="ratio of lgn (default:0,2)")



args = parser.parse_args()


msd=range(1,21)
top_down_pyr=args.top_down_pyr
top_down_pv=args.top_down_pv
sim_len=str(int(args.simtime))
fraction=args.second_lgn

w_bu_pyr=40.0

p_p_w=[]
np_p_w=[]
lfp_b=[]
lfp_g=[]

#fn_comm='model'+model+':'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+sim_len+'_'+str(conn_ratio)+str(str_ratio)+'.json'

for yin in msd:

     
     fn_comm=str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(yin)+'_'+str(fraction)+'_'+sim_len+'.json'
                


     fp=open('lfp_'+fn_comm,'r')
     data=json.load(fp)
     fp.close()
     lfp=numpy.array(data['lfp'])
     f1, Pxx_den1 = signal.welch(lfp, 1000.)

     fp=open('lfp2_'+fn_comm,'r')
     data=json.load(fp)
     fp.close()
     lfp=numpy.array(data['lfp'])
     f2, Pxx_den2 = signal.welch(lfp, 1000.)

     pylab.plot(f1,Pxx_den1-Pxx_den2)
     
pylab.xlim([0,100])
pylab.savefig('../figs/gama_comp_'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(yin)+'_'+str(fraction)+'_'+sim_len+'.eps')

pylab.show()
        

    



