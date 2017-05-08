from __future__ import division
from pyfmi import load_fmu
from pyfmi.master import Master
import progressbar

def simulate_2cymdist_gridyn_fmus(configuration_filename, configuration_filename2, start_time, end_time, step_size, _saveToFile=0, input_profiles=False, x_axis_labels=False):
    """Simulate one CYMDIST FMU.
    """
    # Parameters which will be arguments of the function
    start_time = start_time
    stop_time  = end_time
    step_size = step_size

    # Path to configuration file
    path_config1 = configuration_filename
    path_config2 = configuration_filename2
    cymdist_con_val_str1 = bytes(path_config1, 'utf-8')
    cymdist_con_val_str2 = bytes(path_config2, 'utf-8')

    griddyn_input_valref = []
    griddyn_output_valref = []

    cymdist_input_valref = []
    cymdist_output_valref = []
    cymdist_input_valref2 = []
    cymdist_output_valref2 = []

    cymdist1 = load_fmu("C:/cygwin64/home/Jonathan/project_cyder/web/docker_django/worker/simulation/fmu_code/CYMDIST.fmu", log_level=7)
    cymdist2 = load_fmu("C:/cygwin64/home/Jonathan/project_cyder/web/docker_django/worker/simulation/fmu_code/CYMDIST.fmu", log_level=7)
    griddyn=load_fmu("C:/cygwin64/home/Jonathan/project_cyder/web/docker_django/worker/simulation/fmu_code/14bus2input.fmu", log_level=7)

    cymdist1.setup_experiment(start_time=start_time, stop_time=stop_time)
    cymdist2.setup_experiment(start_time=start_time, stop_time=stop_time)
    griddyn.setup_experiment(start_time=start_time, stop_time=stop_time)

    # Define the inputs
    cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
    #cymdist_input_values = [2520, 2520, 2520, 0, -120, 120]
    cymdist_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']

    griddyn_input_names = ['Bus10_IA', 'Bus10_IB', 'Bus10_IC',
                           'Bus10_IAngleA', 'Bus10_IAngleB', 'Bus10_IAngleC',
                           'Bus11_IA', 'Bus11_IB', 'Bus11_IC',
                           'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
    #griddyn_input_values = [277.6, 200.1, 173.1, -13.7, -130.51, 111.93]
    griddyn_output_names = ['Bus10_VA', 'Bus10_VB', 'Bus10_VC',
                            'Bus10_VAngleA', 'Bus10_VAngleB', 'Bus10_VAngleC',
                            'Bus11_VA', 'Bus11_VB', 'Bus11_VC',
                            'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']

    # Get the value references of griddyn inputs
    for elem in griddyn_input_names:
        griddyn_input_valref.append(griddyn.get_variable_valueref(elem))

    # Get the value references of griddyn outputs
    for elem in griddyn_output_names:
        griddyn_output_valref.append(griddyn.get_variable_valueref(elem))

    # Get the value references of cymdist inputs
    for elem in cymdist_input_names:
        cymdist_input_valref.append(cymdist1.get_variable_valueref(elem))

    # Get the value references of cymdist outputs
    for elem in cymdist_output_names:
        cymdist_output_valref.append(cymdist1.get_variable_valueref(elem))

    # Get the value references of cymdist inputs
    for elem in cymdist_input_names:
        cymdist_input_valref2.append(cymdist2.get_variable_valueref(elem))

    # Get the value references of cymdist outputs
    for elem in cymdist_output_names:
        cymdist_output_valref2.append(cymdist2.get_variable_valueref(elem))

    # Set the flag to save the results
    cymdist1.set("_saveToFile", _saveToFile)
    # cymdist1.set("_communicationStepSize", step_size)
    cymdist2.set("_saveToFile", _saveToFile)
    # cymdist2.set("_communicationStepSize", step_size)
    # Get the initial outputs from griddyn
    # griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
    # Set the initial outputs of GridDyn in cymdist
    # cymdist.set_real (cymdist_input_valref, griddyn_output_values)
    # Get value reference of the configuration file
    cymdist_con_val_ref1 = cymdist1.get_variable_valueref("_configurationFileName")
    cymdist_con_val_ref2 = cymdist2.get_variable_valueref("_configurationFileName")

    # Set the configuration file
    cymdist1.set_string([cymdist_con_val_ref1], [cymdist_con_val_str1])
    cymdist2.set_string([cymdist_con_val_ref2], [cymdist_con_val_str2])

    # Set the value of the multiplier
    griddyn.set('multiplier10', 3.0)
    griddyn.set('multiplier11', 3.0)

    # Initialize the FMUs
    cymdist1.initialize()
    cymdist2.initialize()

    # Call event update prior to entering continuous mode.
    cymdist1.event_update()
    cymdist1.enter_continuous_time_mode()

    cymdist2.event_update()
    cymdist2.enter_continuous_time_mode()

    griddyn.initialize()

    # Create vector to store time
    simTim=[]
    CYMDIST_IA1 = []
    CYMDIST_IB1 = []
    CYMDIST_IC1 = []
    CYMDIST_IA2 = []
    CYMDIST_IB2 = []
    CYMDIST_IC2 = []
    GRIDDYN_V10 = []
    GRIDDYN_V11 = []

    # Interactive mode on
    plt.ion()

    # Create the plot
    fig = plt.figure(figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(411)
    ax1 = fig.add_subplot(412)
    ax2 = fig.add_subplot(413)
    ax3 = fig.add_subplot(414)
    ax.set_ylabel('Inputs')
    ax1.set_ylabel('Feeder currents\n(CymDist 1) [A]')
    ax2.set_ylabel('Feeder currents\n(CymDist 2) [A]')
    ax3.set_ylabel('Bus voltages\n(GridDyn) [V]')
    ax3.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    ax3.set_xlabel('Time (minutes)')
    if input_profiles:
        for input_profile in input_profiles:
            line, = ax.plot(input_profile['x'], input_profile['y'], label=input_profile['label'])
    line1A, = ax1.plot(simTim, CYMDIST_IA1, label='Phase A')
    line1B, = ax1.plot(simTim, CYMDIST_IB1, label='Phase B')
    line1C, = ax1.plot(simTim, CYMDIST_IC1, label='Phase C')
    line2A, = ax2.plot(simTim, CYMDIST_IA2, label='Phase A')
    line2B, = ax2.plot(simTim, CYMDIST_IB2, label='Phase B')
    line2C, = ax2.plot(simTim, CYMDIST_IC2, label='Phase C')
    line10, = ax3.plot(simTim, GRIDDYN_V10, label='Bus 10')
    line11, = ax3.plot(simTim, GRIDDYN_V11, label='Bus 11')
    ax.legend(loc=0)
    ax1.legend(loc=1)
    ax2.legend(loc=1)
    ax3.legend(loc=1)
    fig.tight_layout()

    # # Save all the result to a pandas dataframe
    # cymdist_column_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    # griddyn_column_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC',
    #                         'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']
    # column_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
    # column_names.extend(griddyn_column_names)
    # df = pandas.DataFrame(index=np.arange(start_time, stop_time, step_size) * 10, columns=column_names)

    # Co-simulation loop
    for tim in np.arange(start_time, stop_time, step_size):

        # # Get the outputs from griddyn
        # griddyn_output_values = (griddyn.get_real(griddyn_output_valref))
        griddyn_output_values1 = [2520, 2520, 2520, 0, -120, 120]
        griddyn_output_values2 = [7270, 7270, 7270, 0, -120, 120]

        # set time in cymdist
        cymdist1.time = tim
        # set time in cymdist
        cymdist2.time = tim

        cymdist1.set_real(cymdist_input_valref, griddyn_output_values1)
        cymdist2.set_real(cymdist_input_valref, griddyn_output_values2)

        cymdist_output_values = list(cymdist1.get_real(cymdist_output_valref))
        cymdist_output_values.extend(cymdist2.get_real(cymdist_output_valref))
        griddyn.set_real(griddyn_input_valref, cymdist_output_values)
        griddyn.do_step(current_t=tim, step_size=step_size, new_step=0)

        CYMDIST_IA1.append(cymdist1.get_real(cymdist1.get_variable_valueref('IA'))[0])
        CYMDIST_IB1.append(cymdist1.get_real(cymdist1.get_variable_valueref('IB'))[0])
        CYMDIST_IC1.append(cymdist1.get_real(cymdist1.get_variable_valueref('IC'))[0])
        CYMDIST_IA2.append(cymdist2.get_real(cymdist2.get_variable_valueref('IA'))[0])
        CYMDIST_IB2.append(cymdist2.get_real(cymdist2.get_variable_valueref('IB'))[0])
        CYMDIST_IC2.append(cymdist2.get_real(cymdist2.get_variable_valueref('IC'))[0])
        GRIDDYN_V10.append(griddyn.get_real(griddyn.get_variable_valueref('Bus10_VA'))[0])
        GRIDDYN_V11.append(griddyn.get_real(griddyn.get_variable_valueref('Bus11_VA'))[0])
        simTim.append(tim / 60)

        # for name in cymdist_column_names:
        #     df.loc[simTim[-1], name] = cymdist.get_real(cymdist.get_variable_valueref(name))[0]
        #
        # for name in griddyn_column_names:
        #     df.loc[simTim[-1], name] = griddyn.get_real(griddyn.get_variable_valueref(name))[0]

        line1A.set_xdata(simTim)
        line1A.set_ydata(CYMDIST_IA1)
        line1B.set_xdata(simTim)
        line1B.set_ydata(CYMDIST_IB1)
        line1C.set_xdata(simTim)
        line1C.set_ydata(CYMDIST_IC1)

        line2A.set_xdata(simTim)
        line2A.set_ydata(CYMDIST_IA2)
        line2B.set_xdata(simTim)
        line2B.set_ydata(CYMDIST_IB2)
        line2C.set_xdata(simTim)
        line2C.set_ydata(CYMDIST_IC2)

        line10.set_xdata(simTim)
        line10.set_ydata(GRIDDYN_V10)

        line11.set_xdata(simTim)
        line11.set_ydata(GRIDDYN_V11)

        ax1.relim()
        ax1.autoscale_view(True,True,True)
        ax2.relim()
        ax2.autoscale_view(True,True,True)
        ax3.relim()
        ax3.autoscale_view(True,True,True)
        fig.canvas.draw()
        plt.pause(0.01)

    pdb.set_trace()
    # df.to_csv('~/project_cyder/web/docker_django/worker/simulation/cosimulation_result.csv')
    # close figure automatically
    plt.close()

    # Terminate FMUs
    cymdist1.terminate()
    cymdist2.terminate()
    griddyn.terminate()
    return {'result': 'some stuff'}
