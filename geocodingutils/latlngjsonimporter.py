import sys, credentials, sqlite3, urllib2, json, time, urllib


'''
usage:
1. Add the google geocoding key to credentials.py
2. python latlngjsonimporter.py INPUT_JSON_FILE LOC_FIELD_NAME LOC_QUALIFIER

Note:. Added a one second delay to querying the google API as it has some usage limits
'''

GOOG_GEOCODING_KEY = credentials.GOOG_GEOCODING_KEY

def main(argv):
	INPUT_JSON_FILE = argv[1]
	LOC_FIELD_NAME = argv[2]
	LOC_QUALIFIER = argv[3]
	json_data= json.load(open(INPUT_JSON_FILE))
	data = json_data['data']

	for entry in data:
		loc_name = entry[LOC_FIELD_NAME]
		print "Loc name : " + loc_name
		location = get_loc_coords(loc_name, LOC_QUALIFIER)

		if location is not None:
			entry['LAT'] = location['lat']
                        entry['LNG'] = location['lng']
			time.sleep(1)	
			print 'location: '+ str(location)
		else:
			print 'No blah for '+ loc_name


	with open(INPUT_JSON_FILE, 'w') as outfile:
		json.dump(json_data, outfile)	


def get_loc_coords(loc_name,loc_qualifier):
	full_loc = loc_name + ',' + loc_qualifier
	params = {'address':full_loc, 'key':GOOG_GEOCODING_KEY}
	url = 'https://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(params)

	req = urllib2.Request(url)

	try:
		response = urllib2.urlopen(req)
		data = response.read()
		resultJSON = json.loads(data)

		if resultJSON['status'] == 'OK':
			results = resultJSON['results'][0]
			geometry = results['geometry']			
			if 'bounds' in geometry:
				location = geometry['bounds']['northeast']
				print location
				return location
	except urllib2.HTTPError, err:
		print err
	return None


if __name__ == "__main__":
	main(sys.argv)
