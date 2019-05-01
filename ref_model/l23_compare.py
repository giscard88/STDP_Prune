import sys
import argparse
import json
import numpy
import pylab


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='plot spikes')

parser.add_argument('--random_seed', type=int, default=1,
                    help='The random seed (default: 1)')

parser.add_argument("--top_down_pv", type=float, default=1.0,
                        help="Scale of top-down signals to pv (default: 1)")

parser.add_argument("--top_down_pyr", type=float, default=1.0,
                        help="Scale of top-down signals to pyr (default: 1)")

parser.add_argument("--simtime", type=float, default=20000.0,
                        help="Simulation time (in terms of clock time) (default: 20000.0, 2 sec)")

parser.add_argument("--second_lgn", type=float, default=0.2,
                        help="fraction of lgn input to non-preferred column (default 0.2)")

args = parser.parse_args()

msd=args.random_seed
top_down_pyr=args.top_down_pyr
top_down_pv=args.top_down_pv
sim_len=str(int(args.simtime))

fraction=args.second_lgn

fn_comm=str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+str(fraction)+'_'+sim_len+'.json'

fp=open('spikes_'+fn_comm,'r')
spikes=json.load(fp)
fp.close()

fp=open('lfp_'+fn_comm,'r')
lfp_data=json.load(fp)
fp.close()

layers=['l23','l4']
colors={'pyr':'r','pv':'b'}
celltypes=['pyr','pv']
sub_fig_num=len(layers)



pylab.subplot(3,1,1)
for yin in celltypes:
        spks=spikes['V1_2l23'+yin]
        pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
        pylab.xlim([1320,1360])
        pylab.title('V1_2')
pylab.subplot(3,1,2)
for yin in celltypes:
        spks=spikes['LMl4'+yin]
        pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
        pylab.xlim([1320,1360])
        pylab.title('LM')
pylab.subplot(3,1,3)
for yin in celltypes:
        spks=spikes['V1_1l23'+yin]
        pylab.scatter(spks[0],spks[1],c=colors[yin], s=5, edgecolors='none')
        pylab.xlim([1320,1360])
        pylab.title('V1_1')
pylab.savefig('../figs/l23_compare'+str(top_down_pyr)+'_'+str(top_down_pv)+'_'+str(msd)+'_'+str(fraction)+'_'+sim_len+'.eps')



pylab.show()






