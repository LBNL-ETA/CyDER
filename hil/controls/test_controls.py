# This tests the uPMU FMU.
# This required the Python27 module requests
# to be installed on the machine where the FMU is.
from pyfmi import load_fmu

model = load_fmu("me/controls.fmu")
model.setup_experiment(start_time=0, stop_time=1.0)
model.set("QMaxCap", 0.0)
model.set("QMaxInd", -15000.0)
model.set("thr", 0.05)
model.set("hys", 0.01)
model.initialize()
# Enter event update mode
model.event_update()
# Enter continuous time mode
model.enter_continuous_time_mode()

model.time=0.0
#model.set("v", 1.03)
#model.do_step(current_t=0.0, step_size=0.1)
#model.set("v", 1.03)
#model.do_step(current_t=0.1, step_size=0.1)
#print(model.get("QCon"))
#print(model.get("v"))
model.time=0.5
model.set("v", 1.02)
print(model.get("QCon"))
print(model.get("v"))
