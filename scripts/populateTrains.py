# Full path and name to your csv file
csv_filepathname="data/trains_route.csv"
# Full path to your django project directory
your_djangoproject_home="D://Developement//Website//pyTravelogue//pyTravelogue"

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from journeys.models import Train

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',')

for row in dataReader:
	if row[0] != 'train_code': # Ignore the header row, import everything else
		print(row)
		train = Train()
		train.train_code = row[0]
		train.train_name = row[1]
		train.train_route = row[2]
		train.save()