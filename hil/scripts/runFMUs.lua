local omsimulator=require"OMSimulatorLua"

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
addConnection(model, "sensor.http___upmu_lbl_gov_9000_beea4c9c_c5a7_47c3_afb8_8afa956b5553", "control.v_pu")
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
--description="uPMU voltage phase A" name="http___upmu_lbl_gov_9000_50e545ba_e969_4e12_8bdb_a4f44ed5b26e"
--description="uPMU voltage angle phase A" name="http___upmu_lbl_gov_9000_a5b4ec54_4951_49a6_a03f_fd820d4f8eeb"
--description="uPMU voltage phase B" name="http___upmu_lbl_gov_9000_0eb398f9_0247_41ef_909b_539ad1791cbc"
--description="uPMU voltage angle phase B" name="http___upmu_lbl_gov_9000_5e01ad0a_be51_4f25_8eb5_55cf8f822f3b"
--description="uPMU voltage phase C" name="http___upmu_lbl_gov_9000_5c59f52a_e4e5_4b4d_b0a6_c464818d469a"
--description="uPMU voltage angle phase C" name="http___upmu_lbl_gov_9000_de122777_c60e_40a2_abaf_b54feea3ab9e"

output_voltage_names={"sensor.http___upmu_lbl_gov_9000_50e545ba_e969_4e12_8bdb_a4f44ed5b26e",
"sensor.http___upmu_lbl_gov_9000_a5b4ec54_4951_49a6_a03f_fd820d4f8eeb", "sensor.http___upmu_lbl_gov_9000_0eb398f9_0247_41ef_909b_539ad1791cbc",
"sensor.http___upmu_lbl_gov_9000_5e01ad0a_be51_4f25_8eb5_55cf8f822f3b", "sensor.http___upmu_lbl_gov_9000_5c59f52a_e4e5_4b4d_b0a6_c464818d469a",
"sensor.http___upmu_lbl_gov_9000_de122777_c60e_40a2_abaf_b54feea3ab9e"}
-- tcur = getCurrentTime(model)
-- for _,var in ipairs(output_voltage_names) do
--   print(var .. " at " .. tcur .. ": " .. getReal(model, var))
-- end
print("uPMU_out=" .. getReal(model, "sensor.http___upmu_lbl_gov_9000_beea4c9c_c5a7_47c3_afb8_8afa956b5553"))
print("control_q=" .. getReal(model, "control.q_control"))
terminate(model)
-- unloading the model causes the simulation to fail
-- we might need to add a real temporary temporary which
-- the FMUWrapper tries to remove when calling unload()
--unload(model)
