# Main Python function to be modified to interface with the main simulator.
from requests import get
from json import loads

def get_latest(uuid, server, fmu=True):
	#uuid from database
	#server inclusive port: http://[server]:[port] (standard BTrDB port is 9000)
	#fmu oprtion: print only value for FMU, or timestep and value if False

	r = get("{}/q/nearest/{}?time={}&backwards=true".format(server, uuid, 2524608000*10**9))
	if r.status_code == 200:
		if fmu:
			return loads(r.text.encode('ascii','ignore'))[1]
		else:
			return loads(r.text.encode('ascii','ignore'))
	else:
		return -1

def get_range(uuid, t_start, t_end, server, fmu=True):
	#uuid from database
	#t_start as start time of range in nano-seconds (unix time)
	#t_end as end time of range in nano-seconds (unix time)
	#server inclusive port: http://[server]:[port] (standard BTrDB port is 9000)
	#fmu oprtion: print only value for FMU, or timestep and value if False

	r = get("{}/data/uuid/{}?starttime={}&endtime={}&unitoftime=ns".format(server, uuid, t_start, t_end))
	if r.status_code == 200:
		if fmu:
			return [val for ts, val in loads(r.text.encode('ascii','ignore'))[0]['Readings']]
		else:
			return loads(r.text.encode('ascii','ignore'))[0]['Readings']
	else:
		return -1

if __name__ == "__main__":
    #Example code
    server = "http://yourhost:yourport"
    uuid = "youruuid"
    print 'Test of uPMU queries for {}\nat {}'.format(uuid, server)
    print 'Latest value as FMU:', get_latest(uuid, server)
    temp = get_latest_avg(uuid, server, False)
    print 'Latest value:', temp
    print 'Latest readings of the last 1 second (120 with uPMU):', len(get_range(uuid, temp[0]-1*10**9, temp[0], server))


def exchange(configuration_file, time, input_names,
            input_values, output_names, write_results):
    """
    Return  a list of output values from the Python-based Simulator.
    The order of the output values must match the order of the output names.

    :param configuration_file (String): Path to the Simulator model or configuration file
    :param time (Float): Simulation time
    :param input_names (Strings): Input names
    :param input_values (Floats): Input values (same length as input_names)
    :param output_names (Strings): Output names
    :param write_results (Float): Store results to file (1 to store, 0 else)

    Example:
        >>> configuration_file = 'config.json'
        >>> time = 0
        >>> input_names = 'v'
        >>> input_values = 220.0
        >>> output_names = 'i'
        >>> write_results = 0
        >>> output_values = simulator(configuration_file, time, input_names,
                        input_values, output_names, write_results)
    """
    # The assumption is that the uuid and the server name
    # are concatenated and separated by a :" in output_names.
    # This allows splitting the output_names and extracting those information
    if (isinstance(output_names, list)):
        output_values=[]
        for var in output_names:
            var = var.split(";")
            if(len(var)<2):
                s="The output name={!s} was incorrectly defined. The syntax must be server:uuid".format(var)
                raise ValueError(s)
            # Get the server name
            server=var[0]
            # Get the uuid which identifies the output
            # to be retrieved
            uuid=var[1]
            output_values.append(1.0 * float(get_latest(uuid, server, False)[1]))
            #output_values = 1.0 * float(output_values[1])
    return output_values
