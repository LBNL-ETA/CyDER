# This tests the uPMU FMU.
# This required the Python27 module requests 
# to be installed on the machine where the FMU is.
from pyfmi import load_fmu

model = load_fmu("me/pv.fmu")
model.setup_experiment(start_time=0, stop_time=1.0)
model.set("filNam", "USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos")
model.initialize()
# Enter event update mode
model.event_update()
# Enter continuous time mode
model.enter_continuous_time_mode()
model.time=0.0
print(model.get('PV_generation'))
model.time=43200
print(model.get('PV_generation'))
