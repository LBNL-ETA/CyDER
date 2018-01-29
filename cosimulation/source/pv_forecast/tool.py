from __future__ import division
import source.cymdist_tool.tool as cymdist
import datetime
import progressbar
import pandas
import time as s
import os
import subprocess
import matplotlib.pyplot as plt
import sys
try:
    import cympy
except:
    pass


class PVForecast(object):
    """Forecast EV demand at a feeder"""
    def __init__(self):
        self.configuration = None
        self.feeder = None
        self.configuration = None
        self.input_dir = None
        self.output_dir = None

    def initialize(self, feeder):
        """Initialize feeder inputs"""
        self.feeder = feeder
        self.configuration = feeder.configuration
        self.output_dir = feeder.directory

        # Select trained model within our database of models
        self.pv_input = pandas.read_excel(feeder.cyder_input_row.pv_forecast)
        self.input_dir = 'static\\pv\\' + str(self.pv_input.loc[0, 'zip_code']) + '\\'

    def forecast(self):
        """Forecast PV demand and return configuration file for CyDER"""
        # Save normalized generation with the right format
        pv_forecast = self._load_forecast()
        # pv_forecast = self.normalized_pv_generation()

        # Update the configuration file
        self._update_configuration(pv_forecast)

        # Read power demand and plot
        (pv_forecast).plot()
        plt.ylabel('Normalized PV forecast')
        plt.xlabel('Time')
        plt.show()
        return pv_forecast, self.configuration

    def _update_configuration(self, pv_forecast):
        """Update all pvs within feeder with the pv_forecast timeserie"""
        # Open model and get the devices from the first model
        cympy.study.Open(self.feeder.feeder_folder + self.feeder.feeder_name)
        pvs = cymdist.list_pvs()

        # GET FIRST TIME PV FORECAST <----
        start = pv_forecast.index[0]

        for index, time in enumerate(self.configuration['times']):
            dt = start + datetime.timedelta(seconds=time)
            for pv in pvs.itertuples():
                self.configuration['models'][index]['set_pvs'].append(
                    {'device_number': pv.device_number,
                     'generation': pv.generation * pv_forecast.loc[dt, 'profile'],
                     'description': 'pv forecast'})

    def normalized_pv_generation(self):
        """Return a time serie of normalized pv generation"""
        pv_nominal_generation_csv = pandas.read_csv(self.input_dir + 'pv_nominal_generation.csv')
        independent_inputs_csv = pandas.read_csv(self.input_dir + 'independent_inputs.csv')
        pv_ids = pv_nominal_generation_csv.columns.tolist()

        pv_nominal_generation = []
        for timestep in range(pv_nominal_generation_csv.shape[0]):
          pv_nominal_generation.append(pv_nominal_generation_csv.iloc[timestep, :].tolist())

        independent_inputs = []
        for timestep in range(independent_inputs_csv.shape[0]):
          independent_inputs.append(independent_inputs_csv.iloc[timestep, :].tolist())

        N, M, K = len(independent_inputs), len(independent_inputs[0]), len(pv_ids)
        assert(N == len(pv_nominal_generation))
        assert(K == len(pv_nominal_generation[0]))

        FANN_FILE = '..\\..\\..\\' + self.input_dir + 'fann.net'
        NARX_FILE = '..\\..\\..\\' + self.input_dir + 'narx.net'
        profile = self._predict_pv(
            (NARX_FILE, FANN_FILE),
            independent_inputs, pv_ids, pv_nominal_generation,
            forecast_interval_start=self.feeder.start)
        return profile

    def _predict_pv(self, nn_files, independent_inputs, pv_ids, pv_nominal_generation,
                   forecast_interval_start=None):
        """For every PV whose identifier is specified by PV_IDS, this method will use
           the INDEPENDENT_INPUTS coupled with the PV_NOMINAL_GENERATION to forecast
           into the future. All the predictions will be done with the neural network
           pointed at by NN_FILES.

        Keyword Arguments:
          nn_files: A tuple which contains of the following format:
                    (NARX_NET_FILE, FANN_NET_FILE)
          pv_ids: A list containing with len(pv_ids) = K where each element is a PV
                  identifier.
          independent_inputs: A list of lists where len(independent_inputs) = N and
                              len(independent_inputs[0]) = M and the contents are the
                              value of the independent inputs.
          pv_nominal_generation: A list of lists where len(pv_nominal_generation) = N
                                 and len(pv_nominal_generation[0]) = K and the contents
                                 are the values of the nominal generation.

        Returns:
          Writes one file for each of the pv_ids predicted values with
          the name pv_id-predict.csv
        """
        workdir = self.output_dir + 'pv-output/'
        FORECAST_MAIN_LOCATION='C:\\Users\\DRRC\\Desktop\\forecast-demo\\build\\src\\forecast_main.exe'
        narx_file, fann_file = nn_files
        narx_file_exists, fann_file_exists = os.path.isfile(narx_file), os.path.isfile(fann_file)

        if os.path.isdir(workdir) == False:
            os.makedirs(workdir)
        os.chdir(os.path.join(os.getcwd(), workdir))

        N, M, K = len(independent_inputs), len(independent_inputs[0]), len(pv_ids)
        assert(N == len(pv_nominal_generation))
        assert(K == len(pv_nominal_generation[0]))

        # Write out every input file for our neural network
        for i in range(K):
            f = open(str(pv_ids[i]) + '-inputs', 'w+')
            f.write('{} {} {}\n'.format(N, M + 1, 0))

            for j in range(N):
                combined = independent_inputs[j] + [pv_nominal_generation[j][i]]
                line = ' '.join(str(x) for x in combined) + '\n'
                f.write(line)

            f.close()

        # Run predictions
        averaged_predictions = pandas.DataFrame()
        for i in range(K):
            subprocess.call([FORECAST_MAIN_LOCATION,\
                          '--narx-file={}'.format(narx_file),\
                          '--fann-file={}'.format(fann_file),\
                          '--predict-file=' + str(pv_ids[i]) + '-inputs',],\
                          stdout=None)

            os.rename('predict-output.csv', str(pv_ids[i]) + '-predict.csv')

            predictions = pandas.read_csv(str(pv_ids[i]) + '-predict.csv')
            averaged_predictions['{}'.format(pv_ids[i])] = predictions.iloc[:,0]

        averaged_predictions = averaged_predictions.mean(axis=1)
        averaged_predictions.index = pandas.date_range(start=forecast_interval_start, \
                                                       periods=averaged_predictions.shape[0], \
                                                       freq='15Min')

        averaged_predictions.to_csv('all_predictions.csv')
        df = pandas.DataFrame(index=averaged_predictions.index,
                              data={'profile': averaged_predictions.values})
        os.chdir('../../../')
        return df

    def _load_forecast(self):
        """Load forecast from static file directly"""
        # Load prediction from file
        return pandas.read_csv(
            'static/pv/profile.csv', index_col=0, parse_dates=[0])
