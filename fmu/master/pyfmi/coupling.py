from pyfmi import load_fmu
from pyfmi.master import Master
import time as t
from datetime import datetime
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
plt.switch_backend('Qt4Agg')

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
    step_size  = 0.1
    
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
    print('Ran a simulation with algebraic loop in ' +
          str((end - start).total_seconds()) + ' seconds.')

def simulate_two_griddyn14bus_fmu():
    """Simulate one griddyn FMU.
        
    """   
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 300
    step_size  = 5.0
    
    griddyn_input_valref=[]
    griddyn_output_valref=[] 
    griddyn_output_values=[]
    
    griddyn=load_fmu("../fmus/griddyn/14bus2input.fmu", log_level=7)
    griddyn_input_names = ['Bus10_IA', 'Bus10_IB', 'Bus10_IC', 
                           'Bus10_IAngleA', 'Bus10_IAngleB', 
                           'Bus10_IAngleC','Bus11_IA', 'Bus11_IB', 'Bus11_IC', 
                           'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    griddyn_input_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93,
                            277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    griddyn_output_names = ['Bus10_VA', 'Bus10_VB', 'Bus10_VC', 
                            'Bus10_VAngleA', 'Bus10_VAngleB', 'Bus10_VAngleC',
                            'Bus11_VA', 'Bus11_VB', 'Bus11_VC', 
                            'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']

    griddyn.setup_experiment(start_time=start_time, stop_time=stop_time)

  # Get the value references of griddyn inputs
    for elem in griddyn_input_names:
        griddyn_input_valref.append(griddyn.get_variable_valueref(elem))
    
    # Get the value references of griddyn outputs
    for elem in griddyn_output_names:
        griddyn_output_valref.append(griddyn.get_variable_valueref(elem))
    
    # Set the value of the multiplier
    griddyn.set('multiplier11', 3.0)
    # Set the value of the multiplier
    griddyn.set('multiplier10', 3.0)

    # Initialize the FMUs
    griddyn.initialize()
    
    # Create vector to store time
    simTim=[]
        
    # Co-simulation loop
    start = datetime.now()
    for tim in np.arange(start_time, stop_time, step_size):
        griddyn.set_real(griddyn_input_valref, griddyn_input_values)
        griddyn.do_step(current_t=tim, step_size=step_size)
        simTim.append(tim)
    # Terminate FMUs
    griddyn.terminate()
    end = datetime.now()
    
    print('Ran a single GridDyn simulation with two feeders in ' + 
          str((end - start).total_seconds()) + ' seconds.')

def simulate_one_cymdist_fmu():
    """Simulate one CYMDIST FMU.
        
    """ 
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 5.0
    step_size  = 5.0

    # Path to configuration file
    path_config=os.path.abspath("config.json")
    cymdist_con_val_str = bytes(path_config, 'utf-8')
    
    cymdist_input_valref=[] 
    cymdist_output_valref=[]
    cymdist_output_values=[]  
    
    cymdist = load_fmu("../fmus/CYMDIST/CYMDIST.fmu", log_level=7)
    cymdist.setup_experiment(start_time=start_time, stop_time=stop_time)
    
    # Define the inputs
    cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    cymdist_input_values = [2520, 2520, 2520, 0, -120, 120]
    cymdist_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    
    # Get the value references of cymdist inputs
    for elem in cymdist_input_names:
        cymdist_input_valref.append(cymdist.get_variable_valueref(elem))   
        
    # Get the value references of cymdist outputs 
    for elem in cymdist_output_names:
        cymdist_output_valref.append(cymdist.get_variable_valueref(elem))  

    # Set the flag to save the results
    cymdist.set("_saveToFile", 0)
    # Get value reference of the configuration file 
    cymdist_con_val_ref = cymdist.get_variable_valueref("_configurationFileName")
    
    # Set the configuration file
    cymdist.set_string([cymdist_con_val_ref], [cymdist_con_val_str])
    
    # Initialize the FMUs
    cymdist.initialize()
    
    # Call event update prior to entering continuous mode.
    cymdist.event_update()
    
    # Enter continuous time mode
    cymdist.enter_continuous_time_mode()
    
    print("Done initializing the FMU")
    # Create vector to store time
    simTim=[]

    print ("Starting the time integration" )    
    start = datetime.now()
    cymdist.set_real(cymdist_input_valref, cymdist_input_values)
    print("This is the result of the angle IAngleA: " 
          + str(cymdist.get_real(cymdist.get_variable_valueref('IAngleA'))))
    # Terminate FMUs
    cymdist.terminate()
    end = datetime.now()
    
    print('Ran a single CYMDIST simulation in ' + 
          str((end - start).total_seconds()) + ' seconds.')

def simulate_one_griddyn14bus_fmus():
    """Simulate one CYMDIST FMU.
        
    """  
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 300
    step_size  = 5.0
    sleep_time = 2.0
    
    griddyn_input_valref=[]
    griddyn_output_valref=[] 
    griddyn_output_values=[]
    
    griddyn=load_fmu("../fmus/griddyn/griddyn14bus.fmu", log_level=7)

    griddyn.setup_experiment(start_time=start_time, stop_time=stop_time)

    
    griddyn_input_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC', 
                       'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    griddyn_input_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    griddyn_output_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC', 
                'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']
    
    # Get the value references of griddyn inputs
    for elem in griddyn_input_names:
        griddyn_input_valref.append(griddyn.get_variable_valueref(elem))
    
    # Get the value references of griddyn outputs
    for elem in griddyn_output_names:
        griddyn_output_valref.append(griddyn.get_variable_valueref(elem))

    # Initialize the FMUs
    griddyn.initialize()
    
    # Set the value of the multiplier
    griddyn.set('multiplier', 3.0)
    
    # Create vector to store time
    simTim=[]
    
    # Co-simulation loop
    start = datetime.now()
    for tim in np.arange(start_time, stop_time, step_size):
        
        griddyn.set_real(griddyn_input_valref, griddyn_input_values)
        griddyn.do_step(current_t=tim, step_size=step_size)
        simTim.append(tim)
    # Terminate FMUs
    griddyn.terminate()
    end = datetime.now()
    
    print('Ran a single CYMDIST simulation in ' + 
          str((end - start).total_seconds()) + ' seconds.')

def simulate_cymdist_griddyn14bus_fmus():
    """Simulate coupled GridDyn and CYMDIST FMUs.
        
    """  
    # Parameters which will be arguments of the function
    start_time = 0.0
    stop_time  = 300
    step_size  = 300
    
    # Path to configuration file
    path_config=os.path.abspath("config.json")
    cymdist_con_val_str = bytes(path_config, 'utf-8')
    
    griddyn_input_valref=[]
    griddyn_output_valref=[] 
    griddyn_output_values=[]
    
    cymdist_input_valref=[] 
    cymdist_output_valref=[]
    cymdist_output_values=[]  
    
    cymdist = load_fmu("../fmus/CYMDIST/CYMDIST.fmu", log_level=7)
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
    cymdist.set("_saveToFile", 0)
    # Get the initial outputs from griddyn
    # Get value reference of the configuration file 
    cymdist_con_val_ref = cymdist.get_variable_valueref("_configurationFileName")
    
    # Set the configuration file
    cymdist.set_string([cymdist_con_val_ref], [cymdist_con_val_str])
    
    # Set the value of the multiplier
    griddyn.set('multiplier', 3.0)

    # Initialize the FMUs
    cymdist.initialize()
    griddyn.initialize()
    
    # Call event update prior to entering continuous mode.
    cymdist.event_update()
    cymdist.enter_continuous_time_mode()
    
    # Create vector to store time
    simTim=[]
    CYMDIST_IA = []
    CYMDIST_IB = []
    CYMDIST_IC = []
    GRIDDYN_VA = []
    GRIDDYN_VB = []
    GRIDDYN_VC = []
    
    # Interactive mode on
    plt.ion()

    # Create the plot
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.set_ylabel('Feeder currents\n(cymDist) [A]')
    ax2.set_ylabel('Feeder voltages\n(GridDyn) [pu]')
    ax2.set_xlabel('Time (minutes)')

    line1A, = ax1.plot(simTim, CYMDIST_IA)
    line1B, = ax1.plot(simTim, CYMDIST_IB)
    line1C, = ax1.plot(simTim, CYMDIST_IC)
    line2A, = ax2.plot(simTim, GRIDDYN_VA)
    line2B, = ax2.plot(simTim, GRIDDYN_VB)
    line2C, = ax2.plot(simTim, GRIDDYN_VC)
    ax1.legend(loc=0)
    
    # Co-simulation loop
    start = datetime.now()
    cnt = 0
    for tim in np.arange(start_time, stop_time, step_size):
        cnt+=1
        # Get the outputs from griddyn
        griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
        # set the time in cymdist
        cymdist.time = tim
        cymdist.set_real(cymdist_input_valref, griddyn_output_values)
        cymdist_output_values = (cymdist.get_real(cymdist_output_valref))
        #print("cymdist_output_values" + str(cymdist_output_values))
        
        CYMDIST_IA.append(cymdist.get_real(cymdist.get_variable_valueref('IA'))[0])
        CYMDIST_IB.append(cymdist.get_real(cymdist.get_variable_valueref('IB'))[0])
        CYMDIST_IC.append(cymdist.get_real(cymdist.get_variable_valueref('IC'))[0])
        GRIDDYN_VA.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VA'))[0] / 2520)
        GRIDDYN_VB.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VB'))[0] / 2520)
        GRIDDYN_VC.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VC'))[0] / 2520)
        simTim.append(tim/60)
        line1A.set_xdata(simTim)
        line1A.set_ydata(CYMDIST_IA)
        line1B.set_xdata(simTim)
        line1B.set_ydata(CYMDIST_IB)
        line1C.set_xdata(simTim)
        line1C.set_ydata(CYMDIST_IC)

        line2A.set_xdata(simTim)
        line2A.set_ydata(GRIDDYN_VA)
        line2B.set_xdata(simTim)
        line2B.set_ydata(GRIDDYN_VB)
        line2C.set_xdata(simTim)
        line2C.set_ydata(GRIDDYN_VC)

        ax1.relim()
        ax1.autoscale_view(True,True,True)
        ax2.relim()
        ax2.autoscale_view(True,True,True)
        fig.canvas.draw()
        plt.pause(1)
        #new bit here
        #fig.clf() #where f is the figure
        #plt.close(fig)
    plt.close() 
    # Terminate FMUs
    cymdist.terminate()
    griddyn.terminate()
    end = datetime.now()
    
    print('Ran a coupled GridDyn/CYMDIST simulation in ' + 
          str((end - start).total_seconds() - cnt) + ' seconds.')

if __name__ == '__main__':

    #simulate_algebraicloop_fmus()
    #simulate_one_griddyn14bus_fmu()
    #simulate_two_griddyn14bus_fmu()
    #simulate_one_cymdist_fmu()
    simulate_cymdist_griddyn14bus_fmus()
