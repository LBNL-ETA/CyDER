from __future__ import division
import argparse
import sys
from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import pdb

def simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time, save_to_file=0):
    """Simulate one CYMDIST FMU coupled to a dummy GridDyn FMU.
    """
    # Wire the Master
    cymdist = load_fmu("D:/Users/Jonathan/Documents/GitHub/cyder_tsn/NO_SHARING/CYMDIST/CYMDIST.fmu", log_level=7)
    gridyn = load_fmu("D:/Users/Jonathan/Documents/GitHub/cyder_tsn/NO_SHARING/GridDyn/GridDyn.fmu", log_level=7)
    models = [cymdist, gridyn]
    connections = [(gridyn, "VMAG_A", cymdist, "VMAG_A"),
                   (gridyn, "VMAG_B", cymdist, "VMAG_B"),
                   (gridyn, "VMAG_C", cymdist, "VMAG_C"),
                   (gridyn, "VANG_A", cymdist, "VANG_A"),
                   (gridyn, "VANG_B", cymdist, "VANG_B"),
                   (gridyn, "VANG_C", cymdist, "VANG_C"),
                   (cymdist, "IA", gridyn, "IA"),
                   (cymdist, "IB", gridyn, "IB"),
                   (cymdist, "IC", gridyn, "IC"),
                   (cymdist, "IAngleA", gridyn, "IAngleA"),
                   (cymdist, "IAngleB", gridyn, "IAngleB"),
                   (cymdist, "IAngleC", gridyn, "IAngleC"),]
    coupled_simulation = Master(models, connections)
    opts = coupled_simulation.simulate_options()
    opts['step_size'] = 0.1

    # Set the configuration file
    cymdist.set("save_to_file", save_to_file)
    con_val_str = bytes(configuration_filename, 'utf-8')
    con_val_ref = cymdist.get_variable_valueref("conFilNam")
    cymdist.set_string([con_val_ref], [con_val_str])

    # Launch simulation
    start = datetime.now()
    res = coupled_simulation.simulate(options=opts,
                                      start_time=start_time,
                                      final_time=end_time)
    end = datetime.now()
    print('Ran a coupled CYMDIST/GridDyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')

    # Create a normal result object (need to use Assimulo object?)
    result = {'cymdist': {}, 'griddyn': {}}
    for model_key, model in zip(['cymdist', 'griddyn'], [cymdist, gridyn]):
        for key in ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC',
                    'VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']:
            result[model_key][key] = res[model][key]
    return result

configuration_filename = "D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//config.json"
start_time = 0.0
end_time = 0.1
result = simulate_cymdist_gridyn_fmus(configuration_filename, start_time, end_time)
print(result)
pdb.set_trace()
