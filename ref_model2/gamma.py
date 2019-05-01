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

parser.add_argument("--conn_ratio", type=float, default=1.0,
                        help="Ratio of bottom-up connection probability (default: 1.0)")

parser.add_argument("--str_ratio", type=float, default=1.0,
                        help="Ratio of bottom-up connection strengths (default: 1.0)")

parser.add_argument("--model", type=str, default='1',
                        help="select a model to be tested (1, 2 or 3)")
parser.add_argument("--second_lgn", type=float, default=0.2,
                        help="fraction of lgn (default: 0.2)")



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
     idx1=numpy.where((f>=0) & (f<30))[0]
     idx2=numpy.where((f>=30) & (f<60))[0]
     lfp_b.append(numpy.sum(Pxx_den[idx1]))
     lfp_g.append(numpy.sum(Pxx_den[idx2]))

    


     #pylab.semilogy(f,Pxx_den)
     #pylab.xlim([0,100])

pylab.subplot(2,1,1)
plot_x=numpy.array(lfp_b)
plot_x=plot_x/numpy.amax(plot_x)
pylab.scatter(plot_x,p_p_w,label='pref')
pylab.scatter(plot_x,np_p_w,label='nonpref')
pylab.title('beta (0-30)')
pylab.legend()
pylab.subplot(2,1,2)
pylab.title('gamma (30-60)')
plot_x=numpy.array(lfp_g)
plot_x=plot_x/numpy.amax(plot_x)
pylab.scatter(plot_x,p_p_w,label='pref')

pylab.scatter(plot_x,np_p_w,label='nonpref')
pylab.legend()

pylab.savefig('../figs2/gamma_correlation.eps')
pylab.show()
        

    



