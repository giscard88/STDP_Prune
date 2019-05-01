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

parser.add_argument("--simtime", type=float, default=500000.0,
                        help="Simulation time (in terms of clock time) (default: 500000.0, 10 sec)")

parser.add_argument("--conn_ratio", type=float, default=1.0,
                        help="Ratio of bottom-up connection probability (default: 1.0)")

parser.add_argument("--str_ratio", type=float, default=1.0,
                        help="Ratio of bottom-up connection strengths (default: 1.0)")

parser.add_argument("--model", type=str, default='1',
                        help="select a model to be tested (1, 2 or 3)")




args = parser.parse_args()


msd=range(1,31)
top_down_pyr=args.top_down_pyr
top_down_pv=args.top_down_pv
sim_len=str(int(args.simtime))
conn_ratio=args.conn_ratio
model=args.model
str_ratio=args.str_ratio


w_bu_pyr=40.0

p_p_w=[]
np_p_w=[]
lfp_b=[]
lfp_g=[]

#fn_comm='model'+model+':'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+sim_len+'_'+str(conn_ratio)+str(str_ratio)+'.json'

for yin in msd:

     if model=='3' or model=='2':
         fn_comm='model'+model+':'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(yin)+'_'+sim_len+'_'+str(conn_ratio)+str(str_ratio)+'.json'
                
     else: 
         fn_comm='model'+model+':'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(yin)+'_'+sim_len+'_'+str(conn_ratio)+'.json'

     
     fp=open('weights_'+fn_comm,'r')
     data=json.load(fp)
     fp.close()
     temp=data['after_p_p']
     temp=numpy.array(temp)-w_bu_pyr
     p_p_w.append(numpy.mean(temp))

     temp=data['after_np_p']
     temp=numpy.array(temp)-w_bu_pyr
     np_p_w.append(numpy.mean(temp))
     

     fp=open('lfp_'+fn_comm,'r')
     data=json.load(fp)
     fp.close()
     lfp=numpy.array(data['lfp'])
     f, Pxx_den = signal.welch(lfp, 1000.)
     idx1=numpy.where((f>=5) & (f<20))[0]
     idx2=numpy.where((f>=30) & (f<60))[0]
     lfp_b.append(numpy.sum(Pxx_den[idx1]))
     lfp_g.append(numpy.sum(Pxx_den[idx2]))

    


     #pylab.semilogy(f,Pxx_den)
     #pylab.xlim([0,100])

pylab.subplot(2,2,1)
pylab.scatter(lfp_b,p_p_w)
pylab.subplot(2,2,2)
pylab.scatter(lfp_g,p_p_w)
pylab.subplot(2,2,3)
pylab.scatter(lfp_b,np_p_w)
pylab.subplot(2,2,4)
pylab.scatter(lfp_g,np_p_w)

pylab.show()
        

    



