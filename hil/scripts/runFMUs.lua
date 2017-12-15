local omsimulator=require"OMSimulatorLua"
-- Change the output name of the sensor
--setLogFile("omslog.txt")
model = newModel()
setTempDirectory(".")
-- Instantiate cymdist
--instantiateFMU(model, "cymdist.fmu", "cymdist")
-- Instantiate sensor FMU
instantiateFMU(model, "uPMU.fmu", "sensor")
--Instantiate the controls FMU
instantiateFMU(model, "CyDER_HIL_Controls_voltvar.fmu", "control")
-- add connections
-- connect sensor FMu with inverter control algorithm
addConnection(model, "sensor.y_out", "control.v_pu")
-- connect inverter output to a dummy input.
addConnection(model, "control.q_control", "sensor._dummy")
-- output of control should be sent to input of OPAL-RT FMU
-- connect inverter output to a dummy input.
-- addConnection(model, "control.q_control", "opalrt.control")
-- connect inverter control to the physical device
-- addConnection(model, "control.q_control", "inverter.control")
-- We need to figure what outputs of OPAL-RT go to the inverter controls
-- It is rather thinkable that some inverter control outputs
-- go to the OPAL-RT FMU
-- inverter control output go to the physical device as well.
-- Set tresult file
setResultFile(model, "hil.mat")
-- Set the stopTime
setStopTime(model, 1)
-- Set the communication interval
setCommunicationInterval(model, 1)
-- Intialize all the models
initialize(model)
-- List of CYMDISt input names
input_voltage_names = {'cymdist.VMAG_A', 'cymdist.VMAG_B', 'cymdist.VMAG_C',
                       'cymdist.VANG_A', 'cymdist.VANG_B', 'cymdist.VANG_C'}
-- List of input values
input_voltage_values = {2520.0, 2520.0, 2520.0, 0.0, -120.0, 120.0}
-- i=1
-- for _,var in ipairs(input_voltage_names) do
--   setReal(model, var, input_voltage_values[i])
--   i=i+1
-- end
--doSteps(model, 1)
simulate(model)
-- output_voltage_names={"cymdist.IA", "cymdist.IAngleA", "cymdist.IB", "cymdist.IAngleB", "cymdist.IC", "cymdist.IAngleC"}
-- tcur = getCurrentTime(model)
-- for _,var in ipairs(output_voltage_names) do
--   print(var .. " at " .. tcur .. ": " .. getReal(model, var))
-- end
print("uPMU_out=" .. getReal(model, "sensor.y_out"))
print("control_q=" .. getReal(model, "control.q_control"))
terminate(model)
-- unloading the model causes the simulation to fail
-- we might need to add a real temporary temporary which
-- the FMUWrapper tries to remove when calling unload()
--unload(model)
