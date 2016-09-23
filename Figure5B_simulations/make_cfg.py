#!/usr/bin/python
from IMP.npctransport import *
import sys
import math

# fetch params
# Usage: <cmd> <outfile>
outfile = sys.argv[1]
#print "[%s]" % outfile
kap_k=0.01
kap_range=9
kap_interaction_sites=2
# NOTE: site potential energy is kap_k*kap_range kCal/mol

def get_basic_config():
    config = Configuration()
    IMP.npctransport.set_default_configuration(config)
    config.statistics_fraction.lower=1.0
    #config.dump_interval=1
    config.interaction_k.lower=10
    config.interaction_range.lower=10
    # create_range(config.backbone_k, .2, 1, 10
    config.backbone_k.lower=1
    #config.time_step_factor.lower=0.3
    config.time_step_factor.lower=5
    #create_range(config.rest_length_factor, .5, 1, 10)
    config.excluded_volume_k.lower=20
    # non-specific attraction
    config.nonspecific_range.lower= 5.0
    config.nonspecific_k.lower= 0.015
    config.slack.lower = 30
    config.number_of_trials=1
    config.angular_D_factor.lower=0.3 #increased dynamic viscosity relative to water
    config.statistics_interval_ns=10
    ###
    #simulation bounding volumes:
    config.box_is_on.lower=1
    return config



# ********* MAIN: *********
config= get_basic_config()
#config.dump_interval_ns=0.01
#config.simulation_time_ns=5
config.dump_interval_ns=1000
config.simulation_time_ns=20000
config.box_is_on.lower=1
config.box_side.lower=1000
config.slab_is_on.lower=1
config.slab_thickness.lower=150
config.tunnel_radius.lower=135
#create_range(config.interaction_k, lb=.5, ub=15, steps=8, base=1)

# fg_cyto= IMP.npctransport.add_fg_type(config,
#                                  number_of_beads=12,
#                                  number=8,
#                                  radius=6,
#                                  interactions=1,
#                                  rest_length_factor = 1.5)
fg_middle= IMP.npctransport.add_fg_type(config,
                                 type_name="fg0",
                                 number_of_beads=45,
                                 number=32,
                                 radius=6,
                                 interactions=1,
                                 rest_length_factor = 1.5)
#create_range(fg_middle.number_of_beads,18,20,2)
# fg_nuclear= IMP.npctransport.add_fg_type(config,
#                                  number_of_beads=12,
#                                  number=8,
#                                  radius=6,
#                                  interactions=1,
#                                  rest_length_factor = 1.5)
#surface_area_ratio_to_R25 = math.pow( floaters_R / 25.0, 2 )
#kap_n_interactions = int( math.ceil ( 12 * surface_area_ratio_to_R25 ) )
#create_range(kaps.radius, lb = 10, ub = 30, steps = 5, base = 1)
nonspecifics={}
kaps={}
rrange=range(16,37,2)
for i in rrange:
    type_name="R%d" % i
    nonspecifics[i]= IMP.npctransport.add_float_type(config,
                                                  number=100,
                                                  radius=i,
                                                  type_name=type_name,
                                                  interactions=0)
    IMP.npctransport.add_interaction(config,
                                     name0="fg0",
                                     name1=type_name,
                                     interaction_k=0,
                                     interaction_range=0)
kap_R=20
kap_name="kap%d" % kap_R
kaps[0]= IMP.npctransport.add_float_type(config,
                                         number=1,
                                         radius=kap_R,
                                         type_name=kap_name,
                                         interactions=kap_interaction_sites)
IMP.npctransport.add_interaction(config,
                                 name0="fg0",
                                 name1=kap_name,
                                 interaction_k=kap_k,
                                 interaction_range=kap_range)


interactionFG_FG= IMP.npctransport.add_interaction(config,
                                                   name0= "fg0",
                                                   name1= "fg0",
                                                   interaction_k=0.01,
                                                   interaction_range= 6)
#create_range(interactionFG_FG.interaction_k, lb = 0.01, ub = 10, steps = 7, base = 2)
## internal FG-FG
#for i in range(3):
#    for j in range(i,3):
#        interactionFG_FG= IMP.npctransport.add_interaction(config,
#                                                           name0= "fg%d" % i,
#                                                           name1= "fg%d" % j,
#                                                           interaction_k= float(fgs_k),
#                                                           interaction_range= 2)

# dump to file
f=open(outfile, "wb")
f.write(config.SerializeToString())
print config
