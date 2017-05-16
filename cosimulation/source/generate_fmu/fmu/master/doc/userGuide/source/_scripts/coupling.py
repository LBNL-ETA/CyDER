from pyfmi import load_fmu

def simulate_cymdist_griddyn14bus_fmus():
    """Simulate coupled GridDyn and CYMDIST FMUs.
        
    """  
    # Simulation parameters
    start_time = 0.0
    stop_time  = 300
    step_size  = 300
    
    # Path to the CYMDIST configuration file
    path_config=os.path.abspath("config.json")
    # Conversion to byte for PyFMI
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
    cymdist_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    
    griddyn_input_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC', 
                       'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
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
    
    # Co-simulation loop
    for tim in np.arange(start_time, stop_time, step_size):
        cnt+=1
        # Get the outputs from griddyn
        griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
        # set the time in cymdist
        cymdist.time = tim
        # Set the inputs of cymdist
        cymdist.set_real(cymdist_input_valref, griddyn_output_values)
        # Get the outputs of cymdist
        cymdist_output_values = (cymdist.get_real(cymdist_output_valref))
    # Terminate FMUs
    cymdist.terminate()
    griddyn.terminate()
        
if __name__ == '__main__':
    simulate_cymdist_griddyn14bus_fmus()
