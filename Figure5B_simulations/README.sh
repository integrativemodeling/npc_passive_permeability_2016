#!/bin/bash

# Synopsis:
# =========
# This script runs the simulation of passive diffusion through the
# NPC using the parameters in config.pb.
#
# Pre-requirements:
# =================
# To run this script of passive diffusion simulations, you need to
# build IMP with the npctransport add-in, and change the variable
# $IMP_FOLDER to point to the IMP installation folder.
#
# The npctransport module could be downloaded from
# https://github.com/salilab/npctransport. The npctransport folder
# should be added to the "modules/" subfolder in the IMP source
# repository folder before building IMP. Otherwise, IMP should
# be built from source in standarad form.
#
#
# Output:
# =======
# The output is saved in the protobuf file output.pb and the snapshots
# from the simulation trajectories are saved in movie.rmf. The output
# file can be viewed in text format using the python script in
# $IMP_FOLDER/npctransport/utility/npc_show_output.py
#
# Sample output files are in the Output/ subfolder.
#
#
# Config.pb:
# ==========
# The script is using the configuration file config.pb, which was
# in turn created using the python script ./make_cfg.py, and its
# log output saved in config.txt (config.txt was saved only for reference).
# The file make_cfg.py could be modified to change the running parameters.
# To recreate config.pb, run:
#
# $IMP python ./make_cfg.py config.pb > config.txt
#

IMP_FOLDER=$HOME/imp_git/fast/
IMP=$IMP_FOLDER/setup_environment.sh
seed=`od -An -N4 -td4 /dev/random`
$IMP $IMP_FOLDER/module_bin/npctransport/fg_simulation --configuration config.pb --cylinder_nlayers 4 --output Output/output.pb --short_init_factor 0.5 --short_sim_factor 1.00 --conformations Output/movie.rmf --final_conformations Output/final_conformations.rmf --random_seed $seed
echo "FINISHED RUN"
