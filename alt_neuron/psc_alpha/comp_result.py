import pylab
import numpy
import json
from psc_alpha_param import w_bu_pyr

reference_p_p=[]
reference_np_p=[]


reference_p_p_err=[]
reference_np_p_err=[]


for xin in range(1,21):
    fp=open('weights_psc_alpha1.0_1.0_'+str(xin)+'_0.2_20000.json','r')
    data=json.load(fp)
    temp=data['after_p_p']
    temp=numpy.array(temp)-w_bu_pyr
    reference_p_p.append(numpy.mean(temp))
    reference_p_p_err.append(numpy.std(temp))

    temp=data['after_np_p']
    temp=numpy.array(temp)-w_bu_pyr
    reference_np_p.append(numpy.mean(temp))
    reference_np_p_err.append(numpy.std(temp))
    fp.close()
  




xv=range(2,42,2)
xv=numpy.array(xv)
xv1=xv-0.25
xv2=xv+0.25


pylab.bar(xv1,reference_p_p,width=0.5,label='pref')
pylab.errorbar(xv1,reference_p_p,fmt='+',yerr=reference_p_p_err)

pylab.bar(xv2,reference_np_p,width=0.5,label='nonpref')
pylab.errorbar(xv2,reference_np_p,fmt='+',yerr=reference_np_p_err)
pylab.xticks([2,20,40],['1','10','20'])




pylab.legend()
pylab.savefig('/home/jung/revision/figures/weight_psc_alpha.eps')

pylab.show()



