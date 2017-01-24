from __future__ import division
import argparse
import sys
import datetime
import cympy


def load_allocation(values):
    """Run a load allocation

    Args:
        values (dictionnary): value1 (KVA) and value2 (PF) for A, B and C
    """

    # Create Load Allocation object
    la = cympy.sim.LoadAllocation()

    # Create the Demand object
    demand = cympy.sim.Meter()

    # Fill in the demand values
    demand.IsTotalDemand = False
    demand.DemandA = cympy.sim.LoadValue()
    demand.DemandA.Value1 = values['P_A']
    demand.DemandA.Value2 = values['Q_A']
    demand.DemandB = cympy.sim.LoadValue()
    demand.DemandB.Value1 = values['P_B']
    demand.DemandB.Value2 = values['Q_B']
    demand.DemandC = cympy.sim.LoadValue()
    demand.DemandC.Value1 = values['P_C']
    demand.DemandC.Value2 = values['Q_C']
    demand.LoadValueType = cympy.enums.LoadValueType.KW_KVAR

    # Get a list of networks
    networks = cympy.study.ListNetworks()

    # Set the first feeders demand
    la.SetDemand(networks[0], demand)

    # Set up the right voltage [V to kV]
    cympy.study.SetValueTopo(values['VMAG_A'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage1", networks[0])
    cympy.study.SetValueTopo(values['VMAG_B'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage2", networks[0])
    cympy.study.SetValueTopo(values['VMAG_C'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage3", networks[0])

    # Run the load allocation
    la.Run([networks[0]])
    return True


# Retrieve model name
try:
    parser = argparse.ArgumentParser(description='Needs model and upmu data')

    # Create args and parse them
    arg_names = ['filename', 'breaker_name', 'breaker_type', 'P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C', 'VMAG_A', 'VMAG_B', 'VMAG_C']
    for arg_name in arg_names:
        parser.add_argument(arg_name)
    args = parser.parse_args()

    # Assign args to variable and cast right format
    udata = {}
    for arg_name in ['P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C', 'VMAG_A', 'VMAG_B', 'VMAG_C']:
        udate[arg_name] = float(args[arg_name])
    model_filename = str(args.filename)
    breaker_name = str(args.breaker_name)
    breaker_type = str(args.breaker_type)

except:
    sys.exit('Error: could not retrieve argument')

# Open the model
parent_path = 'D://Users//Jonathan//Documents//GitHub//PGE_Models_DO_NOT_SHARE//'
cympy.study.Open(parent_path + model_filename)

# # Get data from upmu
# udata = {'VMAG_A': 7287.4208984375,
#          'VMAG_B': 7299.921875,
#          'VMAG_C': 7318.2822265625,
#          'P_A': 7272.5364248477308,
#          'P_B': 2118.3817519608633,
#          'P_C': 6719.1867010705246,
#          'Q_A': -284.19075651498088,
#          'Q_B': -7184.1189935099919,
#          'Q_C': 3564.4269660296022,
#          'units': ('kW', 'kVAR', 'V')}

# Run load allocation function to set input values
load_allocation(udata)

# Run the power flow
lf = cympy.sim.LoadFlow()
lf.Run()

# Get the voltages at breaker
v_A = cympy.study.QueryInfoDevice("VA", breaker_name, int(breaker_type))
v_B = cympy.study.QueryInfoDevice("VB", breaker_name, int(breaker_type))
v_C = cympy.study.QueryInfoDevice("VC", breaker_name, int(breaker_type))

v_angle_A = cympy.study.QueryInfoDevice("PH-AngleA", breaker_name, int(breaker_type))
v_angle_B = cympy.study.QueryInfoDevice("PH-AngleB", breaker_name, int(breaker_type))
v_angle_C = cympy.study.QueryInfoDevice("PH-AngleC", breaker_name, int(breaker_type))

i_A = cympy.study.QueryInfoDevice("IA", breaker_name, int(breaker_type))
i_B = cympy.study.QueryInfoDevice("IB", breaker_name, int(breaker_type))
i_C = cympy.study.QueryInfoDevice("IC", breaker_name, int(breaker_type))

i_angle_A = cympy.study.QueryInfoDevice("IAngleA", breaker_name, int(breaker_type))
i_angle_B = cympy.study.QueryInfoDevice("IAngleB", breaker_name, int(breaker_type))
i_angle_C = cympy.study.QueryInfoDevice("IAngleC", breaker_name, int(breaker_type))

# # Print the results
print(udata)  # upmu data
print({'A': v_A, 'B': v_B, 'C': v_C})  # voltage results
print({'A': v_angle_A, 'B': v_angle_B, 'C': v_angle_C})  # voltage angles
print({'A': i_A, 'B': i_B, 'C': i_C})  # current results
print({'A': i_angle_A, 'B': i_angle_B, 'C': i_angle_C})  # current angles
