from pyfmi import load_fmu
from pyfmi.master import Master
from datetime import datetime
import numpy as np
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
        griddyn=load_fmu("../fmus/Tests/SecondModel.fmu", log_level=7)
        
        models = [cymdist, griddyn]
        connections = [(cymdist, "y", griddyn, "u"), 
                       (griddyn, "y", cymdist, "u")]
        
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
        print('Ran a coupled CYMDIST/griddyn simulation in ' +
              str((end - start).total_seconds()) + ' seconds.')

def simulate_single_griddyn_fmu():
    """Simulate one griddyn FMU.
        
    """
    griddyn=load_fmu("../../../../NO_SHARING/griddyn/Test/griddyn.fmu", log_level=7)
    # Set the inputs
    opts=griddyn.simulate_options()
    opts['ncp']=1.0
    print(str(opts))
    # Set the model name reference to be completed in Python API
    griddyn.set("power", 10)
    # Run simulation    
    start = datetime.now()
    res=griddyn.simulate(start_time=0.0, 
                        final_time=1, 
                        options=opts)    
    end = datetime.now()
    
    print('This is the time value ' + str(res['time']))
    print('This is the load value ' + str(res['load']))
    print('Ran a single griddyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')

def simulate_single_griddyn14bus_fmu():
    """Simulate one griddyn FMU.
        
    """   
    griddyn=load_fmu("../fmus/griddyn/griddyn14bus.fmu", log_level=7)
    input_current_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC', 
                           'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    input_current_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    output_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC', 
                    'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']

    # Set the inputs
    opts=griddyn.simulate_options()
    opts['ncp']=1.0

    # Set the flag to save the results
    for cnt, elem in enumerate(input_current_names):
        griddyn.set (elem, input_current_values[cnt])
        # Run simulation    
        
    start = datetime.now()
    res=griddyn.simulate(start_time=0.0, 
                         final_time=0.1, 
                         options=opts)    
    end = datetime.now()
    print('Ran a single CYMDIST simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')
    print("This is the value of the output Bus11_VA " 
          + str(res["Bus11_VAngleA"]))

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

def simulate_cymdist_griddyn14bus_fmus():
    """Simulate one CYMDIST FMU coupled to a griddyn FMU.
        
    """
    cymdist=load_fmu("../fmus/CYMDIST/CYMDIST.fmu", log_level=7)
    griddyn=load_fmu("../fmus/griddyn/griddyn14bus.fmu", log_level=7)
    
    models = [cymdist, griddyn]
    connections = [(griddyn, "Bus11_VA", cymdist, "VMAG_A"),
                   (griddyn, "Bus11_VB", cymdist, "VMAG_B"),
                   (griddyn, "Bus11_VC", cymdist, "VMAG_C"),
                   (griddyn, "Bus11_VAngleA", cymdist, "VANG_A"),
                   (griddyn, "Bus11_VAngleB", cymdist, "VANG_B"),
                   (griddyn, "Bus11_VAngleC", cymdist, "VANG_C"),
                   (cymdist, "IA", griddyn, "Bus11_IA"),
                   (cymdist, "IB", griddyn, "Bus11_IB"),
                   (cymdist, "IC", griddyn, "Bus11_IC"),
                   (cymdist, "IAngleA", griddyn, "Bus11_IAngleA"),
                   (cymdist, "IAngleB", griddyn, "Bus11_IAngleB"),
                   (cymdist, "IAngleC", griddyn, "Bus11_IAngleC"),]
    
    coupled_simulation = Master (models, connections)
    opts=coupled_simulation.simulate_options()
    print(opts)
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
    print('This is the voltage value' + str(res[cymdist]['VMAG_A']))
    print('This is the voltage value' + str(res[cymdist]['VMAG_B']))
    print('This is the voltage value' + str(res[cymdist]['VMAG_C']))
    end = datetime.now()
    
    print('Ran a coupled CYMDIST/griddyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')

def simulate_cymdist_griddyn_fmus():
    """Simulate one CYMDIST FMU coupled to a dummy griddyn FMU.
        
    """
    for i in [0.0, 0.1, 0.2, 0.3, 0.4, 0.4, 0.6, 0.7]:
        cymdist=load_fmu("../../../../NO_SHARING/CYMDIST/CYMDIST.fmu", log_level=7)
        griddyn=load_fmu("../../../../NO_SHARING/griddyn/griddyn.fmu", log_level=7)
        
        models = [cymdist, griddyn]
        connections = [(griddyn, "VMAG_A", cymdist, "VMAG_A"),
                       (griddyn, "VMAG_B", cymdist, "VMAG_B"),
                       (griddyn, "VMAG_C", cymdist, "VMAG_C"),
                       (griddyn, "VANG_A", cymdist, "VANG_A"),
                       (griddyn, "VANG_B", cymdist, "VANG_B"),
                       (griddyn, "VANG_C", cymdist, "VANG_C"),
                       (cymdist, "IA", griddyn, "IA"),
                       (cymdist, "IB", griddyn, "IB"),
                       (cymdist, "IC", griddyn, "IC"),
                       (cymdist, "IAngleA", griddyn, "IAngleA"),
                       (cymdist, "IAngleB", griddyn, "IAngleB"),
                       (cymdist, "IAngleC", griddyn, "IAngleC"),]
        
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
        
        print('Ran a coupled CYMDIST/griddyn simulation in ' +
              str((end - start).total_seconds()) + ' seconds.')
    
def simulate_single_cymdist_fmu2():
    """Simulate one CYMDIST FMU.
        
    """  
    griddyn_input_valref=[]
    griddyn_output_valref=[] 
    griddyn_output_values=[]
    
    cymdist_input_valref=[] 
    cymdist_output_valref=[]
    cymdist_output_values=[]  
    
    #for i in [0.0]:
    cymdist=load_fmu("../fmus/CYMDIST/CYMDIST.fmu", log_level=7)
    griddyn=load_fmu("../fmus/griddyn/griddyn14bus.fmu", log_level=7)
    step_size = 0.1
    cymdist.setup_experiment(start_time=0.0, stop_time=0.0)
    griddyn.setup_experiment(start_time=0.0, stop_time=0.8)
    
    # Define the inputs
    cymdist_input_voltage_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    cymdist_input_voltage_values = [2520, 2520, 2520, 0, -120, 120]
    cymdist_output_current_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    
    griddyn_input_current_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC', 
                       'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    griddyn_input_current_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    griddyn_output_voltage_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC', 
                'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']
    
    for cnt, elem in enumerate(griddyn_output_voltage_names):
        griddyn_output_valref.append(griddyn.get_variable_valueref(elem))
    for cnt, elem in enumerate(griddyn_input_current_names):
        griddyn_input_valref.append(griddyn.get_variable_valueref(elem))
    
    for cnt, elem in enumerate(cymdist_input_voltage_names):
        cymdist_input_valref.append(cymdist.get_variable_valueref(elem))    
    for cnt, elem in enumerate(cymdist_output_current_names):
        cymdist_output_valref.append(cymdist.get_variable_valueref(elem))  
    # Set the inputs
    # opts=cymdist.simulate_options()
    # opts['ncp']=1.0
    # Set the configuration file 
    con_val_ref = cymdist.get_variable_valueref("conFilNam")

    # Set the flag to save the results
    cymdist.set("save_to_file", 0)
    for cnt, elem in enumerate(cymdist_input_voltage_names):
        cymdist.set (elem, cymdist_input_voltage_values[cnt])
        # Run simulation    
        
    start = datetime.now()
    # Build path to configuration file
    path_config="Z:\\thierry\\proj\\cyder_repo\\jonathan\\CyDER\\web\\docker_django\\worker\\config.json"
    con_val_str = bytes(path_config, 'utf-8')
    cymdist.set_string([con_val_ref], [con_val_str])
    
    # Initialize the FMUs
    cymdist.initialize()
    griddyn.initialize()
    
    for time in np.arange(0, 0.8, 0.1):
        # Get the outputs from griddyn
        griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
        print("griddyn_output_values" + str(griddyn_output_values))
        
        print("cymdist_input_valref" + str(cymdist_input_valref))
        cymdist.set_real(cymdist_input_valref, griddyn_output_values)
        cymdist.do_step(current_t=time, step_size=step_size, new_step=0)
        cymdist_output_values = (cymdist.get_real(cymdist_output_valref))
        print("cymdist_output_values" + str(cymdist_output_values))
        
        griddyn.set_real( griddyn_input_valref, cymdist_output_values)
        griddyn.do_step(current_t=time, step_size=step_size, new_step=0)
    
    # Terminate FMUs
    cymdist.terminate()
    griddyn.terminate()
     
    end = datetime.now()
    print('Ran a single CYMDIST simulation in ' + 
          str((end - start).total_seconds()) + ' seconds.')
    print("This is the value of the output IA " + str(cymdist.get_real(cymdist.get_variable_valueref('IA'))) + ". IA is expected to be 277.6 A")
if __name__ == '__main__':
    #simulate_single_cymdist_fmu()
    #simulate_single_griddyn_fmu()
    #simulate_cymdist_griddyn_fmus()
    #simulate_algebraicloop_fmus()
    #simulate_cymdist_griddyn14bus_fmus()
    #simulate_single_griddyn14bus_fmu()
    simulate_single_cymdist_fmu2()
