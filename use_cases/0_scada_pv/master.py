from pyfmi import load_fmu
from pv import PVFactory
import pandas

# Inputs
start = '2016-06-17 10:00:00'
end = '2016-06-17 15:00:00'
timestep = '30T'  # 30 minutes
times = [t for t in range()]

# Select SCADA for the simulation
scada = pandas.read_csv('BU0006.sxst', parse_dates=[0])
scada = scada.set_index('TIME')
scada = scada[start:end]
scada.save('scada.csv')

# Load Cymdist FMU
cymdist_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C',
                       'VANG_A', 'VANG_B', 'VANG_C',
                       'networkid#node#PV', 'networkid#node#PV', 'networkid#node#PV']
cymdist_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
cymdist = load_fmu('fmus/cymdist/cymdist.fmu', log_level=7)
cymdist.setup_experiment(start_time=times[0], stop_time=times[-1])
cymdist_input_val_ref = [cymdist.get_variable_valueref(name) for name
                         in cymdist_input_names]
cymdist_output_val_ref = [cymdist.get_variable_valueref(name) for name
                          in cymdist_output_names]
cymdist.initialize()
cymdist.event_update()
cymdist.enter_continuous_time_mode()

# Load GridDyn FMU
griddyn_input_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC',
                       'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
griddyn_output_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC',
                        'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']
griddyn = load_fmu('fmus/griddyn/griddyn14bus.fmu', log_level=7)
griddyn.setup_experiment(start_time=times[0], stop_time=times[-1])
griddyn_input_val_ref = [griddyn.get_variable_valueref(name) for name
                         in griddyn_input_names]
griddyn_output_val_ref = [griddyn.get_variable_valueref(name) for name
                          in griddyn_output_names]
griddyn.set('multiplier', 1.0)
griddyn.initialize()

# Load PV Factory
pv_capacities = [-200, -100, -50]
pvs = PVFactory('solar.csv', pv_capacities)

# Launch simulation
results = {'t': [],
           'substation_voltages': [[21600, 21600, 21600, 0, -120, 120]],
           'substation_currents': []}
for t in times:
    # Run pv simulation
    pv_production = [pv.step(t) for pv in pvs]

    # Run Cymdist simulation
    cymdist.time = t
    values = list(results['substation_voltages'][0])  # Un-hook T&D 0 --> -1
    values.extend(pv_production)
    cymdist.set_real(cymdist_input_val_ref, values)
    results['substation_currents'].append(
        list(cymdist.get_real(cymdist_output_val_ref)))

    # Run GridDyn
    griddyn.set_real(griddyn_input_val_ref,
                     results['substation_currents'][-1])
    griddyn.do_step(current_t=t, step_size=1, new_step=0)
    results['substation_voltages'].append(
        list(griddyn.get_real(griddyn_output_val_ref)))
    results['t'].append(t)

# Close all FMUs
cymdist.terminate()
griddyn.terminate()


# Plot head voltages and head currents
plt.figure(figsize=(11, 5))
for index, phase in enumerate(['A', 'B', 'C']):
    plt.plot(results['t'],
             [results['substation_voltages'][t][index] for t in results['t'],
             label='phase ' + phase)
plt.ylabel('Voltage at the substation [V]')
plt.legend(loc=0)
plt.show()

plt.figure(figsize=(11, 5))
for index, phase in enumerate(['A', 'B', 'C']):
    plt.plot(results['t'],
             [results['substation_currents'][t][index] for t in results['t'],
             label='phase ' + phase)
plt.ylabel('Current at the substation [A]')
plt.legend(loc=0)
plt.show()
