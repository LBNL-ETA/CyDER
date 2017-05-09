from __future__ import print_function
from __future__ import division
import v2gsim
import pandas
import datetime
import v2gsim
import random
import numpy


def occupancy_to_itineraries(row, itinerary_db, df_itinerary_db, max_hour_parked=6):
    """return a frame of itineraries"""

    def activity_to_boolean(start, end, boolean):
        delta_minutes = int((end - start).total_seconds() / 60)
        return [boolean] * delta_minutes

    def fit_with_average_parked_duration(parked_duration, mean, std, duration_weight):
        return (1/(std * numpy.sqrt(2 * numpy.pi)) * numpy.exp( - (parked_duration - mean)**2 / (2 * std**2) ) * 10)**duration_weight

    # Load occupancy
    dfocc = pandas.read_pickle(row.occupancy_filename)

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
    x_hours = max_hour_parked
    veh_ids = veh.keys()
    for veh_id in veh_ids:
        # Remove vehicle
        if sum(veh[veh_id]) / 60 > x_hours:
            veh.pop(veh_id)

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

    while max_score > minimum_score and it < number_of_iteration:
        print(str(it) + ' / ', end='')

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

    # Down-select vehicles
    vehicle_ids = [scores[i]['vehicle_id'] for i in range(0, it)]
    return_df = df_itinerary_db[df_itinerary_db['Vehicle ID'].isin(vehicle_ids)]
    return_df = return_df.drop('Nothing', axis=1)
    return_df = return_df.rename(columns={'Vehicle ID': 'id', 'State': 'state',
                            'Start time (hour)': 'start',
                            'End time (hour)': 'end',
                            'Distance (mi)': 'distance',
                            'P_max (W)': 'maximum_power',
                            'Location': 'location',
                            'NHTS HH Wt': 'weight'})
    return_df = return_df.replace(row.location_name, row.node_name)
    return return_df


def itinerary_to_power_demand(df):
    """return power demand per node"""
    # Create a project and reduce the number of vehicles
    project = v2gsim.tool.project_from_csv(df)

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
    v2gsim.core.run(project, date_from=project.date,
                    date_to=project.date + datetime.timedelta(days=project.nb_days))

    # Get the results
    return v2gsim.post_simulation.result.total_power_demand(project)
