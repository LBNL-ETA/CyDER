from __future__ import division
from pyfmi import load_fmu
from pyfmi.master import Master
import progressbar


class Master(object):
    """docstring for Master."""

    def __init__(self):
        # Simulation parameters
        self.feeder_configurations = None
        self.timestep = None
        self.times = None
        self.cymdist_fmu_path = './static/fmu/CYMDIST.fmu'
        self.griddyn_fmu_path = './static/fmu/griddyn14bus.fmu'
        self.save_to_file = 0
        self.feeder_voltage_reference = None

        # Simulation variables
        self.feeders = None
        self.feeder_input_valref = None
        self.feeder_output_valref = None
        self.transmission_input_valref = None
        self.transmission_output_valref = None
        self.transmission = None
        self.feeder_result = None
        self.transmission_result = None

        # CONSTANT
        self.feeder_input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'VANG_A', 'VANG_B', 'VANG_C']
        self.feeder_output_names = ['IA', 'IB', 'IC', 'IAngleA', 'IAngleB', 'IAngleC']
        self.transmission_input_names = None
        self.transmission_output_names = None

    def _initialize_feeders(self):
        """Initiliaze feeders"""
        # Initiliaze parameters
        feeder_configurations_bytes = []
        self.feeders = []
        self.feeder_input_valref = []
        self.feeder_output_valref = []
        self.feeder_result = []

        # Loop for each feeder model
        for feeder_conf in self.feeder_configurations:
            # Ask Thierry about this??
            feeder_configurations_bytes.append(bytes(feeder_conf, 'utf-8'))

            # Load FMUs
            self.feeders.append(load_fmu(self.cymdist_fmu_path, log_level=7))

            # Setup experiment
            self.feeders[-1].setup_experiment(
                start_time=self.times[0], stop_time=self.times[-1])

            # Create lists to hold value references
            self.feeder_input_valref.append([])
            self.feeder_output_valref.append([])

            # Get the value references of cymdist inputs
            for elem in self.feeder_input_names:
                self.feeder_input_valref[-1].append(self.feeders[-1].get_variable_valueref(elem))

            # Get the value references of cymdist outputs
            for elem in self.feeder_output_names:
                self.feeder_output_valref[-1].append(self.feeders[-1].get_variable_valueref(elem))

            # Set flag
            self.feeders[-1].set("_saveToFile", self.save_to_file)

            # Set configuration file
            ref = self.feeders[-1].get_variable_valueref("_configurationFileName")
            self.feeders[-1].set_string([ref], [feeder_configurations_bytes[-1]])

            # Initialize the FMUs
            self.feeders[-1].initialize()

            # Call event update prior to entering continuous mode.
            self.feeders[-1].event_update()
            self.feeders[-1].enter_continuous_time_mode()

            # Create holder for output variables
            self.feeder_result.append({name: [] for name in self.feeder_output_names})

    def _initialize_transmission_1bus(self):
        """Initialize transmission"""
        # Load GridDyn Fmu
        self.transmission = load_fmu(self.griddyn_fmu_path, log_level=7)

        # Set up experiment
        griddyn.setup_experiment(start_time=self.times[0], stop_time=self.times[-1])

        self.transmission_input_names = ['Bus11_IA', 'Bus11_IB', 'Bus11_IC',
                       'Bus11_IAngleA', 'Bus11_IAngleB', 'Bus11_IAngleC']
        self.transmission_output_names = ['Bus11_VA', 'Bus11_VB', 'Bus11_VC',
                'Bus11_VAngleA', 'Bus11_VAngleB', 'Bus11_VAngleC']

        # Create holders for the value reference
        self.transmission_input_valref = []
        self.transmission_output_valref = []

        # Get the value references of griddyn inputs
        for elem in self.transmission_input_names:
            self.transmission_input_valref.append(
                self.transmission.get_variable_valueref(elem))

        # Get the value references of griddyn outputs
        for elem in self.transmission_output_names:
            self.transmission_output_valref.append(
                self.transmission.get_variable_valueref(elem))


        # Set the value of the multiplier
        self.transmission.set('multiplier', 3.0)

        # Initialize
        self.transmission.initialize()

    def solve(self):
        """Launch a PyFMI simulation"""
        # Initialize feeders
        self._initialize_feeders()

        # Initialize transmission
        self._initialize_transmission_1bus()

        print('')
        print('Cosimulation in progress...')
        progress = progressbar.ProgressBar(widgets=['progress: ',
                                                    progressbar.Percentage(),
                                                    progressbar.Bar()],
                                           maxval=len(times)).start()

        # Co-simulation loop
        for iteration, time in enumerate(self.times):
            # Set feeder voltage reference and do step
            output_values_accross_all_feeders = []
            for index in range(0, len(self.feeders)):
                self.feeders[index].time = time
                self.feeders[index].set_real(
                    self.feeder_input_valref[index],
                    [self.feeder_voltage_reference[index]])

                # Save feeder results
                output_values = list(
                    self.feeders[index].get_real(self.feeder_output_valref))
                for name, value in zip(self.feeder_output_names, output_values):
                    self.feeder_result[index][name].append(value)

                # Save values for transmission
                output_values_accross_all_feeders.extend(output_values)

            # Set transmission current and do step
            self.transmission.set_real(
                self.transmission_input_valref,
                output_values_accross_all_feeders)
            self.transmission.do_step(
                current_t=time, step_size=self.timestep, new_step=0)

            # Save transmission results
            output_values = list(
                self.transmission.get_real(self.transmission_output_valref))
            for name, value in zip(self.transmission_output_names, output_values):
                self.transmission_result[name].append(value)
            progress.update(iteration)
        progress.finish()

        # Close all FMUs
        for index in range(0, len(self.feeders)):
            self.feeders[index].terminate()
        self.transmission.terminate()

        print("########## HOURRRA ##############")
