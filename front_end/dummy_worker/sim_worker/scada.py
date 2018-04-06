import pandas


class Scada(object):
    """"""
    def __init__(self, scada_filename):
        """"""
        self.scada_filename = scada_filename
        self.data = pandas.read_csv(self.scada_filename, parse_dates=[0])
        self.data = self.data.set_index('TIME')
        self.feeders = [value.split('_')[0] for value in self.data.columns]

    def get(self, t):
        """"""
        # Select load from SCADA[]
        feeder_loads = {}
        index = self.data.index[self.data.index.get_loc(t)]
        for feeder in self.feeders:
            feeder_loads[feeder] = {'MW': self.data.loc[index, feeder + '_MW'],
                                  'MVAR': self.data.loc[index, feeder + '_MVAR']}
        return feeder_loads
