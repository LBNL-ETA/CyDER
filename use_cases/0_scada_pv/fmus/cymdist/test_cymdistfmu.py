import datetime
import pandas
import os
path = os.getcwd()
import matplotlib.pyplot as plt
import cymdistfmu
os.chdir(path)

# #######################################################################
# Plot SCADA data
scada = pandas.read_csv('test_scada.csv')
scada = scada.set_index('TIME')
scada = scada.filter(regex=(".*_MW")).sum(axis=1)
plt.figure(figsize=(12, 5))
plt.plot(scada.iloc[0:10], label='SCADA data')
plt.xlabel('Time [hours]')
plt.ylabel('Active power [MW]')
plt.legend(loc=0)
plt.show()

# Test 1 PV + SCADA
configuration_filename = 'test_config.json'
input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C',
               'VANG_A', 'VANG_B', 'VANG_C',
               '024050401#314589739808-XFO#PV',
               '024050401#1823720.55_13644205.171#PV',
               '024050404#314621139826-XFO#PV']
input_values = [12590.00, 12590.00, 12590.00, 0, -120, 120, 0, 0, 0]
output_names = ['SOURCE_2405BK1#IA', 'SOURCE_2405BK1#IB',
                'SOURCE_2405BK1#IC', 'SOURCE_2405BK1#IAngleA',
                'SOURCE_2405BK1#IAngleB', 'SOURCE_2405BK1#IAngleC']
save_to_file = 0
outputs = {'scada': None}
results = []
for t in range(0, 10):
    # Toggle PV off/on
    if t >= 5:
        input_values[6] = -100  # kW generated
        input_values[7] = -100
        input_values[8] = -100

    # Launch simulation
    t_start = datetime.datetime.now()
    outputs = cymdistfmu.cymdist(configuration_filename, t, input_names,
            input_values, None, output_names, save_to_file)
    t_end = datetime.datetime.now()
    results.append({name: outputs[i] for i, name in enumerate(output_names)})
    results[-1]['time'] = t
    print('Simulation completed in ' +
          str((t_end - t_start).total_seconds()) + ' seconds')

# Can I save the model that was created on the last iteration?
# ----------------------------------------------------------------------
plt.figure(figsize=(12, 5))
plt.plot([result['time'] for result in results],
         [result['SOURCE_2405BK1#IA']
          for result in results],
         label='IA at SOURCE_2405BK1')
plt.plot([result['time'] for result in results],
         [result['SOURCE_2405BK1#IB']
          for result in results],
         label='IB at SOURCE_2405BK1')
plt.plot([result['time'] for result in results],
         [result['SOURCE_2405BK1#IC']
          for result in results],
         label='IC at SOURCE_2405BK1')
plt.xlabel('Time [hours]')
plt.ylabel('Current [A]')
plt.legend(loc=0)
plt.show()
# #######################################################################
