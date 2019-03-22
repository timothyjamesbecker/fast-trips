#!/usr/bin/env python

import argparse
import os
from fasttrips import Run

if __name__ == '__main__':
    des = """command line script for FastTrips simulation tool"""
    parser = argparse.ArgumentParser(description=des, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-N', '--network_dir',type=str,help='\t[None]')
    parser.add_argument('-D', '--demand_dir', type=str, help='\t[None]')
    parser.add_argument('-C','--config_dir',type=str,help='\t[None]')
    parser.add_argument('-O', '--out_dir', type=str, help='\t[None]')
    parser.add_argument('--no_stochastic',action='store_true',help='\t[False]')
    parser.add_argument('--no_capacity', action='store_true', help='\t[False]')
    parser.add_argument('--no_overlap_split', action='store_true', help='\t[False]')
    parser.add_argument('--global_iters',type=int,help='\t[False]')
    parser.add_argument('--pf_iters',type=int,help='\t[False]')
    parser.add_argument('--dispersion',type=float,help='\t[1.0]')
    parser.add_argument('--conversion_factor',type=int,help='\t[10]')
    parser.add_argument('--cpus',type=int,help='\tNumber of processes to generate[1]')
    args = parser.parse_args()

    if args.network_dir is not None:
        network_dir =  args.network_dir
    else: raise IOError
    if args.demand_dir is not None:
        demand_dir =  args.demand_dir
    else: raise IOError
    if args.config_dir is not None and \
            os.path.exists(args.config_dir+'/config_ft.txt') and \
            os.path.exists(args.config_dir+'/pathweight_ft.txt') and \
            os.path.exists(args.config_dir+'/config_ft.py'):
        config_dir = args.config_dir
    else: raise IOError
    if args.out_dir is not None:
        out_dir = args.out_dir
    else: raise IOError

    if args.global_iters is not None:        global_iters = args.global_iters
    else:                                    global_iters = 1
    if args.pf_iters is not None:            pf_iters = args.pf_iters
    else:                                    pf_iters = 10
    if args.dispersion is not None:          disp = args.dispersion
    else:                                    disp = 1.0
    if args.conversion_factor is not None:   factor = args.conversion_factor
    else:                                    factor = 10
    if args.cpus is not None:                cpus = args.cpus
    else:                                    cpus = 1
    if args.no_stochastic:                   pf_type = "deterministic"
    else:                                    pf_type = "stochastic"

    Run.run_fasttrips(input_network_dir       = network_dir,
                      input_demand_dir        = demand_dir,
                      run_config              = config_dir+'/config_ft.txt',
                      input_weights           = config_dir+'/pathweight_ft.txt',
                      output_dir              = out_dir,
                      output_folder           = out_dir,
                      user_class_function     = "user_class",
                      input_functions         = config_dir+'/config_ft.py',
                      overlap_variable        = "count",
                      pathfinding_type        = pf_type,
                      overlap_split_transit   = not args.no_overlap_split,
                      iters                   = global_iters,
                      pf_iters                = pf_iters,
                      dispersion              = disp,
                      utils_conversion_factor = factor,
                      capacity                = not args.no_capacity)