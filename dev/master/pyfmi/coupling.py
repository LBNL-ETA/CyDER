from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import os

def simulate_single_fmu():
    """Simulate one CYMDIST FMU.
        
    """
    cymdist=load_fmu("../../../../NO_SHARING/CYMDIST/HL0004.fmu", log_level=0)
    input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C']
    input_values = [7287, 7299, 7318, 7272, 2118, 6719, -284, -7184, 3564]
    output_names = ['voltage_A', 'voltage_B', 'voltage_C']
    output_node_names = ['HOLLISTER_2104', 'HOLLISTER_2104', 'HOLLISTER_2104']
    k=0
    for i in input_names:
        cymdist.set (i, input_values[k])
        k+=1
    opts=cymdist.simulate_options()
    opts['solver']='CVode'
    opts['step_size']=1
    res=cymdist.simulate(options=opts, 
                            start_time=0.0, 
                            final_time=1.0)
    print (cymdist.get_log())
    print ("This is the single simulation results " + str(res))
    

def simulate_multiple_fmus():
    """Simulate one CYMDIST FMU coupled to a dummy GridDyn FMU.
        
    """
    cymdist=load_fmu("../../../../NO_SHARING/CYMDIST/HL0004.fmu", log_level=0)
    gridyn=load_fmu("../../../../NO_SHARING/GridDyn/GridDyn.fmu", log_level=0)
    
    models = [cymdist, gridyn]
    connections = [(gridyn, "VMAG_A", cymdist, "VMAG_A"),
                   (gridyn, "VMAG_B", cymdist, "VMAG_B"),
                   (gridyn, "VMAG_C", cymdist, "VMAG_C"),
                   (gridyn, "P_A", cymdist, "P_A"),
                   (gridyn, "P_B", cymdist, "P_B"),
                   (gridyn, "P_C", cymdist, "P_C"),
                   (gridyn, "Q_A", cymdist, "Q_A"),
                   (gridyn, "Q_B", cymdist, "Q_B"),
                   (gridyn, "Q_C", cymdist, "Q_C"),
                   (cymdist, "voltage_A_HOLLISTER_2104", gridyn, "voltage_A_HOLLISTER_2104"),
                   (cymdist, "voltage_B_HOLLISTER_2104", gridyn, "voltage_B_HOLLISTER_2104"),
                   (cymdist, "voltage_C_HOLLISTER_2104", gridyn, "voltage_C_HOLLISTER_2104"),]
    
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