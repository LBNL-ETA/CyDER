from pyfmi import load_fmu
from pyfmi.master import Master
from matplotlib.pyplot import plot, draw, show
import matplotlib.pyplot as plt
import time as t
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
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 0.1
    step_size = 0.1
    
    cymdist=load_fmu("../fmus/Tests/FirstModel.fmu", log_level=7)
    griddyn=load_fmu("../fmus/Tests/SecondModel.fmu", log_level=7)
    
    models = [cymdist, griddyn]
    connections = [(cymdist, "y", griddyn, "u"), 
                   (griddyn, "y", cymdist, "u")]
    
    coupled_simulation = Master (models, connections)
    
    opts=coupled_simulation.simulate_options()
    opts['step_size']=step_size
    opts['logging']=True

    start = datetime.now()
    # Run simulation
    res=coupled_simulation.simulate(options=opts, 
                            start_time=start_time, 
                            final_time=stop_time)
    end = datetime.now()
    print('Ran a coupled CYMDIST/griddyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')

def simulate_single_griddyn_fmu():
    """Simulate one griddyn FMU.
        
    """
    
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 0.1
    
    griddyn=load_fmu("../../../../NO_SHARING/griddyn/Test/griddyn.fmu", log_level=7)
    # Set the inputs
    opts=griddyn.simulate_options()
    opts['ncp']=1.0

    # Set the model name reference to be completed in Python API
    griddyn.set("power", 10)
    # Run simulation    
    start = datetime.now()
    res=griddyn.simulate(start_time=start_time, 
                        final_time=stop_time, 
                        options=opts)    
    end = datetime.now()
    
    print('This is the time value ' + str(res['time']))
    print('This is the load value ' + str(res['load']))
    print('Ran a single griddyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')

def simulate_single_griddyn14bus_fmu():
    """Simulate one griddyn FMU.
        
    """   
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 0.1
    
    griddyn=load_fmu("../fmus/griddyn/griddyn14bus.fmu", log_level=7)
    griddyn_input_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC', 
                           'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    griddyn_input_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    griddyn_output_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC', 
                    'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']

    griddyn_input_valref = []
    # Get the value references of griddyn inputs
    for elem in griddyn_input_names:
        griddyn_input_valref.append(griddyn.get_variable_valueref(elem))
    
    # Set the inputs
    opts=griddyn.simulate_options()
    opts['ncp']=1.0

    # Set the inputs of GridDyn
    griddyn.set_real (griddyn_input_valref, griddyn_input_values)
    
    # Run simulation        
    start = datetime.now()
    res=griddyn.simulate(start_time=start_time, 
                         final_time=stop_time, 
                         options=opts)    
    end = datetime.now()
    print('Ran a single CYMDIST simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')
    print("This is the value of the output Bus11_VA " 
          + str(res["Bus11_VA"]))

def simulate_single_cymdist_fmu():
    """Simulate one CYMDIST FMU.
        
    """ 
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 0.1
    
    # Path to configuration file
    path_config="Z:\\thierry\\proj\\cyder_repo\\jonathan\\CyDER\\web\\docker_django\\worker\\config.json"
    con_val_str = bytes(path_config, 'utf-8')  

    cymdist=load_fmu("../fmus/CYMDIST/CYMDIST.fmu", log_level=7)
    cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    cymdist_input_values = [2520, 2520, 2520, 0, -120, 120]
    #cymdist_input_values = [ -1.45600000e+47,  -1.45600000e+47,  -1.45600000e+47,  -1.45600000e+47,
    #                        -1.45600000e+47,  -1.45600000e+47]
    cymdist_output_names = ['IA', 'IAngleA', 'IB', 'IAngleB', 'IC', 'IAngleC']
    
    cymdist_input_valref = []
        # Get the value references of cymdist inputs
    for elem in cymdist_input_names:
        cymdist_input_valref.append(cymdist.get_variable_valueref(elem))
    
    # Set the inputs
    opts=cymdist.simulate_options()
    opts['ncp']=1.0
    # Set the configuration file 
    con_val_ref = cymdist.get_variable_valueref("conFilNam")

    # Set the flag to save the results
    cymdist.set("save_to_file", 0)

    # Set the cymdist inputs
    cymdist.set_real(cymdist_input_valref, cymdist_input_values)
    cymdist.set_string([con_val_ref], [con_val_str])
    
    # Run simulation        
    start = datetime.now()
    res=cymdist.simulate(start_time=start_time, 
                         final_time=stop_time, 
                         options=opts)    
    end = datetime.now()
    print('Ran a single CYMDIST simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')
    print("This is the value of the output IA " 
          + str(res["IA"]) + ". IA is expected to be 277.6 A")

def simulate_cymdist_griddyn14bus_fmus():
    """Simulate one CYMDIST FMU coupled to a griddyn FMU.
        
    """
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 0.1
    step_size = 0.1

    # Path to configuration file
    path_config="Z:\\thierry\\proj\\cyder_repo\\jonathan\\CyDER\\web\\docker_django\\worker\\config.json"
    con_val_str = bytes(path_config, 'utf-8')
    
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
    
    # Create coupled simulation
    coupled_simulation = Master (models, connections)
    
    # Set the options
    opts=coupled_simulation.simulate_options()
    opts['step_size']=step_size
    
    # Get the configuration file 
    con_val_ref = cymdist.get_variable_valueref("conFilNam")

    cymdist.set("save_to_file", 0)
    cymdist.set_string([con_val_ref], [con_val_str])
    
    # Run simulation
    start = datetime.now()
    res=coupled_simulation.simulate(options=opts, 
                            start_time=start_time, 
                            final_time=stop_time)
    end = datetime.now()
    print('This is the voltage value (VMAG_A) in Cymdist' + str(res[cymdist]['VMAG_A']))
    print('This is the current value (IA) in Cymdist' + str(res[cymdist]['IA']))
    print('Ran a coupled CYMDIST/griddyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')

def simulate_cymdist_griddyn_fmus():
    """Simulate one CYMDIST FMU coupled to a dummy griddyn FMU.
        
    """
    
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 0.1
    step_size = 0.1

    # Path to configuration file
    path_config="Z:\\thierry\\proj\\cyder_repo\\jonathan\\CyDER\\web\\docker_django\\worker\\config.json"
    con_val_str = bytes(path_config, 'utf-8')

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
    opts['step_size']=step_size
    
    # Get the configuration file 
    con_val_ref = cymdist.get_variable_valueref("conFilNam")

    cymdist.set("save_to_file", 0)
    cymdist.set_string([con_val_ref], [con_val_str])
    
    # Run simulation
    start = datetime.now()
    res=coupled_simulation.simulate(options=opts, 
                            start_time=start_time, 
                            final_time=stop_time)
    end = datetime.now()
    
    print('This is the voltage value (VMAG_A) in Cymdist' + str(res[cymdist]['VMAG_A']))
    print('This is the current value (IA) in Cymdist' + str(res[cymdist]['IA']))
    print('Ran a coupled CYMDIST/griddyn simulation in ' +
          str((end - start).total_seconds()) + ' seconds.')
    
def do_step_cymdist_griddyn14bus_fmus():
    """Simulate one CYMDIST FMU.
        
    """  
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 0.8
    step_size = 0.1
    sleep_time = 2
    # Path to configuration file
    path_config="Z:\\thierry\\proj\\cyder_repo\\jonathan\\CyDER\\web\\docker_django\\worker\\config.json"
    con_val_str = bytes(path_config, 'utf-8')
    
    griddyn_input_valref=[]
    griddyn_output_valref=[] 
    griddyn_output_values=[]
    
    cymdist_input_valref=[] 
    cymdist_output_valref=[]
    cymdist_output_values=[]  
    
    cymdist=load_fmu("../fmus/CYMDIST/CYMDIST.fmu", log_level=7)
    griddyn=load_fmu("../fmus/griddyn/griddyn14bus.fmu", log_level=7)

    cymdist.setup_experiment(start_time=start_time, stop_time=stop_time)
    griddyn.setup_experiment(start_time=start_time, stop_time=stop_time)
    
    # Define the inputs
    cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    #cymdist_input_values = [2520, 2520, 2520, 0, -120, 120]
    cymdist_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    
    griddyn_input_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC', 
                       'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    #griddyn_input_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    griddyn_output_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC', 
                'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']
    
    # Get the value references of griddyn inputs
    for elem in griddyn_input_names:
        griddyn_input_valref.append(griddyn.get_variable_valueref(elem))
    
    # Get the value references of griddyn outputs
    for elem in griddyn_output_names:
        griddyn_output_valref.append(griddyn.get_variable_valueref(elem))
    
    # Get the value references of cymdist inputs
    for elem in cymdist_input_names:
        cymdist_input_valref.append(cymdist.get_variable_valueref(elem))   
        
    # Get the value references of cymdist outputs 
    for elem in cymdist_output_names:
        cymdist_output_valref.append(cymdist.get_variable_valueref(elem))  

    # Set the flag to save the results
    cymdist.set("save_to_file", 0)
    # Get the initial outputs from griddyn
   # griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
    # Set the initial outputs of GridDyn in cymdist
    #cymdist.set_real (cymdist_input_valref, griddyn_output_values) 
    # Get value reference of the configuration file 
    con_val_ref = cymdist.get_variable_valueref("conFilNam")
    
    # Set the configuration file
    cymdist.set_string([con_val_ref], [con_val_str])
    
    start = datetime.now()
    # Initialize the FMUs
    cymdist.initialize()
    griddyn.initialize()
    
    # Create vectot to store time
    simTim=[]
    
    CYMDIST_VA = []
    CYMDIST_IA = []
    
    #Plots a couple of time since 
    # matplotlib throws a bit image allocation 
    # error if it runs out of memory
    fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1)
    fig.subplots_adjust(hspace=.5)
    ax1.grid(True)
    ax2.grid(True)
    ax1.set_title('Voltage(Distribution)')
    ax1.set_xlabel('time') 
    ax1.set_ylabel('VMA_A[V]') 
    ax2.set_title('Current(Distribution)')
    ax2.set_xlabel('time') 
    ax2.set_ylabel('IA[A]') 
    # Co-simulation loop
    for tim in np.arange(start_time, stop_time, step_size):
        # Get the outputs from griddyn
        griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
        #print("griddyn_output_values" + str(griddyn_output_values))
        
        #print("cymdist_input_valref" + str(cymdist_input_valref))
        cymdist.set_real(cymdist_input_valref, griddyn_output_values)
        cymdist.do_step(current_t=tim, step_size=step_size, new_step=0)
        cymdist_output_values = (cymdist.get_real(cymdist_output_valref))
        #print("cymdist_output_values" + str(cymdist_output_values))
        
        griddyn.set_real(griddyn_input_valref, cymdist_output_values)
        griddyn.do_step(current_t=tim, step_size=step_size, new_step=0)
        
        CYMDIST_VA.append(cymdist.get_real(cymdist.get_variable_valueref('VMAG_A')))
        CYMDIST_IA.append(cymdist.get_real(cymdist.get_variable_valueref('IA')))
        #print('This is the voltage value (VMAG_A) in Cymdist' 
        #  + str(cymdist.get_real(cymdist.get_variable_valueref('VMAG_A'))))
        #print('This is the current value (IA) in Cymdist' 
        #  + str(cymdist.get_real(cymdist.get_variable_valueref('IA'))))
        simTim.append(tim)
        ax1.plot(simTim, CYMDIST_VA, 'g')
        ax2.plot(simTim, CYMDIST_IA, 'b')
        plt.show(block=False)
        plt.pause(1) 
        #new bit here
        #fig.clf() #where f is the figure
        #plt.close(fig) 
    # Terminate FMUs
    cymdist.terminate()
    griddyn.terminate()
    end = datetime.now()
    
    print('Ran a single CYMDIST simulation in ' + 
          str((end - start).total_seconds()) + ' seconds.')

if __name__ == '__main__':
    #simulate_single_cymdist_fmu()
    #simulate_single_griddyn_fmu()
    #simulate_cymdist_griddyn_fmus()
    #simulate_algebraicloop_fmus()
    #simulate_cymdist_griddyn14bus_fmus()
    #simulate_single_griddyn14bus_fmu()
    do_step_cymdist_griddyn14bus_fmus()
