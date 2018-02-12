from __future__ import print_function
from __future__ import division
import source.cymdist_tool.tool as cymdist
import v2gsim
import pandas
import datetime
import random
import numpy
import matplotlib.pyplot as plt
import progressbar
import traceback
try:
    import cympy
except:
    pass

class EVForecast(object):
    """Forecast EV demand at a feeder"""

    def __init__(self):
        self.ev_forecast = None
        self.vehicle_project = None
        self.directory = None
        self.pk = None
        self.feeder_timestep = None
        self.itinerary_path = None
        self.power_demand_path = None
        self.configuration = None

    def initialize(self, feeder):
        """Initialize feeder inputs"""
        self.ev_forecast = pandas.read_excel(feeder.cyder_input_row.ev_forecast)
        self.vehicle_project = pandas.read_excel(
            self.ev_forecast.loc[0, 'vehicle_parameters'], sheetname=None)
        self.directory = feeder.directory
        self.pk = feeder.pk
        self.feeder_timestep = feeder.timestep
        self.feeder = feeder
        self.itinerary_path = self.directory + str(self.pk) + '_itinerary.csv'
        self.power_demand_path = self.directory + str(self.pk) + '_power.csv'
        self.configuration = feeder.configuration

    def forecast(self):
        """Forecast EV demand and return configuration file for CyDER"""
        # Create an itinerary file from an occupancy schedule
        self._occupancy_to_itineraries()

        # Forecast power demand based on the an itinerary file
        power_demand = self._itineraries_to_power_demand()

        # Save power demand with the right format
        formatted_power_demand = self._save_power_demand(power_demand)

        # Update the configuration file
        self._update_configuration(formatted_power_demand)

        # Read power demand and plot
        (formatted_power_demand / 1000).plot()
        plt.ylabel('Power demand [kW]')
        plt.xlabel('Time')
        plt.show()
        return self.configuration

    def _open_itinerary_database(self):
        """Open itinerary database to pick itineraries"""
        # Create a V2G-Sim project
        itinerary_db = v2gsim.model.Project()

        # Initialize starting date before loading vehicles
        itinerary_db.date = self.vehicle_project['project'].loc[0, 'start_date']

        # Load vehicles into the V2G-Sim project
        print('')
        print('Loading itineraries...')
        df_itinerary_db = pandas.read_excel(
            io=self.ev_forecast.loc[0, 'itinerary_database'], sheetname='Activity')
        itinerary_db = v2gsim.itinerary.from_excel(
            itinerary_db, is_preload=True, df=df_itinerary_db)

        # Filter out vehicles that don't have a full cycle over the day
        # (avoid midnight mismatch)
        itinerary_db.vehicles = v2gsim.itinerary.get_cycling_itineraries(itinerary_db)
        return itinerary_db, df_itinerary_db

    def _preprocess_itinerary_database(self, row, itinerary_db):
        """Filter out itineraries before picking itineraries
        Return a dictionary containing boolean describing vehicle match with the
        occupancy schedule"""

        def activity_to_boolean(start, end, boolean):
            delta_minutes = int((end - start).total_seconds() / 60)
            return [boolean] * delta_minutes

        # Load occupancy
        dfocc = pandas.read_pickle(row.occupancy_filename)
        (dfocc.parked).plot()
        plt.ylabel('Number of vehicles')
        plt.xlabel('Time')
        plt.show()

        # Initiliaze vehicles
        # 1) Filter - Remove vehicle that don't have work places chargers
        veh = {}
        sub_vehicles = []
        for vehicle in itinerary_db.vehicles:
            for activity in vehicle.activities:
                if isinstance(activity, v2gsim.model.Parked):
                    if activity.location.category in row.location_name:
                        sub_vehicles.append(vehicle)
                        break

        for vehicle in sub_vehicles:
            veh[vehicle.id] = []
            for activity in vehicle.activities:
                if isinstance(activity, v2gsim.model.Parked):
                    if activity.location.category in row.location_name:
                        # Add the right number of minute as True
                        veh[vehicle.id].extend(activity_to_boolean(activity.start, activity.end, 1))
                    else:
                        # Add the right number of zeros
                        veh[vehicle.id].extend(activity_to_boolean(activity.start, activity.end, 0))
                else:
                    # Add the right number of zeros
                    veh[vehicle.id].extend(activity_to_boolean(activity.start, activity.end, 0))
            if len(veh[vehicle.id]) != 1440:
                import pdb
                pdb.set_trace()

        # 2) Filter - remove vehicle parked more than x hours at work
        x_hours = 6
        veh_ids = veh.keys()
        for veh_id in list(veh_ids):
            # Remove vehicle
            if sum(veh[veh_id]) / 60 > x_hours:
                veh.pop(veh_id)
        return veh, dfocc

    def _select_itineraries(self, veh, dfocc):
        """Match occupancy schedule with itineraries and return vehicle ids"""

        def fit_with_average_parked_duration(parked_duration, mean, std, duration_weight):
            return (1/(std * numpy.sqrt(2 * numpy.pi)) * numpy.exp( - (parked_duration - mean)**2 / (2 * std**2) ) * 10)**duration_weight
        # Initialize occupancy
        occ = {}
        occ[0] = dfocc.parked[0:-1].tolist()  # Remove last value

        # Scoring process and update of the new occupancy
        number_of_iteration = 100
        it = 0
        minimum_score = 0
        max_score = 999
        mean_duration, std_duration = 3, 2
        duration_weight = 1.5  # How much should the scoring system prefere vehicle with mean_duration
        remove_vehicle = True
        temp_veh = veh.copy()
        scores = {}

        # Create the progress bar
        print('')
        print('Selecting itineraries...')
        progress = progressbar.ProgressBar(widgets=['progress: ',
                                                    progressbar.Percentage(),
                                                    progressbar.Bar()],
                                           maxval=number_of_iteration).start()

        while max_score > minimum_score and it < number_of_iteration:

            # Score each vehicle
            temp_scores = []
            for veh_id in temp_veh:
                temp_scores.append([sum([occ[it][i]
                                        if temp_veh[veh_id][i] > 0
                                        else 0
                                        for i in range(0, len(occ[it]))]), veh_id, sum(temp_veh[veh_id]) / 60])
                temp_scores[-1][0] *= fit_with_average_parked_duration(temp_scores[-1][2], mean_duration, std_duration, duration_weight)

            # Find the vehicle with the best score and save stats
            scores[it] = {}
            scores[it]['max'], scores[it]['vehicle_id'], scores[it]['duration'] = max(temp_scores, key=lambda item:item[0])
            scores[it]['average'] = sum([pair[0] for pair in temp_scores]) / len(temp_scores)
            max_score = scores[it]['max']

            # Get the next occ
            occ[it + 1] = [occ[it][i] - 1
                           if temp_veh[scores[it]['vehicle_id']][i] > 0
                           else occ[it][i]
                           for i in range(0, len(occ[it]))]

            # Remove vehicle
            if remove_vehicle:
                temp_veh.pop(scores[it]['vehicle_id'])

            # Increase iteration
            it += 1
            progress.update(it)
        progress.finish()
        return [scores[i]['vehicle_id'] for i in range(0, it)]

    def _postprocess_selected_itineraries(self, row, vehicle_ids, df_itinerary_db):
        """Create a dataframe using the itinerary database with only the chosen vehicles"""
        # Down select vehicle within the big pool of vehicles
        return_df = df_itinerary_db[df_itinerary_db['Vehicle ID'].isin(vehicle_ids)]
        return_df = return_df.drop('Nothing', axis=1)
        return_df = return_df.rename(columns={'Vehicle ID': 'id', 'State': 'state',
                                'Start time (hour)': 'start',
                                'End time (hour)': 'end',
                                'Distance (mi)': 'distance',
                                'P_max (W)': 'maximum_power',
                                'Location': 'location',
                                'NHTS HH Wt': 'weight'})
        return_df = return_df.replace(row.location_name, row.load_name)
        return return_df

    def _occupancy_to_itineraries(self):
        """Load occupancy schedule and create a new itinerary file"""
        # Open and instantiate the itinerary database
        itinerary_db, df_itinerary_db = self._open_itinerary_database()

        # For each occupancy schedule pick itineraries
        itineraries = []
        for row in self.ev_forecast.itertuples():
            veh, occupancy = self._preprocess_itinerary_database(row, itinerary_db)
            vehicles_ids = self._select_itineraries(veh, occupancy)
            itineraries.append(self._postprocess_selected_itineraries(
                row, vehicles_ids, df_itinerary_db))

        # Merge all itineraries into a single file
        itinerary = pandas.DataFrame()
        for frame in itineraries:
            itinerary = pandas.concat([itinerary, frame], axis=1)
        itinerary.to_csv(self.itinerary_path)

    def _itineraries_to_power_demand(self):
        """Return power demand per node from a standart itinerary file"""
        df = self.vehicle_project

        # Create a project and reduce the number of vehicles
        project = v2gsim.tool.project_from_csv(df, filename=self.itinerary_path)

        # Set number of vehicles
        df['vehicle_stock'].loc[0, 'number_of_vehicles'] = int(len(project.vehicles) * 0.3)
        df['vehicle_stock'].loc[1, 'number_of_vehicles'] = int(len(project.vehicles) * 0.7)

        # Load car models
        project.car_models = v2gsim.tool.car_model_from_excel(df, project.ambient_temperature)

        # Assign car model to vehicles
        scaling = v2gsim.tool.assign_car_model(df, project)

        # Load infrastructure description
        project.charging_stations = v2gsim.tool.charging_stations_from_excel(df)

        # Set available infrastructures at locations
        v2gsim.tool.set_available_infrastructures_at_locations_v2(df, project)

        # Change the function to get result from locations
        for location in project.locations:
            location.result_function = v2gsim.tool.custom_save_location_state

        # Change the way charging station behave
        for station in project.charging_stations:
            station.charging = v2gsim.charging.uncontrolled.charge_soc_dependent

        # Launch the simulation
        print('')
        print('Forecasting power demand...')
        v2gsim.core.run(project, date_from=project.date,
                        date_to=project.date + datetime.timedelta(days=project.nb_days))

        # Get the results
        return v2gsim.post_simulation.result.total_power_demand(project)

    def _save_power_demand(self, power_demand):
        """Save power demand with the right timestep for a selection of load"""
        # Export results to a flat format
        timestep_min = str(int(self.feeder_timestep  / 60)) + 'T'
        nb_days = (self.vehicle_project['project'].loc[0, 'end_date'] - self.vehicle_project['project'].loc[0, 'start_date']).days
        tsd = self.vehicle_project['project'].loc[0, 'start_date'] + datetime.timedelta(days=nb_days - 1)
        ted = self.vehicle_project['project'].loc[0, 'end_date']
        load_names = self.ev_forecast.load_name.unique().tolist()
        load_names_demand = [value + '_demand' for value in load_names]
        power_demand = power_demand[tsd:ted][load_names_demand].resample(timestep_min).last()
        power_demand.to_csv(self.power_demand_path)
        return power_demand

    def _update_configuration(self, power_demand):
        """Update configuration file with EV consumption at load"""
        # Open model and list the loads
        cympy.study.Open(self.feeder.feeder_folder + self.feeder.feeder_name)
        loads = cymdist.list_loads()

        # Select loads of interest
        load_ids = [value.split('_')[1] for value in power_demand.columns.tolist()]
        loads = loads[loads.device_number.isin(load_ids)]

        # Loop over time window
        for index, time in enumerate(self.configuration['times']):
            for load, column_name in zip(loads.iterrows(), power_demand.columns.tolist()):
                _, load = load
                self.configuration['models'][index]['set_loads'].append(
                    {'device_number': load['device_number'],
                     'active_power': [],
                     'description': 'ev forecast'})

                # Dummy way to count the phases
                phase_count = 0
                for phase_index in ['0', '1', '2']:
                    if load['activepower_' + phase_index]:
                        phase_count += 1

                current_time = self.feeder.start + datetime.timedelta(seconds=time)
                power_to_add = power_demand.loc[current_time, column_name] / (1000 * phase_count)
                for phase_index in ['0', '1', '2']:
                    if load['activepower_' + phase_index]:
                        self.configuration['models'][index]['set_loads'][-1]['active_power'].append(
                            {'active_power': float(load['activepower_' + phase_index]) + power_to_add,
                             'phase_index': phase_index,
                             'phase': str(load['phase_' + phase_index])})
