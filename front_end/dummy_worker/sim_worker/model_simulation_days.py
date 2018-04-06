import scada
import solarprofile
import pandas

def get_simulation_days(modelName):
    """
    
    Args: model name as a string
    Returns: a python dictionnary
        keys are the feeder names
        Values are pandas Series listing the corresponding two minimum net load days (values indexed by timestamp) 
    """
    sc=scada.Scada('sim_worker/raw_SCADA/'+ modelName + '.csv') 
    #Total PV capacity is arbitrarily chosen to be 1MW
    so=solarprofile.solar_profile(sc.data.index[0],sc.data.index[-1],1000)
    S1=sc.data
    S2=so['GHI']
    
    #removes index duplicates in order to perform an outer join operation on the timestamp index
    S1=S1[~S1.index.duplicated()]
    S2=S2[~S2.index.duplicated()]
    
    #outer join operation on timestamp with solar values resampled by hourly mean
    df = pandas.concat([S2.resample('H').mean(), S1], axis=1, join='outer')
    
    #computes net load as NL=Load-PV
    df=df.iloc[:,1:].subtract(df.iloc[:,0], axis='index')
    x={}
    for col in df :
        temp=pandas.Series()
        #computes daily minimums for given feeder
        d=df[col].resample('D').min()
        for idx, month in d.groupby(d.index.month):
            #selects the two smallest daily net load minimums for each month
            temp=temp.append(month.nsmallest(2))
        x[col]=temp 
    return x
