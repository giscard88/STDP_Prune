import sys
import argparse

# set parameters for depressing synapse: 
h=0.1   # simulation step size (ms)

cpn=1

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='read out lfp signals from neuropixel')
parser.add_argument('--random_seed', type=int, default=1,
                    help='The random seed (default: 1)')

parser.add_argument("--top_down_pv", type=float, default=1.0,
                        help="Scale of top-down signals to pv (default: 1)")

parser.add_argument("--top_down_pyr", type=float, default=1.0,
                        help="Scale of top-down signals to pyr (default: 1)")

parser.add_argument("--simtime", type=float, default=10000.0,
                        help="Simulation time (in terms of clock time) (default: 10000.0, 10 sec)")


parser.add_argument("--show_graph", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Show graphs ")



parser.add_argument("--second_lgn", type=float, default=0.2,
                        help="fraction of lgn input to non-preferred column (default 0.2)")

args = parser.parse_args()

msd=args.random_seed
top_down_pyr=args.top_down_pyr
top_down_pv=args.top_down_pv
simtime=args.simtime
fraction=args.second_lgn
show_graph=args.show_graph


num_scale=5
pyr23_num=64*num_scale #200
pv23_num=16*num_scale #35


pyr4_num=64*num_scale #200
pv4_num=16*num_scale #35




Neuron_nums={'l23pyr':pyr23_num,'l23pv':pv23_num,
             'l4pyr':pyr4_num,'l4pv':pv4_num}







layers=['l23','l4']

#within layer
P_l23_l23={'pyr_pyr':0.05,'pyr_pv':0.5,'pv_pv':0.5,'pv_pyr':0.8}
P_l4_l4 = {'pyr_pyr':0.05,'pyr_pv':0.5,'pv_pv':0.5,'pv_pyr':0.8}

#across later
P_l23_l4={'pyr_pyr':0.0,'pyr_pv':0.0,'pv_pv':0.0,'pv_pyr':0.0}
P_l4_l23={'pyr_pyr':0.4,'pyr_pv':0.2,'pv_pv':0.0,'pv_pyr':0.0}



P_conn={'l23_l23':P_l23_l23, 'l23_l4':P_l23_l4, 'l4_l23':P_l4_l23, 'l4_l4':P_l4_l4}

V1_weights={'pyr_pyr':2.0,'pyr_pv':10.0,'pv_pyr':-12.0,'pv_pv':-8.0}
V1_exceptions={'l4pyr_l23pyr':5.0, 'l4pyr_l23pv':2.0} 

LM_weights=V1_weights
LM_exceptions={'l4pyr_l23pyr':3.0, 'l4pyr_l23pv':3.0,'l4pv_l4pyr':-15.0,'l4pv_l4pv':-2.0} 


Ext={'V1l23pyr':25.0,'V1l23pv':20.0,
     'V1l4pyr':25.0,'V1l4pv':20.0, 
     
     'LMl23pyr':25.0,'LMl23pv':20.0,
     'LMl4pyr':25.0,'LMl4pv':20.0,
     }






#probabiilty
P_pref_pref_pyr=0.05
P_pref_pref_pv=0.05
P_td_pyr=0.05
P_td_pv=0.05


#lgn inputs
w_lgn_pyr=20.0
w_lgn_pv=10.0


w_bu_pyr=20.0
w_bu_pv=20.0

#top-down weights


td_super_pyr=5.0 #6.0
td_super_pv=5.0 #10.0

#td_deep_pv=10.0



Pyr_params = {
            "tau_syn_ex": 1.0,
            "tau_syn_in":3.0
	    }


PV_params = {"tau_syn_ex": 1.0,
            "tau_syn_in":2.1

           }

