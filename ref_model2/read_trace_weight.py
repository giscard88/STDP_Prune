import json
import pylab
import numpy

fp=open('trace_weights_0.0_0.0_1_0.2_20000.json','r')
no_top=json.load(fp)
fp.close()

fp=open('trace_weights_1.0_1.0_1_0.2_20000.json','r')
top=json.load(fp)
fp.close()


time=numpy.array(range(1,401))*50.0
pylab.figure(1)

pylab.plot(time, numpy.array(top['p_p'])-40.0,label='p_p')
pylab.plot(time, numpy.array(top['np_p'])-40.0,label='np_p')
pylab.title('top')
pylab.savefig('../figs/trace_weights_top-down_0.0_0.0_1_0.2_20000.eps')

pylab.figure(2)

pylab.plot(time, numpy.array(no_top['p_p'])-40.0,label='p_p')
pylab.plot(time, numpy.array(no_top['np_p'])-40.0,label='np_p')
pylab.title('no-top')
pylab.savefig('../figs2/trace_weights_nontop-down_0.0_0.0_1_0.2_20000.eps')
pylab.show()
