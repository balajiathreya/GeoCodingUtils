import sys, credentials, sqlite3, urllib2, json, time

'''
usage:
1. Add the google geocoding key to credentials.py
2. python latlngjsonimporter.py INPUT_JSON_FILE LOC_FIELD_NAME 

Note:. Added a one second delay to querying the google API as it has some usage limits
'''

GOOG_GEOCODING_KEY = credentials.GOOG_GEOCODING_KEY

def main(argv):
	INPUT_JSON_FILE = argv[1]
	LOC_FIELD_NAME = argv[2]

	json_data= json.load(open(INPUT_JSON_FILE))
	data = json_data['data']

	for i in range(4):
		entry = data[i]
		loc_name = entry[LOC_FIELD_NAME]
		print "Loc name : " + loc_name
		location = get_loc_coords(loc_name)

		if location is not None:
			entry['LAT'] = location['lat']
                        entry['LNG'] = location['lng']
			time.sleep(1)	
			print 'location: '+ str(location)
		else:
			print 'No blah for '+ loc_name


	with open(INPUT_JSON_FILE, 'w') as outfile:
		json.dump(json_data, outfile)	


def get_loc_coords(loc_name):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+loc_name+'&key='+GOOG_GEOCODING_KEY
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	data = response.read()
	resultJSON = json.loads(data)

	if resultJSON['status'] == 'OK':
		results = resultJSON['results'][0]
		location = results['geometry']['location']
		print location
		return location
		
	return None


if __name__ == "__main__":
	main(sys.argv)
