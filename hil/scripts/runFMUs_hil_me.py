import numpy as np
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import os
import time
import pandas as pd
#plt.switch_backend('Qt4Agg')
def run_simulator (nSteps):

    try:
        from pyfmi import load_fmu
    except BaseException:
        print ('PyFMI not installed. Script will not be be run.')
        return
    ############## Control FMU
    stepsize = 5
    #start_time = int(time.time() - time.mktime(datetime(2018, 1, 1, 0, 0).timetuple()))
    now = datetime.now()
    start_time = int(time.mktime(datetime(2018, 4, 19, now.hour, now.minute, now.second).timetuple()) -\
                    time.mktime(datetime(2018, 1, 1).timetuple()))
    print start_time
    stop_time = nSteps * start_time
    control_fmu_path = "../controls/me/controls.fmu"
    control1 = load_fmu(control_fmu_path)
    control1.setup_experiment(start_time=start_time, stop_time=stop_time)
    # Set parameters of the inverter control
    control1.set("QMaxCap", 0.0)
    control1.set("QMaxInd", -200000.0)
    control1.set("thr", 0.07)
    control1.set("hys", 0.033)
    control1.initialize()
    print ("Completed initialization of Controls FMU 1")
    control1.event_update()
    control1.enter_continuous_time_mode()
    control1_input_names = ["v"]
    control1_output_names = ["QCon"]

    ############## Control FMU
    control2 = load_fmu(control_fmu_path)
    control2.setup_experiment(start_time=start_time, stop_time=stop_time)
    # Set parameters of the inverter control
    control2.set("QMaxCap", 0.0)
    control2.set("QMaxInd", -200000.0)
    control2.set("thr", 0.07)
    control2.set("hys", 0.033)
    control2.initialize()
    print ("Completed initialization of Controls FMU 2")
    control2.event_update()
    control2.enter_continuous_time_mode()
    control2_input_names = ["v"]
    control2_output_names = ["QCon"]

    ############## Control FMU
    control3 = load_fmu(control_fmu_path)
    control3.setup_experiment(start_time=start_time, stop_time_defined=False, stop_time=stop_time)
    # Set parameters of the inverter control
    control3.set("QMaxCap", 0.0)
    control3.set("QMaxInd", -200000.0)
    control3.set("thr", 0.07)
    control3.set("hys", 0.033)
    control3.initialize()
    print ("Completed initialization of Controls FMU 3")
    control3.event_update()
    control3.enter_continuous_time_mode()
    control3_input_names = ["v"]
    control3_output_names = ["QCon"]

    ############## Control FMU
    control4 = load_fmu(control_fmu_path)
    control4.setup_experiment(start_time=start_time, stop_time_defined=False, stop_time=stop_time)
    # Set parameters of the inverter control
    control4.set("QMaxCap", 0.0)
    control4.set("QMaxInd", -1.0)
    control4.set("thr", 0.07)
    control4.set("hys", 0.033)
    control4.initialize()
    print ("Completed initialization of Controls FMU 4")
    control4.event_update()
    control4.enter_continuous_time_mode()
    control4_input_names = ["v"]
    control4_output_names = ["QCon"]

    # Inverter API FMU
    inverterapi_path = "../inverterapi/me/inverterapi.fmu"
    #inverterapi = load_fmu(inverterapi_path)
    #inverterapi.setup_experiment(start_time=start_time, stop_time_defined=False, stop_time=stop_time)
    #inverterapi.initialize()
    print ("Completed initialization of Inverter API FMU")
    #inverterapi.event_update()
    #inverterapi.enter_continuous_time_mode()
    #inveterapi_input_names = ["P"]

    # uPMU FMU
    upmu_path = "../sensors/me/uPMU.fmu"
    upmu=None
    #upmu = load_fmu(upmu_path)
    #upmu.setup_experiment(start_time=start_time, stop_time=stop_time)
    #upmu.initialize()
    print ("Completed initialization of uPMU FMU")
    #upmu.event_update()
    #upmu.enter_continuous_time_mode()
    upmu_output_names = ["uPMU"]

    # PV FMU
    pv_path = "../pv/me/pv.fmu"
    pv1 = load_fmu(pv_path)
    pv1.setup_experiment(start_time=start_time, stop_time_defined=False, stop_time=stop_time)
    pv1.set("filNam", "../pv/USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos")
    pv1.set('A_PV', 6000)
    pv1.set('azi', 0)
    pv1.initialize()
    print ("Completed initialization of PV FMU 1")
    pv1.event_update()
    pv1.enter_continuous_time_mode()
    pv1_output_names = ["PV_generation"]

    # PV FMU
    pv2 = load_fmu(pv_path)
    pv2.setup_experiment(start_time=start_time, stop_time_defined=False, stop_time=stop_time)
    pv2.set("filNam", "../pv/USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos")
    pv2.set('A_PV', 6000)
    pv2.set('azi', -90)
    pv2.initialize()
    print ("Completed initialization of PV FMU 2")
    pv2.event_update()
    pv2.enter_continuous_time_mode()
    pv2_output_names = ["PV_generation"]

    # PV FMU
    pv3 = load_fmu(pv_path)
    pv3.setup_experiment(start_time=start_time, stop_time_defined=False, stop_time=stop_time)
    pv3.set("filNam", "../pv/USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos")
    pv3.set('A_PV', 6000)
    pv3.set('azi', 90)
    pv3.initialize()
    print ("Completed initialization of PV FMU 3")
    pv3.event_update()
    pv3.enter_continuous_time_mode()
    pv3_output_names = ["PV_generation"]

    #OPAL-RT FMU
    opalrt_fmu_path  = "../realtime/models/multirate2/me/opalrt.fmu"
    opalrt = load_fmu(opalrt_fmu_path)
    opalrt.setup_experiment(start_time=start_time, stop_time_defined=False, stop_time=stop_time)
    opalrt.set("_configurationFileName", "../realtime/models/multirate2/multirate2.llp")
    opalrt.initialize()
    print ("Completed initialization of OPAL-RT FMU")
    opalrt.event_update()
    opalrt.enter_continuous_time_mode()

    # Input: multirate2a/SC_Console/port1(22) (22- 27 (P1, Q1, P2, Q2, P3, Q3))
    # Output: multirate2a/SM_HIL/port1(49) (49 - 51 (V1, V2, V3))
    opalrt_input_names = ['multirate2a_SC_Console_port1_22_', 'multirate2a_SC_Console_port1_23_',
                        'multirate2a_SC_Console_port1_24_', 'multirate2a_SC_Console_port1_25_',
                        'multirate2a_SC_Console_port1_26_', 'multirate2a_SC_Console_port1_27_']

    opalrt_output_names = ['multirate2a_SM_HIL_port1_49_', 'multirate2a_SM_HIL_port1_50_',
                        'multirate2a_SM_HIL_port1_51_', 'multirate2a_SM_HIL_port1_52_']
    # OPAL-RT FMU
    # Interactive mode on
    # plt.ion()
    # plt.ticklabel_format(useOffSet=False)
    # simTim=[]
    # opalrt_res_0 = []
    # opalrt_res_1 = []
    # opalrt_res_0 = []
    # opalrt_res_1 = []
    # opalrt_res_0 = []
    # opalrt_res_1 = []
    # opalrt_res_0 = []
    # opalrt_res_1 = []
    results = {}
    results['time'] = []
    results['pv1_P'] = []
    results['pv1_Q'] = []
    results['pv1_Qraw'] = []
    results['pv2_P'] = []
    results['pv2_Q'] = []
    results['pv2_Qraw'] = []
    results['pv3_P'] = []
    results['pv3_Q'] = []
    results['pv3_Qraw'] = []
    results['pv1_V'] = []
    results['pv2_V'] = []
    results['pv3_V'] = []
    results['pvhil_P'] = []
    results['pv4_Qraw'] = []
    results['pvhil_V'] = []


    # Create the plot
    # fig = plt.figure()
    # ax1 = fig.add_subplot(211)
    # ax2 = fig.add_subplot(212)
    # ax1.set_ylabel('Inverter Control\n[1]')
    # ax2.set_ylabel('Node Voltage\n[p.u]')
    # ax2.set_xlabel('Time [s]')
    #
    # line1A, = ax1.step(simTim, opalrt_res_0)
    # line2A, = ax2.step(simTim, opalrt_res_1)
    #
    # ax1.legend(loc=0)
    # val_in = 1.0
    # Simulation loop
    pv_control_memory = {}
    pv_control_memory['pv1'] = 0
    pv_control_memory['pv2'] = 0
    pv_control_memory['pv3'] = 0
    pv_control_memory['pv4'] = 100
    t_constant = 2.5 # 5.0 works ok
    for idx in range(0, nSteps):
        print("========This is the {!s} invocation".format(idx))
        realtime = int(time.time() - time.mktime(datetime(2018, 1, 1, 0, 0).timetuple()))
        print ("The model time={!s}".format(realtime))
        # Assign the realtime in all FMUs.
        opalrt.time = realtime
        control1.time = realtime
        control2.time = realtime
        control3.time = realtime
        control4.time = realtime
        #inverterapi.time=realtime
        pv1.time = realtime
        pv2.time = realtime
        pv3.time = realtime
        #upmu.time = realtime

        _opalrt_outs= opalrt.get(opalrt_output_names)
        #print ("This is the outputs[0] of OPAL-RT={}".format(_opalrt_outs[0][0]))
        #print ("This is the outputs[1] of OPAL-RT={}".format(_opalrt_outs[1][0]))
        #print ("This is the outputs[2] of OPAL-RT={}".format(_opalrt_outs[2][0]))
        # Connect OPAL-RT to inverter control
        offset = 0.0
        res = _opalrt_outs[0][0]/120.0 + offset
        control1.set("v", res)
        results['pv1_V'].append(res)
        res = _opalrt_outs[1][0]/120.0 + offset
        control2.set("v", res)
        results['pv2_V'].append(res)
        res = _opalrt_outs[2][0]/120.0 + offset
        control3.set("v", res)
        results['pv3_V'].append(res)

        print ("================ output of v={!s}".format(control3.get("v")))
        print ("================ output of Q={!s}".format(control3.get("QCon")))

        ### Connect PV with OPAL-RT
        res = pv1.get("PV_generation")[0] *-1
        opalrt.set(opalrt_input_names[0], res)
        results['pv1_P'].append(res)
        res = control1.get("QCon")[0]
        results['pv1_Qraw'].append(res)
        pv_control_memory['pv1'] = pv_control_memory['pv1'] + (res-pv_control_memory['pv1']) / t_constant
        opalrt.set(opalrt_input_names[1], pv_control_memory['pv1'])
        results['pv1_Q'].append(pv_control_memory['pv1'])

        res = pv2.get("PV_generation")[0] *-1
        opalrt.set(opalrt_input_names[2], res)
        results['pv2_P'].append(res)
        res = control2.get("QCon")[0]
        results['pv2_Qraw'].append(res)
        pv_control_memory['pv2'] = pv_control_memory['pv2'] + (res-pv_control_memory['pv2']) / t_constant
        opalrt.set(opalrt_input_names[3], pv_control_memory['pv2'])
        results['pv2_Q'].append(pv_control_memory['pv2'])

        res = pv3.get("PV_generation")[0] *-1
        opalrt.set(opalrt_input_names[4], res)
        results['pv3_P'].append(res)
        res = control3.get("QCon")[0]
        results['pv3_Qraw'].append(res)
        pv_control_memory['pv3'] = pv_control_memory['pv3'] + (res-pv_control_memory['pv3']) / t_constant
        opalrt.set(opalrt_input_names[5], pv_control_memory['pv3'])
        results['pv3_Q'].append(pv_control_memory['pv3'])

        # Connect uPMU with inverter control
        #res = upmu.get("uPMU")[0] /120.
        # Voltage at interconnection point.
        res = _opalrt_outs[3][0]/120.0
        control4.set("v", res)
        results['pvhil_V'].append(res)
        # Connect inverter control to inverter api
        # This needs to be changed to be P instead of QCon
        res = control4.get("QCon")[0]
        results['pv4_Qraw'].append(res)
        res = (1-res) *100
        pv_control_memory['pv4'] = pv_control_memory['pv4'] + (res-pv_control_memory['pv4']) / t_constant
        print ("Inverter Control", res, "Control Calculated", pv_control_memory['pv4'], "PF", control4.get("QCon"))
        #inverterapi.set("P", int(pv_control_memory['pv4']))
        # The FMU will only update if get and set are called.
        #inverterapi.get("_dummy")
        results['pvhil_P'].append(pv_control_memory['pv4'])
        # Get the realtime from the clock in the opal-rt model
        results['time'].append(realtime)
        #simTim.append(realtime)
        # line1A.set_xdata(simTim)
        # line1A.set_ydata(control_res)
        #opalrt_res_0.append(float("{0:.8f}".format(_opalrt_outs[0][0]/120.0)))
        #opalrt_res_1.append(float("{0:.8f}".format(_opalrt_outs[1][0]/120.0)))
        #df = pd.DataFrame({"time": np.array(simTim), "voltage[0]":np.array(opalrt_res_0), "voltage[1]":np.array(opalrt_res_1)})
        df = pd.DataFrame(results)
        df.to_csv("opalrt_res.csv", index=False)
        # line2A.set_xdata(simTim)
        # line2A.set_ydata(opalrt_res_0)
        # #line2A.set_ydata(opalrt_res_1)
        # ax1.relim()
        # ax1.autoscale_view(True,True,True)
        # ax2.relim()
        # ax2.autoscale_view(True,True,True)
        # fig.canvas.draw()
        # if(tim==stop_time-stepsize):
        #     print ("Wait prior to closing")
        #     plt.waitforbuttonpress()
        # else:
        #     plt.pause(1)
        print ("Sleep for 270s")
        time.sleep(1)

    #plt.close()
if __name__ == "__main__":
    # Check command line options
    # The OPAL-RT model is running with a time factor of 1
    # The time factor is set in the model directly
    print ('Starting the simulation')
    start = datetime.now()
    run_simulator(2000)
    end = datetime.now()
    print('Ran a single co-simulation in {!s} seconds.'.format(
        (end - start).total_seconds()))
