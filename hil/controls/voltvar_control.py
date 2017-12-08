import os
import sys
import numpy as N
import pylab as p

from pymodelica import compile_fmu
from pyfmi import load_fmu
from datetime import datetime

pat_to_lib=sys.argv[1]
nam_cla=sys.argv[2]
api=sys.argv[3]

def translate(with_plots=False):

    print "-------------- starting JModelica"
    print("This is CyDER_LIB={!s}".format(pat_to_lib))

    #class_names = [  "Annex60.Utilities.Math.SmoothMaxInline"   ]
    #class_names = [ "CyDER.HIL.Examples.Validate_VoltVarControl"]
    class_names = [nam_cla]
    print("This is class_names={!s}".format(class_names))

    for class_name in class_names:

        print "=================================================================="
        print "=== Compiling {}".format(class_name)
#        fmu_name = compile_fmu(class_name)
        fmu_name = compile_fmu(class_name, pat_to_lib, compiler_log_level = 'd',
                version = '2.0', target=api)
        #fmu_name = compile_fmu(class_name, compiler_options={'extra_lib_dirs':[ANNEX60_LIB, BUILDINGS_LIB]})

def simulate(with_plots=True):

    print "-------------- starting JModelica"

    class_names = ["CyDER.HIL.Examples.Validate_VoltVarControl"]

    for class_name in class_names:

        print "=================================================================="
        print "=== Compiling {}".format(class_name)
#        fmu_name = compile_fmu(class_name)
        fmu_name = compile_fmu(class_name, compiler_log_level = 'd', compiler_options={'extra_lib_dirs':[pat_to_lib]})

        model = load_fmu(fmu_name)
        opts = model.simulate_options() #Retrieve the default options
        opts['solver'] = 'CVode'
        opts['CVode_options']['atol'] = 1.0e-6 #Options specific for CVode
        opts['CVode_options']['store_event_points'] = False
        opts['ncp'] = 20
        print "=== Simulating {}".format(class_name)
#        res = model.simulate(final_time=86400)
        model.set_log_level(7)
        model.set_debug_logging(True)
        print("========= Starting simulation")
        res = model.simulate(options=opts, final_time=120)
#        res = model.simulate(start_time=0, final_time=final_time, options=opts)
        print model.get_log()
        print "========= Finished simulation of {}".format(class_name)

    if with_plots:
        fig = p.figure()
        p.plot(t, res['x'], t, res['y'])
        p.legend(('y'))
        p.show()

if __name__=="__main__":
    timediff=[]
    #simulate(with_plots=False)
    for i in range (1):
        tstart = datetime.now()
        translate(with_plots=False)
        tend = datetime.now()
        timediff.append((tend-tstart).seconds)
    print "==== This is the vector with different times " + str (timediff)
    print "=====The mean value of the time is " + str(N.mean(timediff))
    print "=====The total time simulation time is " + str(N.sum(timediff)/60) + "min."
