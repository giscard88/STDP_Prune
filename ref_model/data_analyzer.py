import pylab
import json
import argparse
import numpy
from collections import defaultdict
import os
#from network_param import w_bu_pyr

w_bu_pyr=40.0

parser = argparse.ArgumentParser(description='read out lfp signals from neuropixel')

parser.add_argument("--var", type=str, default='top_down_pyr',
                        help="bottom-up connection changes w.r.t. X (default: top_down_pyr")

parser.add_argument("--top_down_pv", type=float, default=1.0,
                        help="Scale of top-down signals to pv (default: 1)")

parser.add_argument("--top_down_pyr", type=float, default=1.0,
                        help="Scale of top-down signals to pyr (default: 1)")

parser.add_argument("--simtime", type=float, default=20000.0,
                        help="Simulation time (in terms of clock time) (default: 50000.0, 10 sec)")

parser.add_argument("--second_lgn", type=float, default=0.2,
                        help="fraction of lgn input to non-preferred column (default 0.2)")


args = parser.parse_args()


#msd=range(1,31)
top_down_pyr=args.top_down_pyr
top_down_pv=args.top_down_pv
sim_len=str(int(args.simtime))

fraction=args.second_lgn

axis=args.var

if axis=='top_down_pyr':
    test=[0.0,0.25,0.5,0.75,1.0,1.25,1.5]
    msd=range(1,21)

elif axis=='top_down_pv':
    test=[0.0,0.25,0.5,0.75,1.0,1.25,1.5]
    print (test)
    msd=range(1,21)

elif axis=='second_lgn':
    test=[0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975]
    print (test)
    msd=range(1,21)


p_conns=defaultdict(list)
np_conns=defaultdict(list)


#fn_comm='model'+model+':'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+sim_len+'_'+str(conn_ratio)+str(str_ratio)+'.json'
for xin in test:
    for yin in msd:
        if axis=='top_down_pyr':
             
             fn_comm=str(xin)+'_'+str(top_down_pv)+'_'+str(yin)+'_'+str(fraction)+'_'+sim_len+'.json'
                



        if axis=='top_down_pv':
           
             fn_comm=str(top_down_pyr)+'_'+str(xin)+'_'+str(yin)+'_'+str(fraction)+'_'+sim_len+'.json'


        if axis=='second_lgn':
 
             fn_comm=str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(yin)+'_'+str(xin)+'_'+sim_len+'.json'




        fp=open('weights_'+fn_comm,'r')
        data=json.load(fp)
        temp=data['after_p_p']
        temp=numpy.array(temp)-w_bu_pyr
        p_conns[str(xin)].append(numpy.mean(temp))

        temp=data['after_np_p']
        temp=numpy.array(temp)-w_bu_pyr
        np_conns[str(xin)].append(numpy.mean(temp))

y1=[]
y2=[]
y1e=[]
y2e=[]
xv1=[]
xv2=[]
base=1
for xi, xin in enumerate(test):
    y1.append(numpy.mean(p_conns[str(xin)]))
    y1e.append(numpy.std(p_conns[str(xin)]))
    y2.append(numpy.mean(np_conns[str(xin)]))
    y2e.append(numpy.std(np_conns[str(xin)]))
    xv1.append(xi+1-0.125)
    xv2.append(xi+1+0.125)

print xv1,xv2
print y1
print y2

test_numpy=numpy.array(test)

if axis=='top_down_pyr':
    test_numpy=test_numpy*15.0

elif axis=='top_down_pv':
    test_numpy=test_numpy*20.0

pylab.bar(xv1,y1,width=0.25)
pylab.errorbar(xv1,y1,yerr=y1e,fmt='o')
pylab.bar(xv2,y2,width=0.25)
pylab.errorbar(xv2,y2,yerr=y2e,fmt='o')
pylab.xticks(range(1,len(xv1)+1),test_numpy)

if axis=='second_lgn':
    from scipy import stats
    d1=p_conns[str(1.0)]
    d2=np_conns[str(1.0)]
    t,p=stats.ttest_ind(d1,d2)
    print (d1)
    print (d2)
    print (p)
    

pylab.savefig('../figs/'+axis+'_'+str(args.top_down_pyr)+'_'+str(args.top_down_pv)+'_'+str(args.second_lgn)+'.eps')
pylab.show()    
     


        
        
     


    






