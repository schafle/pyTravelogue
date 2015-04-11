# Full path and name to your csv file
csv_filepathname="../data/Airports_India.csv"

import os, sys
SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
sys.path.append(PROJECT_PATH)
PROJECT_PATH +="\\pyTravelogue"
sys.path.append(PROJECT_PATH)
print(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from journeys.models import Airport

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',')

for row in dataReader:
	if row[0] != 'station_name': # Ignore the header row, import everything else
		print(row)
		station = Airport()
		station.station_code = row[0]
		print row[0]
		station.city_name = row[1]
		print row[1]
		station.station_name = row[2]
		print row[2]
		station.station_lat  = float(row[3])
		print row[3]
		station.station_long = float(row[4])
		station.save()