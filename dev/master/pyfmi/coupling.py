from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import os

def simulate_algebraicloop_fmus():
    """Simulate two dummy FMUs which form an algebraic loop.
    The first FMU implements y = u (u is the input, y is the output)
    The second FMU implements y = u*u (u is the input, y is the output)
    The coupled system connects the output of the first model
    with the input of the second model, and the output of the 
    second model to the input of the first model.
    This forms an algebraic loop which leads to the equation u = u*u
        
    """
    for i in [0.0, 0.1]:
        cymdist=load_fmu("../fmus/Tests/FirstModel.fmu", log_level=7)
        gridyn=load_fmu("../fmus/Tests/SecondModel.fmu", log_level=7)
        
        models = [cymdist, gridyn]
        connections = [(cymdist, "y", gridyn, "u"), 
                       (gridyn, "y", cymdist, "u")]
        
        coupled_simulation = Master (models, connections)
        
        opts=coupled_simulation.simulate_options()
        opts['step_size']=0.1
        opts['logging']=True
    
        start = datetime.now()
        # Run simulation
        res=coupled_simulation.simulate(options=opts, 
                                start_time=0.0, 
                                final_time=1.0)
        end = datetime.now()
        print('Ran a coupled CYMDIST/GridDyn simulation in ' +
              str((end - start).total_seconds()) + ' seconds.')

def simulate_single_gridyn_fmu():
    """Simulate one GridDyn FMU.
        
    """
    gridyn=load_fmu("../../../../NO_SHARING/GridDyn/Test/griddyn.fmu", log_level=7)
    # Set the inputs
    opts=gridyn.simulate_options()
    opts['ncp']=1.0
    print(str(opts))
    # Set the model name reference to be completed in Python API
    gridyn.set("power", 10)
    # Run simulation    
    start = datetime.now()
    res=gridyn.simulate(start_time=0.0, 
                        final_time=1, 
                        options=opts)    
    end = datetime.now()
    
    print('This is the time value ' + str(res['time']))
    print('This is the load value ' + str(res['load']))
    print('Ran a single GridDyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')

def simulate_single_cymdist_fmu():
    """Simulate one CYMDIST FMU.
        
    """   
    for i in [0.0]:
        cymdist=load_fmu("../../../../NO_SHARING/CYMDIST/BU0001.fmu", log_level=7)
        input_voltage_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
        input_voltage_values = [2520, 2520, 2520, 0, -120, 120]
        output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']
    
        # Set the inputs
        opts=cymdist.simulate_options()
        opts['ncp']=1.0
        # Set the configuration file 
        con_val_ref = cymdist.get_variable_valueref("conFilNam")
    
        # Set the flag to save the results
        cymdist.set("save_to_file", 0)
        for cnt, elem in enumerate(input_voltage_names):
            cymdist.set (elem, input_voltage_values[cnt])
            # Run simulation    
            
        start = datetime.now()
        #Build path to configuration file
        path_config="Z:\\thierry\\proj\\cyder_repo\\cyder\\dev\\master\\pyfmi\\config" \
                    + str(int(i))+".json"
        con_val_str = bytes(path_config, 'utf-8')
        cymdist.set_string([con_val_ref], [con_val_str])
        res=cymdist.simulate(start_time=0.0 + i, 
                             final_time=0.1 + i, 
                             options=opts)    
        end = datetime.now()
        print('Ran a single CYMDIST simulation in ' +
              str((end - start).total_seconds()) + ' seconds.')
        print("This is the value of the output IA " 
              + str(res["IA"] + ". IA is expected to be 277.6 A"))

def simulate_cymdist_gridyn14bus_fmus():
    """Simulate one CYMDIST FMU coupled to a dummy GridDyn FMU.
        
    """
    for i in [0.0, 0.1, 0.2, 0.3, 0.4, 0.4, 0.6, 0.7]:
        cymdist=load_fmu("../fmus/CYMDIST/CYMDIST.fmu", log_level=7)
        gridyn=load_fmu("../fmus/GridDyn/griddyn14bus.fmu", log_level=7)
        
        models = [cymdist, gridyn]
        connections = [(gridyn, "Bus11_VA", cymdist, "VMAG_A"),
                       (gridyn, "Bus11_VB", cymdist, "VMAG_B"),
                       (gridyn, "Bus11_VC", cymdist, "VMAG_C"),
                       (gridyn, "Bus11_VAngleA", cymdist, "VANG_A"),
                       (gridyn, "Bus11_VAngleB", cymdist, "VANG_B"),
                       (gridyn, "Bus11_VAngleC", cymdist, "VANG_C"),
                       (cymdist, "IA", gridyn, "Bus11_IA"),
                       (cymdist, "IB", gridyn, "Bus11_IB"),
                       (cymdist, "IC", gridyn, "Bus11_IC"),
                       (cymdist, "IAngleA", gridyn, "Bus11_IAngleA"),
                       (cymdist, "IAngleB", gridyn, "Bus11_IAngleB"),
                       (cymdist, "IAngleC", gridyn, "Bus11_IAngleC"),]
        
        coupled_simulation = Master (models, connections)
        opts=coupled_simulation.simulate_options()
        print(opts)
        opts['step_size']=0.1
        
        # Set the configuration file 
        con_val_ref = cymdist.get_variable_valueref("conFilNam")

        # Run simulation
        start = datetime.now()
#         cymdist.set("save_to_file", 0)
#         #Build path to configuration file
#         path_config="Z:\\thierry\\proj\\cyder_repo\\jonathan\\CyDER\\web\\docker_django\\worker\\config.json"
#         con_val_str = bytes(path_config, 'utf-8')
#         cymdist.set_string([con_val_ref], [con_val_str])
#         res=coupled_simulation.simulate(options=opts, 
#                                 start_time=0.0, 
#                                 final_time=0.1)
#       print('This is the voltage value' + str(res[cymdist]['VMAG_A']))
        end = datetime.now()
        
        print('Ran a coupled CYMDIST/GridDyn simulation in ' +
              str((end - start).total_seconds()) + ' seconds.')

def simulate_cymdist_gridyn_fmus():
    """Simulate one CYMDIST FMU coupled to a dummy GridDyn FMU.
        
    """
    for i in [0.0, 0.1, 0.2, 0.3, 0.4, 0.4, 0.6, 0.7]:
        cymdist=load_fmu("../../../../NO_SHARING/CYMDIST/CYMDIST.fmu", log_level=7)
        gridyn=load_fmu("../../../../NO_SHARING/GridDyn/GridDyn.fmu", log_level=7)
        
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
        
        coupled_simulation = Master (models, connections)
        opts=coupled_simulation.simulate_options()
        opts['step_size']=0.1
        
        # Set the configuration file 
        con_val_ref = cymdist.get_variable_valueref("conFilNam")

        # Run simulation
        start = datetime.now()
        cymdist.set("save_to_file", 0)
        #Build path to configuration file
        path_config="Z:\\thierry\\proj\\cyder_repo\\jonathan\\CyDER\\web\\docker_django\\worker\\config.json"
        con_val_str = bytes(path_config, 'utf-8')
        cymdist.set_string([con_val_ref], [con_val_str])
        res=coupled_simulation.simulate(options=opts, 
                                start_time=0.0, 
                                final_time=0.1)
#         print('This is the voltage value' + str(res[cymdist]['VMAG_A']))
        end = datetime.now()
        
        print('Ran a coupled CYMDIST/GridDyn simulation in ' +
              str((end - start).total_seconds()) + ' seconds.')
        
if __name__ == '__main__':
    #simulate_single_cymdist_fmu()
    #simulate_single_gridyn_fmu()
    #simulate_cymdist_gridyn_fmus()
    #simulate_algebraicloop_fmus()
    simulate_cymdist_gridyn14bus_fmus()
