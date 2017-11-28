#This utility script provides support to get the latest value or a range of values from a uPMU database (BTrDB)
#Documentation of BTrDB: https://github.com/SoftwareDefinedBuildings/btrdb/blob/v3/httpinterface/httpinterface.go
#Christoph Gehbauer (cgehbauer@lbl.gov) 09/29/2017
 
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
	temp = get_latest(uuid, server, False)
	print 'Latest value:', temp
	print 'Latest readings of the last 1 second (120 with uPMU):', len(get_range(uuid, temp[0]-1*10**9, temp[0], server))