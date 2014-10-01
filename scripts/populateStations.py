# Full path and name to your csv file
csv_filepathname="../data/station_latlong_new.csv"
# Full path to your django project directory
#your_djangoproject_home="D://Developement//Website//pyTravelogue//pyTravelogue"
import os
SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

import sys,os
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from journeys.models import Station

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',')

for row in dataReader:
	if row[0] != 'station_name': # Ignore the header row, import everything else
		print(row)
		station = Station()
		station.station_name = row[0]
		#Station.objects.get_or_create(station_name=row[0], station_code=row[1], station_lat=float(row[2]), station_long=float(row[3]))
		station.station_code = row[1]
		station.station_lat  = float(row[2])
		station.station_long = float(row[3])
		station.save()