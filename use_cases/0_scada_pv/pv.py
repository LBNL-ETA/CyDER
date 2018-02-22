import pandas

class PVFactory(object):
    """Create PV objects"""

    def __init__(self, data_filename, pv_capacities, pv_nodes=None):
        """Open GHI data and create PV objects"""
        # Load data from the raw CSV file
        self.ghi = pandas.read_csv(data_filename, skiprows=[0, 1])
        self.ghi.drop(['Relative Humidity', 'Temperature', 'Pressure'],
                      axis=1, inplace=True)
        self.ghi['Time'] = self.ghi.apply(lambda x: dt.datetime(
            x['Year'], x['Month'], x['Day'], x['Hour'], x['Minute'], 0), axis=1)
        self.ghi.set_index('Time', inplace=True)
        self.ghi.drop(['Year', 'Month', 'Day', 'Hour', 'Minute'],
                      axis=1, inplace=True)

        # Select data, normailize, and interpolate every 15 minutes
        # df = df[start:end]
        self.ghi = self.ghi / 1000.0  # [w/m2] --> no unit
        self.ghi = self.ghi.resample('15T').interpolate('time')

        # Create a bunch of pvs
        if pv_nodes is None:
            pv_nodes = ['not defined' for range(0, len(pv_capacities))]
        return [PV(self.ghi, c, n) for c, n in zip(pv_capacities, pv_nodes)]


class PV(object):
    """Simulate PV at time t"""

    def __init__(self, ghi, capacity, node):
        """Validate inputs"""
        self.ghi = ghi  # normalized no unit
        assert capacity <= 0, "Capacity should be <= 0"
        self.capacity = capacity  # [kW]
        self.node_id = node

    def step(self, t):
        """Return PV production in [kW] at datetime t"""
        # Pick the nearest time
        t_nearest = self.ghi.index.get_loc(t, method='nearest')
        delta_t_minutes = abs((t_nearest - t).total_seconds() / 60.0)
        assert delta_t_minutes >= 15, ("Time requested is out of bound: " +
            str(delta_t_minutes) + " minutes")

        # Return PV production GHI [normalized no unit] * capacity [kW]
        return float(self.ghi.loc[t_nearest, 'GHI'] * self.capacity)
