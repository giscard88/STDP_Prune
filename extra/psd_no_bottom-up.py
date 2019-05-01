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
                        help="Simulation time (in terms of clock time) (default: 500000.0, 10 sec)")

parser.add_argument("--second_lgn", type=float, default=0.2,
                        help="fraction of lgn (default: 0.2)")



args = parser.parse_args()


msd=range(1,21)
top_down_pyr=args.top_down_pyr
top_down_pv=args.top_down_pv
sim_len=str(int(args.simtime))
fraction=args.second_lgn


w_bu_pyr=40.0


lfp1=[]
lfp2=[]

#fn_comm='model'+model+':'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+sim_len+'_'+str(conn_ratio)+str(str_ratio)+'.json'

for yin in msd:

     
     fn_comm='no_bottom-up_'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(yin)+'_'+str(fraction)+'_'+sim_len+'.json'
                


     fp=open('lfp_'+fn_comm,'r')
     data=json.load(fp)
     fp.close()
     lfp=numpy.array(data['lfp'])
     f, Pxx_den = signal.welch(lfp, 1000.)
     idx=numpy.where((f>=0) & (f<100))[0]

     lfp1.append(Pxx_den[idx])

     fp=open('lfp2_'+fn_comm,'r')
     data=json.load(fp)
     fp.close()
     lfp=numpy.array(data['lfp'])
     f, Pxx_den = signal.welch(lfp, 1000.)
     idx=numpy.where((f>=0) & (f<100))[0]

     lfp2.append(Pxx_den[idx])

f=f[idx]

lfp1=numpy.array(lfp1)
lfp2=numpy.array(lfp2)

lfp_1=numpy.mean(lfp1,0)
lfp_2=numpy.mean(lfp2,0)

lfp1_mx=numpy.amax(lfp_1)
lfp2_mx=numpy.amax(lfp_2)

if lfp1_mx>lfp2_mx:
    mx=lfp1_mx
else:
    mx=lfp2_mx
pylab.plot(f,lfp_1/mx,label='pref')
pylab.plot(f,lfp_2/mx,label='nonpref')
pylab.legend()
pylab.savefig('../figs/'+'psd_no_bottom-up'+'_'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(fraction)+'_'+sim_len+'.eps')
pylab.show()
        

    



