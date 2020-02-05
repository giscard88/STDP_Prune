import pylab
import numpy
import json
from dopamine_param import w_bu_pyr

V1_1=[]
V1_2=[]
V2_1=[]
V2_2=[]


sel_pop=1
if sel_pop==1:
    v1='1.0'
    v2='0.0'
else:
    v1='0.0'
    v2='1.0'

for xin in range(1,21):
    if sel_pop==1:
        fp=open('weights_multi_dopamine2-1-1.0_1.0_'+str(xin)+'_0.2_20000.json','r')
    else:
        fp=open('weights_multi_dopamine-2-1.0_1.0_'+str(xin)+'_0.2_20000.json','r') 
    data=json.load(fp)
    fp.close()
    temp=data['after_p_p']
    temp=numpy.array(temp)-w_bu_pyr
    v=V1_1.append(numpy.mean(temp))

    temp=data['after_np_p']
    temp=numpy.array(temp)-w_bu_pyr
    V1_2.append(numpy.mean(temp))

    temp=data['after_V2_1']
    temp=numpy.array(temp)-w_bu_pyr
    V2_1.append(numpy.mean(temp))

    temp=data['after_V2_2']
    temp=numpy.array(temp)-w_bu_pyr
    V2_2.append(numpy.mean(temp))

   





xv1=[0,1]
xv2=[4,5]


y1=[numpy.mean(V1_1),numpy.mean(V1_2)]
y1err=[numpy.std(V1_1),numpy.std(V1_2)]

y2=[numpy.mean(V2_1),numpy.mean(V2_2)]
y2err=[numpy.std(V2_1),numpy.std(V2_2)]



pylab.bar(xv1,y1,color='r',label='V1')
pylab.errorbar(xv1,y1,fmt='r+',yerr=y1err)

pylab.bar(xv2,y2,color='g',label='V2')
pylab.errorbar(xv2,y2,fmt='g+',yerr=y2err)


pylab.legend()
#pylab.savefig('/local2/STDP_prune_refined/figs/comp_result.eps')

pylab.show()



