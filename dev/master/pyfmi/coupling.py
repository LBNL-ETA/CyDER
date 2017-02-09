from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import os

def simulate_single_fmu():
    """Simulate one CYMDIST FMU.
        
    """
    cymdist=load_fmu("../../../../NO_SHARING/CYMDIST/BU0001.fmu", log_level=7)
    input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    input_values = [2520, 2520, 2520, 0.0, -120.0, 120.0]
    output_names = ['KWA', 'KWB', 'KWC', 'KVARA', 'KVARB', 'KVARC']
    output_node_names = ['800032440', '800032440', '800032440', 
                         '800032440', '800032440', '800032440']
    k=0
    for i in input_names:
        cymdist.set (i, input_values[k])
        k+=1
    opts=cymdist.simulate_options()
    res=cymdist.simulate(options=opts, 
                            start_time=0.0, 
                            final_time=1.0)
    print (cymdist.get_log())
    print ("This is the single simulation results " + str(res))
    

def simulate_multiple_fmus():
    """Simulate one CYMDIST FMU coupled to a dummy GridDyn FMU.
        
    """
    cymdist=load_fmu("../../../../NO_SHARING/CYMDIST/BU0001.fmu", log_level=7)
    gridyn=load_fmu("../../../../NO_SHARING/GridDyn/GridDyn.fmu", log_level=7)
    
    models = [cymdist, gridyn]
    connections = [(gridyn, "VMAG_A", cymdist, "VMAG_A"),
                   (gridyn, "VMAG_B", cymdist, "VMAG_B"),
                   (gridyn, "VMAG_C", cymdist, "VMAG_C"),
                   (gridyn, "VANG_A", cymdist, "VANG_A"),
                   (gridyn, "VANG_B", cymdist, "VANG_B"),
                   (gridyn, "VANG_C", cymdist, "VANG_C"),
                   (cymdist, "KWA_800032440", gridyn, "KWA_800032440"),
                   (cymdist, "KWB_800032440", gridyn, "KWB_800032440"),
                   (cymdist, "KWC_800032440", gridyn, "KWC_800032440"),
                   (cymdist, "KVARA_800032440", gridyn, "KVARA_800032440"),
                   (cymdist, "KVARB_800032440", gridyn, "KVARB_800032440"),
                   (cymdist, "KVARC_800032440", gridyn, "KVARC_800032440"),]
    
    coupled_simulation = Master (models, connections)
    opts=coupled_simulation.simulate_options()
    opts['step_size']=1.0
    opts['logging']=True
    print(str(opts))
    start = datetime.now()
    res=coupled_simulation.simulate(options=opts, 
                            start_time=0.0, 
                            final_time=1.0)
    end = datetime.now()
    print('Ran a coupled CYMDIST/GridDyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')
        
if __name__ == '__main__':
    #simulate_single_fmu()
    simulate_multiple_fmus()