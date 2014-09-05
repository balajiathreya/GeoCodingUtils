import sys, credentials, sqlite3, urllib2, json, time

'''
usage:
1. Add the google geocoding key to credentials.py
2. python latlngdbimporter.py DB_FILE TABLE_NAME LOCATION_COLUMN_INDEX 
3. comment out the call to addLatLngColumns the first time you run the script

Note:. Added a one second delay to querying the google API as it has some usage limits
'''

GOOG_GEOCODING_KEY = credentials.GOOG_GEOCODING_KEY

def main(argv):
	DB_FILE = argv[1]
	TABLE_NAME = argv[2]
	LOC_COL_INDEX = int(argv[3])
	
	conn = sqlite3.connect(DB_FILE)
	c = conn.cursor()
	#addLatLngColumns(c, TABLE_NAME)
	rows = c.execute('SELECT * FROM ' + TABLE_NAME )
	resultrows = list()
	for row in rows:
		resultrows.append(row)
	
	for row in resultrows:
		loc_name = row[LOC_COL_INDEX]
		row_id = row[0]
		if not 'TOTAL' in loc_name:
			location = get_loc_coords(loc_name)
			if location is not None:
				updateTable(c,location,TABLE_NAME,row_id)
				time.sleep(1)	
				print 'location: '+ str(location)
		else:
			print 'No blah for '+ str(row)
	conn.commit()
	conn.close()


def get_loc_coords(loc_name):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+loc_name+'&key='+GOOG_GEOCODING_KEY
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	data = response.read()
	resultJSON = json.loads(data)

	if resultJSON['status'] == 'OK':
		results = resultJSON['results'][0]
		location = results['geometry']['location']
		return location
		
	return None


def updateTable(c, location, table_name, row_id):
	update_query = 'UPDATE ' + table_name + ' SET LAT = ? , LNG = ? WHERE ID = ?'
	lat = location['lat']
	lng = location['lng']
	arr = [lat, lng, row_id]
	c.execute(update_query, arr)



def addLatLngColumns(c, table_name):
	c.execute('ALTER TABLE ' + table_name + ' ADD COLUMN LAT REAL')
	c.execute('ALTER TABLE ' + table_name + ' ADD COLUMN LNG REAL')	


if __name__ == "__main__":
	main(sys.argv)
