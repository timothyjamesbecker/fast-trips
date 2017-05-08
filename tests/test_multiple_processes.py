import os

import pytest

import fasttrips
from fasttrips import Run


def test_multiple_processes():

    EXAMPLES_DIR   = os.path.join(os.getcwd(),"Examples","test_scenario")

    INPUT_NETWORKS = os.path.join(EXAMPLES_DIR,"network")
    INPUT_DEMAND   = os.path.join(EXAMPLES_DIR,"demand_reg")
    OUTPUT_DIR     = os.path.join(EXAMPLES_DIR,"output")

    r = Run.run_fasttrips(
        input_net_dir    = INPUT_NETWORKS,
        input_demand_dir = INPUT_DEMAND,
        run_config       = os.path.join(INPUT_DEMAND,"config_ft.txt"),
        input_weights    = os.path.join(INPUT_DEMAND,"pathweight_ft.txt"),
        output_dir       = OUTPUT_DIR,
        output_folder    = "test_2processes",
        pathfinding_type = "stochastic",
        number_of_processes   = 2,
        iters            = 1,
        dispersion       = 0.50 )
    
    assert r["passengers_arrived"] > 0
