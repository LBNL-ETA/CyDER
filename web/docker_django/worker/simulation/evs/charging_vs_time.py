from __future__ import division
import v2gsim
import pandas
import numpy


def custom_save_location_state(location, timestep, date_from, date_to,
                               vehicle=None, activity=None,
                               power_demand=None, SOC=None, nb_interval=None,
                               init=False, run=False, post=False):
    """Save local results from a parked activity during running
    time. If date_from and date_to, set a fresh pandas DataFrame at locations.

    Args:
        location (Location): location
        timestep (int): calculation timestep
        date_from (datetime.datetime): date to start recording power demand
        date_to (datetime.datetime): date to end recording power demand
        vehicle (Vehicle): vehicle
        activity (Parked): parked activity
        power_demand (list): power demand from parked activity
        SOC (list): state of charge from the parked activity
        nb_interval (int): number of timestep for the parked activity

    Example:
        >>> # Initialize a result DataFrame for each location
        >>> save_power_demand_at_location(location, timestep, date_from=some_date,
                                          date_to=other_date)
        >>> # Save data during run time
        >>> save_power_demand_at_location(location, timestep, vehicle, activity,
                                          power_demand, nb_interval)
    """
    if run:
        activity_index1, activity_index2, location_index1, location_index2, save = v2gsim.result._map_index(
            activity.start, activity.end, date_from, date_to, len(power_demand),
            len(location.result['power_demand']), timestep)

        # Save a lot of interesting result
        if save:
            location.result['power_demand'][location_index1:location_index2] += (
                power_demand[activity_index1:activity_index2])

            # Add 'number_of_vehicle_parked' in the initialization section
            location.result['number_of_vehicle_parked'][location_index1:location_index2] += 1

            # Number of vehicle currently charging
            location.result['number_of_vehicle_charging'][location_index1:location_index2] += (
                [1 if power != 0.0 else 0 for power in power_demand])

    elif init:
        # Initiate a dictionary of numpy array to hold result (faster than DataFrame)
        location.result = {'power_demand': numpy.array([0.0] * int((date_to - date_from).total_seconds() / timestep)),
                           'number_of_vehicle_parked': numpy.array([0.0] * int((date_to - date_from).total_seconds() / timestep)),
                           'number_of_vehicle_charging': numpy.array([0.0] * int((date_to - date_from).total_seconds() / timestep))}

    elif post:
        # Convert location result back into pandas DataFrame (faster that way)
        i = pandas.date_range(start=date_from, end=date_to,
                              freq=str(timestep) + 's', closed='left')
        location.result = pandas.DataFrame(index=i, data=location.result)


# Create a project that will hold other objects such as vehicles, locations
# car models, charging stations and some results. (see model.Project class)
project = v2gsim.model.Project()

# Use the itinerary module to import itineraries from an Excel file.
# Instantiate a project with the necessary information to run a simulation.
# Default values are assumed for the vehicle to model
# and the charging infrastructures to simulate.
project = v2gsim.itinerary.from_excel(project, 'California.xlsx')

# This function from the itinerary module return all the vehicles that
# start and end their day at the same location (e.g. home)
project.vehicles = v2gsim.itinerary.get_cycling_itineraries(project)

# Remove all the vehicles that don't have a "home" location
home_vehicles = []
for vehicle in project.vehicles:
    home = False
    temp_distance = 0
    for activity in vehicle.activities:
        if isinstance(activity, v2gsim.model.Parked):
            if activity.location.category == 'Home':
                home = True
        if isinstance(activity, v2gsim.model.Driving):
            temp_distance += activity.distance
    if home and temp_distance > 20:
        home_vehicles.append(vehicle)

print('There was ' + str(len(project.vehicles)) + ' vehicles.')
project.vehicles = home_vehicles
print('New vehicle count is ' + str(len(project.vehicles)) + ' vehicles.')

# Some default infrastructure have been created for you, namely "no_charger",
# "L1" and "L2", you can change the probability of a vehicle to be plugged
# to one of those infrastructures at different locations as follow:
for location in project.locations:
    if location.category == 'Home':
        location.available_charging_station.loc['no_charger', 'probability'] = 0.0
        location.available_charging_station.loc['L1', 'probability'] = 1.0
        location.available_charging_station.loc['L2', 'probability'] = 0.0
    elif location.category == 'Work':
        location.available_charging_station.loc['no_charger', 'probability'] = 0.3
        location.available_charging_station.loc['L1', 'probability'] = 0.2
        location.available_charging_station.loc['L2', 'probability'] = 0.5
    else:
        location.available_charging_station.loc['no_charger', 'probability'] = 1.0
        location.available_charging_station.loc['L1', 'probability'] = 0.0
        location.available_charging_station.loc['L2', 'probability'] = 0.0

# Change the function to get result from locations
for location in project.locations:
    location.result_function = custom_save_location_state

# At first every vehicle start with a full battery. In order to start from
# a more realistic state of charge (SOC), we run some iterations of a day,
# to find a stable SOC for each vehicle at the end of the day.
# This value is then used as the initial SOC condition to a realistic state.
v2gsim.core.initialize_SOC(project, nb_iteration=3)

# Launch the simulation and save the results
v2gsim.core.run(project)

# Concatenate the power demand for each location into one frame.
# you can access the demand at any location by using "loactionName_demand"
# or access the total demand with "total".
total_power_demand = v2gsim.post_simulation.result.total_power_demand(project)

# Number of people charging
charging_vehicles = pandas.DataFrame(index=total_power_demand.index,
                                     data={'Total': [0] * len(total_power_demand),
                                           'Other': [0] * len(total_power_demand)})
charging_vehicles.index.rename('datetime', inplace=True)
for location in project.locations:
    if location.category == 'Home':
        charging_vehicles['Home'] = location.result.number_of_vehicle_charging
    elif location.category == 'Work':
        charging_vehicles['Work'] = location.result.number_of_vehicle_charging
    else:
        charging_vehicles['Other'] += location.result.number_of_vehicle_charging
    charging_vehicles['Total'] += location.result.number_of_vehicle_charging
charging_vehicles = charging_vehicles / len(project.vehicles)
charging_vehicles = charging_vehicles.resample('1S').interpolate()
charging_vehicles.to_csv('vehicle_charging.csv')
